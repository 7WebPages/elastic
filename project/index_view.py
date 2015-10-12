from django.views.generic.base import TemplateView
from elastic_django.models import MyModel


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['facets'] = MyModel.es.search('').facet(['age', 'year_in_school']).facets
        return context
