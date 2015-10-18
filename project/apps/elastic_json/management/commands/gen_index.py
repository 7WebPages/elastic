from django.core.management.base import BaseCommand
import json
import requests
from elastic_json.models import Student


class Command(BaseCommand):
    help = "generates elasticsearch indexes described in models."

    def handle(self, *args, **options):
        mapping = Student._meta.es_mapping
        index = Student._meta.es_index_name
        type_name = Student._meta.es_type_name
        # we have to take "method" fields from mapping, as it's internal word
        url = 'http://localhost:9200/%s/_mapping/%s' % (index, type_name)
        resp = requests.put(url, data=json.dumps(mapping))
        assert resp.text == '{"acknowledged":true}'
