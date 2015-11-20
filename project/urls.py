from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from elastic_json.views import autocomplete_view, student_detail
from project.index_view import HomePageView


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', autocomplete_view, name='autocomplete-view'),
    url(r'^student/$', student_detail, name='student-detail'),
    url(r'', HomePageView.as_view(), name='index-view')
]

if settings.DEBUG:
    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

        import debug_toolbar
        urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
