"""
RESTful API for Library data.
"""

from django.core.exceptions import ValidationError
from rest_framework import serializers, viewsets, routers, filters

from library.models import (Artist, Piece, ScoreType, Container, Orchestra,
                            Performance)


class IntegerChoicesField(serializers.WritableField):
    """
    Write and read strings, but translate into integers internally.

    Accepts a choices tuple of ((int, string), ...) to use for translation.
    """

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(IntegerChoicesField, self).__init__(*args, **kwargs)
        self.string_to_integer = {v: k for (k, v) in choices}
        self.integer_to_string = {k: v for (k, v) in choices}
        self.string_to_integer[None] = None
        self.integer_to_string[None] = None

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


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist


class ContainerSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Container
        fields = ('id', 'slug', 'name', 'description', 'number', 'children')
ContainerSerializer.base_fields['children'] = ContainerSerializer(many=True)
ContainerSerializer.base_fields['children'] = ContainerSerializer(many=True)


class ParentContainerSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Container
        fields = ('id', 'slug', 'name', 'description', 'number', 'parent')
ParentContainerSerializer.base_fields['parent'] = ParentContainerSerializer()
ParentContainerSerializer.base_fields['parent'] = ParentContainerSerializer()


class PieceSerializer(serializers.ModelSerializer):
    difficulty = IntegerChoicesField(choices=Piece.DIFFICULTY_CHOICES)
    composers = ArtistSerializer(many=True)
    arrangers = ArtistSerializer(many=True)
    path = serializers.CharField(read_only=True)
    container = ParentContainerSerializer()
    score = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Piece


class PieceViewSet(viewsets.ModelViewSet):
    """
    List of all pieces, with search and filtering. Including composers,
    arrangers, and containers nested.
    """
    paginate_by = None
    model = Piece
    serializer_class = PieceSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'subtitle', 'comment')

    def metadata(self, request):
        data = super(PieceViewSet, self).metadata(request)
        data['actions']['POST']['difficulty']['choices'] = \
            dict(Piece.DIFFICULTY_CHOICES)

        data['actions']['GET'] = {'search': 'string'}
        return data


class ScoreTypeViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = ScoreType


class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer
    paginate_by = None
    model = Container

    def get_queryset(self):
        is_list = getattr(self.request, 'list', False)
        if is_list:
            return Container.objects.filter(parent__isnull=True)
        return Container.objects.all()

    def list(self, request):
        request.list = True
        return super(ContainerViewSet, self).list(request)


class OrchestraViewSet(viewsets.ModelViewSet):
    paginate_by = None
    model = Orchestra


class OrchestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orchestra
        fields = ['name', 'id']


class PerformancePieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['title', 'id']


class PerformanceSerializer(serializers.ModelSerializer):
    orchestras = OrchestraSerializer(many=True)
    pieces = PerformancePieceSerializer(many=True)

    class Meta:
        model = Performance
        fields = ('place', 'date', 'orchestras', 'pieces', 'comments')


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    Records of songs' performances by orchestra.
    """
    paginate_by = None
    model = Performance
    serializer_class = PerformanceSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('place', 'comments')

    def metadata(self, request):
        data = super(PerformanceViewSet, self).metadata(request)
        data['actions']['GET'] = {'search': 'string'}
        return data


router = routers.DefaultRouter()

router.register(r'piece', PieceViewSet)
router.register(r'scoretype', ScoreTypeViewSet)
router.register(r'container', ContainerViewSet)
router.register(r'orchestra', OrchestraViewSet)
router.register(r'performance', PerformanceViewSet)
