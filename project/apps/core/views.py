import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .models import Student


client = settings.ES_CLIENT


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
    student_id = request.GET.get('student_id')
    student = Student.objects.get(pk=student_id)
    return render(request, 'student-details.html', context={'student': student})

