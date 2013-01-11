from tastypie.resources import ModelResource
from library.models import (Piece, Composer, Arranger, CabinetGroup, Cabinet,
    Drawer, ScoreType, Orchestra, Performance)


class PieceResource(ModelResource):
    class Meta:
        queryset = Piece.objects.all()
        resource_name = 'piece'


class ComposerResource(ModelResource):
    class Meta:
        queryset = Composer.objects.all()
        resource_name = 'composer'


class ArrangerResource(ModelResource):
    class Meta:
        queryset = Arranger.objects.all()
        resource_name = 'arranger'


class CabinetResource(ModelResource):
    class Meta:
        queryset = Cabinet.objects.all()
        resource_name = 'cabinet'


class CabinetGroupResource(ModelResource):
    class Meta:
        queryset = CabinetGroup.objects.all()
        resource_name = 'cabinetgroup'


class DrawerResource(ModelResource):
    class Meta:
        queryset = Drawer.objects.all()
        resource_name = 'drawer'


class ScoreTypeResource(ModelResource):
    class Meta:
        queryset = ScoreType.objects.all()
        resource_name = 'scoretype'


class OrchestraResource(ModelResource):
    class Meta:
        queryset = Orchestra.objects.all()
        resource_name = 'orchestra'


class ScoreTypeResource(ModelResource):
    class Meta:
        queryset = ScoreType.objects.all()
        resource_name = 'scoretype'
