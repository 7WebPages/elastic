from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


class University(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'elastic_django_university'


class Course(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'elastic_django_course'


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
    name = models.CharField(max_length=255)
    # various relationships models
    university = models.ForeignKey(University, null=True, blank=True)
    courses = models.ManyToManyField(Course, null=True, blank=True)

    class Meta:
        db_table = 'elastic_django_student'
        es_index_name = 'django'
        es_type_name = 'student'
        es_mapping = {
            'properties': {
                "_id": {
                    "index": "not_analyzed",
                    "store": True
                },
                'university': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'index': 'not_analyzed'},
                        'sid': {'type': 'string', 'index': 'not_analyzed'}
                    }
                },
                'name': {'type': 'string', 'index': 'not_analyzed'},
                'age': {'type': 'short'},
                'year_in_school': {'type': 'string'},
                'name_complete': {
                    'type': 'completion',
                    'analyzer': 'simple',
                    'payloads': False,
                    'preserve_separators': True,
                    'preserve_position_increments': True,
                    'max_input_length': 50
                },
            }
        }


    # class Elasticsearch(EsIndexable.Elasticsearch):
    #     mappings = {
    #         'name': {'boost': 3.0},
    #         'university': {
    #             'type': 'nested',
    #             'properties': {
    #                 'name': {'type': 'string'},
    #             }
    #         }
    #     }
    #     facets_fields = ['year_in_school', 'age']
    #     completion_fields = ['name']
