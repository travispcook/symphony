from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'library.views.app_index', name='app'),
)
