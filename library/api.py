from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie import fields

from library.models import (Piece, Composer, Arranger, CabinetGroup, Cabinet,
    Drawer, ScoreType, Orchestra, Performance)


class PieceResource(ModelResource):
    # Relationship fields
    composers = fields.ToManyField('library.api.ComposerResource', 'composer')
    drawer = fields.ToOneField('library.api.DrawerResource', 'drawer')
    cabinet = fields.ToOneField('library.api.CabinetResource', 'cabinet',
                                readonly=True)
    cabinetgroup = fields.ToOneField('library.api.CabinetGroupResource',
                                     'group', readonly=True)
    scoretype = fields.ToOneField('library.api.ScoreTypeResource', 'score')
    
    # Custom fields
    drawer_number = fields.IntegerField(readonly=True)
    cabinet_number = fields.IntegerField(readonly=True)
    group = fields.CharField(readonly=True)
    location = fields.CharField(readonly=True)
    score = fields.CharField(readonly=True)

    def dehydrate_drawer_number(self, bundle):
        return bundle.obj.drawer.number

    def dehydrate_cabinet_number(self, bundle):
        return bundle.obj.cabinet.number

    def dehydrate_group(self, bundle):
        return bundle.obj.group.shortname

    def dehydrate_location(self, bundle):
        return str(bundle.obj.drawer)

    def dehydrate_score(self, bundle):
        return bundle.obj.scoretype

    class Meta:
        queryset = Piece.objects.all()
        # TODO set real authorization.
        authorization = Authorization()
        filtering = {
            'title': ALL,
            'subtitle': ALL,
            'difficulty': ('exact', 'in'),
            'composers': ALL_WITH_RELATIONS,
            'arrangers': ALL_WITH_RELATIONS,
            'drawer__cabinet': ('exact', 'in'),
            'drawer': ('exact', 'in'),
            'score': ('exact', 'in'),
        }


class ComposerResource(ModelResource):
    pieces = fields.ToManyField('library.api.PieceResource', 'piece_set')

    class Meta:
        queryset = Composer.objects.all()
        # TODO set real authorization.
        authorization = Authorization()
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
        }


class ArrangerResource(ModelResource):
    pieces = fields.ToManyField('library.api.PieceResource', 'piece_set')

    class Meta:
        queryset = Arranger.objects.all()
        # TODO set real authorization.
        authorization = Authorization()
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
        }


class CabinetGroupResource(ModelResource):
    cabinets = fields.ToManyField('library.api.CabinetResource', 'cabinets')
    drawers = fields.ToManyField('library.api.DrawerResource', 'drawers')

    # Custom fields
    location = fields.CharField(readonly=True)
    total_pieces = fields.IntegerField(attribute='total_pieces', readonly=True)
    
    def dehydrate_location(self, bundle):
        return str(bundle.obj)

    class Meta:
        queryset = CabinetGroup.objects.all()
        # TODO set real authorization.
        authorization = Authorization()


class CabinetResource(ModelResource):
    cabinetgroup = fields.ToOneField('library.api.CabinetGroupResource',
                                     'group')
    drawers = fields.ToManyField('library.api.DrawerResource', 'drawers',
                                 full=True)

    # Custom fields
    group = fields.CharField(readonly=True)
    location = fields.CharField(readonly=True)
    total_pieces = fields.IntegerField(attribute='total_pieces', readonly=True)
    
    def dehydrate_group(self, bundle):
        return bundle.obj.group.shortname

    def dehydrate_location(self, bundle):
        return str(bundle.obj)

    class Meta:
        queryset = Cabinet.objects.all()
        # TODO set real authorization.
        authorization = Authorization()
        filtering = {
            'cabinetgroup': ('exact', 'in'),
        }


class DrawerResource(ModelResource):
    cabinetgroup = fields.ToOneField('library.api.CabinetGroupResource',
                                     'group')
    cabinet = fields.ToOneField('library.api.CabinetResource', 'cabinet')
    pieces = fields.ToManyField('library.api.PieceResource', 'piece_set')

    # Custom fields
    cabinet_number = fields.IntegerField(readonly=True)
    group = fields.CharField(readonly=True)
    location = fields.CharField(readonly=True)
    total_pieces = fields.IntegerField(attribute='total_pieces', readonly=True)
    
    def dehydrate_cabinet_number(self, bundle):
        return bundle.obj.cabinet.number

    def dehydrate_group(self, bundle):
        return bundle.obj.group.shortname

    def dehydrate_location(self, bundle):
        return str(bundle.obj)

    class Meta:
        queryset = Drawer.objects.all()
        # TODO set real authorization.
        authorization = Authorization()
        filtering = {
            'cabinetgroup': ('exact', 'in'),
            'cabinet': ('exact', 'in'),
        }


class ScoreTypeResource(ModelResource):
    pieces = fields.ToManyField('library.api.PieceResource', 'piece_set')

    class Meta:
        queryset = ScoreType.objects.all()
        # TODO set real authorization.
        authorization = Authorization()


class OrchestraResource(ModelResource):
    performances = fields.ToManyField('library.api.PerformanceResource', 
                                      'performance_set')
    class Meta:
        queryset = Orchestra.objects.all()
        # TODO set real authorization.
        authorization = Authorization()


class PerformanceResource(ModelResource):
    pieces = fields.ToManyField('library.api.PieceResource', 'piece')

    class Meta:
        queryset = Performance.objects.all()
        # TODO set real authorization.
        authorization = Authorization()
        filtering = {
            'date': ('lt', 'lte', 'range', 'gte', 'gt'),
        }
