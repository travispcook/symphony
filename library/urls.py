from django.conf.urls.defaults import *
from library.api import PieceResource

piece_resource = PieceResource()

urlpatterns = patterns('',
    url(r'^api/', include(piece_resource.urls)),
)
