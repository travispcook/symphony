from django.conf.urls.defaults import *
from tastypie.api import Api

from library.api import (PieceResource, ComposerResource, ArrangerResource,
    CabinetGroupResource, CabinetResource, DrawerResource, ScoreTypeResource,
    OrchestraResource, PerformanceResource)

v1_api = Api(api_name='v1')
v1_api.register(PieceResource())
v1_api.register(ComposerResource())
v1_api.register(ArrangerResource())
v1_api.register(CabinetGroupResource())
v1_api.register(CabinetResource())
v1_api.register(DrawerResource())
v1_api.register(ScoreTypeResource())
v1_api.register(OrchestraResource())
v1_api.register(PerformanceResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', 'library.views.app_index', name='app'),
)
