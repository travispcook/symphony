from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView
from rest_framework import routers
from library import serializers

urlpatterns = patterns('',
    url(r'^$', 'library.views.app_index', name='app'),
)


# django rest framework section
router = routers.DefaultRouter()

router.register(r'artist', serializers.ArtistViewSet,)
router.register(r'piece', serializers.PieceViewSet,)
router.register(r'scoretype', serializers.ScoreTypeViewSet,)
router.register(r'container', serializers.ContainerViewSet,)
router.register(r'orchestra', serializers.OrchestraViewSet,)
router.register(r'performance', serializers.PerformanceViewSet,)


urlpatterns += patterns('', 
	url(r'^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

