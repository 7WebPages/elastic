import json
from django.http import HttpResponse

from .models import Student


def search_view(request):
    pass


def autocomplete_view(request):
    q = request.GET.get('term', '')
    results = Student.es.complete('name', q)
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
