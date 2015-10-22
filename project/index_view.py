from django.views.generic.base import TemplateView
from elastic_json.models import Student
from elasticsearch import Elasticsearch
from copy import deepcopy


client = Elasticsearch()


def convert_hit_to_template(hit1):
    hit = deepcopy(hit1)
    almost_ready = hit['_source']
    almost_ready['pk'] = hit['_id']
    return almost_ready


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        body = {
            'aggs': {
                'course_names': {
                    'terms': {
                        'field': 'course_names', 'size': 0
                    }
                },
                'university': {
                    'terms': {
                        'field': 'university.name'
                    }
                },
                'year_in_school': {
                    'terms': {
                        'field': 'year_in_school'
                    }
                },
            },
            'query': {'match_all': {}}
        }

        cc = client.search(index='django', doc_type='student', body=body)
        # request = self.request
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['hits'] = [convert_hit_to_template(c) for c in cc['hits']['hits']]
        context['aggregations'] = cc['aggregations']
        return context
