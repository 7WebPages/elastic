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
    is_active = False
    if url_args.get(field_name):
        base_list = url_args[field_name].split(',')
        if field_value in base_list:
            del base_list[base_list.index(field_value)]
            is_active = True
        else:
            base_list.append(field_value)
        url_args[field_name] = ','.join(base_list)
    else:
        url_args[field_name] = field_value
    return url_args, is_active


def prepare_facet_data(aggregations_dict, get_args):
    resp = {}
    for area in aggregations_dict.keys():
        resp[area] = []
        for item in aggregations_dict[area]['buckets']:
            url_args, is_active = facet_url_args(
                url_args=deepcopy(get_args.dict()),
                field_name=area,
                field_value=item['key']
            )
            resp[area].append({
                'url_args': urlencode(url_args),
                'name': item['key'],
                'count': item['doc_count'],
                'is_active': is_active
            })
    return resp


def gen_es_query(request):
    req_dict = deepcopy(request.GET.dict())
    if not req_dict:
        return {'match_all': {}}
    filters = []
    for field_name in req_dict.keys():
        if '__' in field_name:
            filter_field_name = field_name.replace('__', '.')
        else:
            filter_field_name = field_name
        for field_value in req_dict[field_name].split(','):
            if not field_value:
                continue
            filters.append(
                {
                    'term': {filter_field_name: field_value},
                }
            )
    return {
        'filtered': {
            'query': {'match_all': {}},
            'filter': {
                'bool': {
                    'must': filters
                }
            }
        }
    }


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
                'university__name': {
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
            # 'query': {'match_all': {}}
        }
        es_query = gen_es_query(self.request)
        body.update({'query': es_query})
        cc = client.search(index='django', doc_type='student', body=body)

        context = super(HomePageView, self).get_context_data(**kwargs)
        context['hits'] = [convert_hit_to_template(c) for c in cc['hits']['hits']]
        context['aggregations'] = prepare_facet_data(
            cc['aggregations'],
            self.request.GET
        )
        return context
