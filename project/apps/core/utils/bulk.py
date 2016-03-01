from elasticsearch.helpers import bulk
from django.conf import settings


def put_all_to_index(model_name):
    es = settings.ES_CLIENT
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
