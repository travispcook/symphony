# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        Piece = orm.Piece
        Container = orm.Container
        CabinetGroup = orm.CabinetGroup
        Cabinet = orm.Cabinet
        Drawer = orm.Drawer

        group_containers = {}
        for cg in CabinetGroup.objects.all():
            group_containers[cg] = Container.objects.create(
                slug=cg.shortname, name=cg.description)

        cabinet_containers = {}
        for cab in Cabinet.objects.all():
            cabinet_containers[cab] = Container.objects.create(
                slug=cab.number, name="Cabinet {}".format(cab.number),
                number=cab.number, parent=group_containers[cab.group])

        drawer_containers = {}
        for drawer in Drawer.objects.all():
            drawer_containers[drawer] = Container.objects.create(
                slug=drawer.number,
                name="Drawer {}".format(drawer.number),
                number=drawer.number,
                parent=cabinet_containers[drawer.cabinet])

        for piece in Piece.objects.all():
            piece.container = drawer_containers[piece.drawer]
            piece.save()


    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'library.artist': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'library.cabinet': {
            'Meta': {'ordering': "['group', 'number']", 'object_name': 'Cabinet'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.CabinetGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'library.cabinetgroup': {
            'Meta': {'ordering': "['shortname']", 'object_name': 'CabinetGroup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        u'library.container': {
            'Meta': {'ordering': "('parent', 'number')", 'object_name': 'Container'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['library.Container']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32'})
        },
        u'library.drawer': {
            'Meta': {'ordering': "['cabinet', 'number']", 'object_name': 'Drawer'},
            'cabinet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Cabinet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'library.orchestra': {
            'Meta': {'ordering': "['shortname']", 'object_name': 'Orchestra'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'shortname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        u'library.performance': {
            'Meta': {'ordering': "['date']", 'object_name': 'Performance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orchestra': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['library.Orchestra']", 'symmetrical': 'False'}),
            'piece': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['library.Piece']", 'symmetrical': 'False'}),
            'place': ('django.db.models.fields.TextField', [], {'max_length': '1024'})
        },
        u'library.piece': {
            'Meta': {'ordering': "['title']", 'object_name': 'Piece'},
            'arranger': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pieces_arranged'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['library.Artist']"}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'composer': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pieces_composed'", 'symmetrical': 'False', 'to': u"orm['library.Artist']"}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Container']"}),
            'difficulty': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'drawer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.Drawer']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['library.ScoreType']", 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'library.scoretype': {
            'Meta': {'object_name': 'ScoreType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['library']
    symmetrical = True
