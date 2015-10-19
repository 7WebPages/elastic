from django.core.management.base import BaseCommand
from elastic_json.models import Student
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = "generates elasticsearch indexes described in models."

    def handle(self, *args, **options):
        put_all_to_index(Student)


def put_all_to_index(model_name):
    es = Elasticsearch()
    data = [convert_for_bulk(s, 'create') for s in model_name.objects.all()]
    bulk(client=es, actions=data, stats_only=True)


def convert_for_bulk(django_object, action=None):
    if not action:
        raise AttributeError('no action specified')
    data = django_object.es_repr()
    metadata = {
        '_op_type': action,
        "_index": django_object._meta.es_index_name,
        "_type": django_object._meta.es_type_name,
    }
    data.update(**metadata)
    return data
