"""
Serialize models in the symphony library.
"""

from rest_framework import serializers
from library.models import Artist


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    """
    serialize out the list of artists in the library
    """
    class Meta:
        model = Artist
        fields = ('first_name', 'last_name',)
