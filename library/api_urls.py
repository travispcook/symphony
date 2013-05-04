from django.conf.urls.defaults import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from library.api import ArtistList, ArtistDetail

urlpatterns = patterns('library.api',
    url('^$', 'api_root'),
    url('^artists/$', ArtistList.as_view(), name='artist-list'),
    url('^artists/(?P<pk>\d+)/$', ArtistDetail.as_view(), name='artist-detail'),
)


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])


# default login/logout views
# TODO
