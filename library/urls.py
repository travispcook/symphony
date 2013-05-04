from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', 'library.views.app_index', name='app'),
)
