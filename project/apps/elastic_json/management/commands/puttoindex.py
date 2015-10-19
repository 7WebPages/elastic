from django.core.management.base import BaseCommand
import json
import requests
from elastic_json.models import Student


class Command(BaseCommand):
    help = "generates elasticsearch indexes described in models."

    def handle(self, *args, **options):
        put_all_to_index(Student)


def put_all_to_index(model_name):
    url = 'http://localhost:9200/_bulk'
    data = [convert_for_bulk(s, 'create') for s in model_name.objects.all()]
    data_serialized = '%s\n' % '\n'.join(data)
    resp = requests.post(url, data=data_serialized)
    resp_data = resp.json()
    assert resp_data['errors'] is False
    assert len(resp_data)['items'] == len(data)


def convert_for_bulk(django_object, action=None):
    if not action:
        raise AttributeError('no action specified')
    data = django_object.es_repr()
    metadata = {
        action: {
            "_index": django_object._meta.es_index_name,
            "_type": django_object._meta.es_type_name,
            "_id": data['_id']
        }
    }
    return '\n'.join(
        (json.dumps(metadata), json.dumps(data))
    )
