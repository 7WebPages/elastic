from django.views.generic.base import TemplateView
from elastic_json.models import Student
from elasticsearch import Elasticsearch


client = Elasticsearch()


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
        context['facets'] = Student.es.search('').facet(['age', 'year_in_school']).facets
        return context
