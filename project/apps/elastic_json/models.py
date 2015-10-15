from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


class University(models.Model):
    name = models.CharField(max_length=255, unique=True)


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
                    'max_input_length': 50
                },
                # as elasticsearch doesn't require array to be specified, we
                # just put string here. As a result, this will be list of strings.
                "course_names": {"type": "string", "store": "yes", "index": "not_analyzed"},
            }
        }
