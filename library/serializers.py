"""
Serialize models in the symphony library.
"""

from rest_framework import serializers, viewsets
from library.models import Artist, Piece, ScoreType, Container, Orchestra
from library.models import Performance


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    """ Serialize the Artist model """
    class Meta:
        model = Artist
        fields = ('first_name', 'last_name',)

# using the implicit model style is not as good as explicit, but we're just 
# getting the app up and running right now.
class ArtistViewSet(viewsets.ModelViewSet):
    model = Artist
class PieceViewSet(viewsets.ModelViewSet):
    model = Piece
class ScoreTypeViewSet(viewsets.ModelViewSet):
    model = ScoreType
class ContainerViewSet(viewsets.ModelViewSet):
    model = Container
class OrchestraViewSet(viewsets.ModelViewSet):
    model = Orchestra
class PerformanceViewSet(viewsets.ModelViewSet):
    model = Performance
