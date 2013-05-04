"""
Rest interface 
"""
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from library.serializers import ArtistSerializer
from library.models import Artist



@api_view(['GET'])
def api_root(request, format=None):
    """
    Entry endpoint of the API
    """
    return Response({
       'artists': reverse('artist-list', request=request),
       })


class ArtistList(generics.ListCreateAPIView):
    """
    API endpoint for a list of artists
    """
    model = Artist
    serializer_class = ArtistSerializer


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for a single artist
    """
    model = Artist
    serializer_class = ArtistSerializer
