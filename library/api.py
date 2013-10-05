"""
RESTful API for Library data.
"""

from django.core.exceptions import ValidationError
from rest_framework import serializers, viewsets, routers

from library.models import (Artist, Piece, ScoreType, Container, Orchestra,
                            Performance)


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    """ Serialize the Artist model """
    class Meta:
        model = Artist
        fields = ('first_name', 'last_name',)


class IntegerChoicesField(serializers.WritableField):
    """
    Write and read strings, but translate into integers internally.

    Accepts a choices tuple of ((int, string), ...) to use for translation.
    """

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        self.string_to_integer = {v: k for (k, v) in choices}
        self.integer_to_string = {k: v for (k, v) in choices}
        super(IntegerChoicesField, self).__init__(*args, **kwargs)

    def to_native(self, value):
        """Python -> JSON"""
        integer = super(IntegerChoicesField, self).to_native(value)
        try:
            return self.integer_to_string[integer]
        except KeyError:
            raise ValidationError(
                "No key '{}' in "
                "IntegerChoicesField.integer_to_string({})".format(
                    integer, self.integer_to_string)
            )

    def from_native(self, value):
        string = super(IntegerChoicesField, self).from_native(value)
        try:
            return self.string_to_integer[string]
        except KeyError:
            raise ValidationError(
                "No key '{}' in "
                "IntegerChoicesField.string_to_integer({})".format(
                    string, self.string_to_integer)
            )


class PieceSerializer(serializers.ModelSerializer):
    difficulty = IntegerChoicesField(choices=Piece.DIFFICULTY_CHOICES)

    class Meta:
        model = Piece


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


router = routers.DefaultRouter()

router.register(r'artist', ArtistViewSet)
router.register(r'piece', PieceViewSet)
router.register(r'scoretype', ScoreTypeViewSet)
router.register(r'container', ContainerViewSet)
router.register(r'orchestra', OrchestraViewSet)
router.register(r'performance', PerformanceViewSet)
