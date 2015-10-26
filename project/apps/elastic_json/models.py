from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import django.db.models.options as options
from django.apps import apps
from elasticsearch import Elasticsearch


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping', 'es_related'
)
es_client = Elasticsearch()


class University(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        # es_related = [('Student', 'university')]
        es_related = ['elastic_json.models.Student']

    def save(self, *args, **kwargs):
        super(type(self), self).save(*args, **kwargs)
        for watcher in self._meta.es_related:
            if isinstance(watcher, tuple):
                watcher_name, related_field_name = watcher
            else:
                watcher_name = watcher
                related_field_name = self._meta.model_name
            watcher_app = watcher_name.split('.')[0]
            watcher_modelname = watcher_name.split('.')[-1].lower()
            all_models = apps.get_models()
            watcher_model = [
                m for m in all_models
                if m._meta.app_label == watcher_app
                and m._meta.model_name == watcher_modelname
            ][0]

            qs = watcher_model.objects.filter(
                **{
                    '%s_id' % related_field_name: self.pk
                }
            ).values_list('pk', flat=True)
            for item_pk in qs:
                item = watcher_model.objects.get(pk=item_pk)
                item.push_field_to_index(related_field_name)


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    # note: incorrect choice in MyModel.create leads to creation of incorrect record
    year_in_school = models.CharField(
        max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    age = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # various relationships models
    university = models.ForeignKey(University, null=True, blank=True)
    courses = models.ManyToManyField(Course, null=True, blank=True)

    class Meta:
        es_index_name = 'django'
        es_type_name = 'student'
        # we make some assumptions:
        # 1. all model's fields have same names in elasticsearch index.
        # 2. django's id is stored in _id field
        # 3. in case you want autocomplete - name the field xxx_complete
        #    and provide get_es_xxx method.
        # 4. in case you want to put related objects - please, name them
        #    in the same way like in model.
        es_mapping = {
            "_id": {
                "store": True,
                'index': 'not_analyzed'
            },
            'properties': {
                # so that we're able to filter or generate facets based on university
                # here, we could've used pure university_name, but this is just
                # an example to illustrate elasticsearch/django
                'university': {
                    'type': 'object',
                    "_id": {
                        "store": True,
                        'index': 'not_analyzed'
                    },
                    'properties': {
                        'name': {'type': 'string', 'index': 'not_analyzed'},
                    }
                },
                'first_name': {'type': 'string', 'index': 'not_analyzed'},
                'last_name': {'type': 'string', 'index': 'not_analyzed'},
                'age': {'type': 'short'},
                'year_in_school': {'type': 'string'},
                'name_complete': {
                    'type': 'completion',
                    'analyzer': 'simple',
                    'payloads': True,  # note that we have to provide payload while updating
                    'preserve_separators': True,
                    'preserve_position_increments': True,
                    'max_input_length': 50,
                },
                # as elasticsearch doesn't require array to be specified, we
                # just put string here. As a result, this will be list of strings.
                "course_names": {
                    "type": "string", "store": "yes", "index": "not_analyzed",
                    'method': 'get_es_course_names'
                },
            }
        }

    def es_repr(self):
        data = {}
        mapping = self._meta.es_mapping
        if not isinstance(mapping, dict) or not mapping.get('properties'):
            raise TypeError('bad configuration of elasticsearch mapping')

        if mapping.get('_id'):
            data['_id'] = self.pk

        for field_name in mapping['properties'].keys():
            data[field_name] = self.field_es_repr(field_name)
        return data

    def get_field_config(self, field_name):
        return self._meta.es_mapping['properties'][field_name]

    def field_es_repr(self, field_name):
        config = self.get_field_config(field_name)
        if config['type'] == 'object':
            try:
                related_object = getattr(self, field_name)
                obj_data = {}
                if config.get('_id'):
                    obj_data['_id'] = related_object.pk
                    for prop in config['properties'].keys():
                        obj_data[prop] = getattr(related_object, prop)
            except AttributeError:
                obj_data = getattr(self, 'get_es_%s' % field_name)()
            field_es_value = obj_data

        elif config['type'] == 'completion':
            field_es_value = getattr(self, 'get_es_%s' % field_name)()

        else:
            if config.get('method'):
                field_es_value = getattr(self, config['method'])()
            else:
                field_es_value = getattr(self, field_name)
        return field_es_value

    def get_es_name_complete(self):
        return {
            "input": [self.first_name, self.last_name],
            "output": "%s %s" % (self.first_name, self.last_name),
            "payload": {"pk": self.pk},
        }

    def get_es_course_names(self):
        if not self.courses.exists():
            return []
        return [c.name for c in self.courses.all()]

    def push_field_to_index(self, field_name):
        data = self.field_es_repr(field_name)
        es_client.update(
            index=self._meta.es_index_name,
            doc_type=self._meta.es_type_name,
            id=self.pk,
            body={
                'doc': {
                    field_name: data
                }
            }
        )
