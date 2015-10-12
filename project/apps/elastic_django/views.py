import json
from django.http import HttpResponse

from .models import MyModel


def search_view(request):
    pass


def autocomplete_view(request):
    q = request.GET.get('term', '')
    results = MyModel.es.complete('name', q)
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
