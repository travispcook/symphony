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
    paginate_by = None
    model = Artist
class PieceViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = Piece
class ScoreTypeViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = ScoreType
class ContainerViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = Container
class OrchestraViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = Orchestra
class PerformanceViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = Performance
