import json
from django.http import HttpResponse

from elasticsearch import Elasticsearch
from .models import Student


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
    options = resp['name_complete'][0]['options']
    data = json.dumps(
        [{'id': i['payload']['pk'], 'value': i['text']} for i in options]
    )
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def student_detail(request):
    return Student.objects.get(pk=student_id)

