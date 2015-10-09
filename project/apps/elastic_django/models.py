from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_elasticsearch.models import EsIndexable


class MyModel(EsIndexable, models.Model):
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

    class Elasticsearch(EsIndexable.Elasticsearch):
        mappings = {
            'name': {'boost': 3.0},
        }
        facets_fields = ['year_in_school', 'age']
        completion_fields = ['name']
