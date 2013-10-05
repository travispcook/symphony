from django.conf.urls.defaults import patterns, url, include
from library.api import router

urlpatterns = patterns(
    '',
    url(r'^$', 'library.views.app_index', name='app'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
)
