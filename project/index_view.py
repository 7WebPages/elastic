from django.views.generic.base import TemplateView
from elastic_json.models import Student
from urllib import urlencode
from elasticsearch import Elasticsearch
from copy import deepcopy


client = Elasticsearch()


def convert_hit_to_template(hit1):
    hit = deepcopy(hit1)
    almost_ready = hit['_source']
    almost_ready['pk'] = hit['_id']
    return almost_ready


def facet_url_args(url_args, field_name, field_value):
    if url_args.get(field_name):
        base_list = url_args[field_name].split(',')
        if field_value in base_list:
            del base_list[base_list.index(field_value)]
        else:
            base_list.append(field_value)
        url_args[field_name] = ','.join(base_list)
    else:
        url_args[field_name] = field_value
    return url_args


def prepare_facet_data(aggregations_dict, get_args):
    resp = {}
    for area in aggregations_dict.keys():
        resp[area] = []
        for item in aggregations_dict[area]['buckets']:
            url_args = facet_url_args(
                url_args=deepcopy(get_args.dict()),
                field_name=area,
                field_value=item['key']
            )
            resp[area].append({
                'url_args': urlencode(url_args),
                'name': item['key'],
                'count': item['doc_count']
            })
    return resp


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
        context['aggregations'] = prepare_facet_data(
            cc['aggregations'],
            self.request.GET
        )
        return context
