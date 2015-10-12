from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from elastic_django.views import autocomplete_view, search_view
from project.index_view import HomePageView


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', search_view, name='search-view'),
    url(r'^autocomplete/', autocomplete_view, name='autocomplete-view'),
    url(r'', HomePageView.as_view())
]

if settings.DEBUG:
    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        import debug_toolbar
        urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
