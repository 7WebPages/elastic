import json
from django.http import HttpResponse

from elasticsearch import Elasticsearch
client = Elasticsearch()


def autocomplete_view(request):
    query = request.GET.get('term', '')
    resp = client.suggest(
        index='django',
        body={
            'name_complete': {
                "text": query,
                "completion": {
                    "field": 'name_complete',
                }
            }
        }
    )
    data = json.dumps(resp['hits'])
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
