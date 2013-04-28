from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'library.views.app_index', name='app'),
)
