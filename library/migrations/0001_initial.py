# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Composer'
        db.create_table(u'library_composer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'library', ['Composer'])

        # Adding model 'Arranger'
        db.create_table(u'library_arranger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'library', ['Arranger'])

        # Adding model 'Piece'
        db.create_table(u'library_piece', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('drawer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Drawer'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.ScoreType'], null=True, blank=True)),
            ('difficulty', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'library', ['Piece'])

        # Adding M2M table for field composer on 'Piece'
        db.create_table(u'library_piece_composer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm[u'library.piece'], null=False)),
            ('composer', models.ForeignKey(orm[u'library.composer'], null=False))
        ))
        db.create_unique(u'library_piece_composer', ['piece_id', 'composer_id'])

        # Adding M2M table for field arranger on 'Piece'
        db.create_table(u'library_piece_arranger', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm[u'library.piece'], null=False)),
            ('arranger', models.ForeignKey(orm[u'library.arranger'], null=False))
        ))
        db.create_unique(u'library_piece_arranger', ['piece_id', 'arranger_id'])

        # Adding model 'ScoreType'
        db.create_table(u'library_scoretype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal(u'library', ['ScoreType'])

        # Adding model 'CabinetGroup'
        db.create_table(u'library_cabinetgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shortname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal(u'library', ['CabinetGroup'])

        # Adding model 'Cabinet'
        db.create_table(u'library_cabinet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.CabinetGroup'])),
        ))
        db.send_create_signal(u'library', ['Cabinet'])

        # Adding model 'Drawer'
        db.create_table(u'library_drawer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cabinet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Cabinet'])),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'library', ['Drawer'])

        # Adding model 'Orchestra'
        db.create_table(u'library_orchestra', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shortname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'library', ['Orchestra'])

        # Adding model 'Performance'
        db.create_table(u'library_performance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.TextField')(max_length=1024)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'library', ['Performance'])

        # Adding M2M table for field orchestra on 'Performance'
        db.create_table(u'library_performance_orchestra', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('performance', models.ForeignKey(orm[u'library.performance'], null=False)),
            ('orchestra', models.ForeignKey(orm[u'library.orchestra'], null=False))
        ))
        db.create_unique(u'library_performance_orchestra', ['performance_id', 'orchestra_id'])

        # Adding M2M table for field piece on 'Performance'
        db.create_table(u'library_performance_piece', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('performance', models.ForeignKey(orm[u'library.performance'], null=False)),
            ('piece', models.ForeignKey(orm[u'library.piece'], null=False))
        ))
        db.create_unique(u'library_performance_piece', ['performance_id', 'piece_id'])


    def backwards(self, orm):
        # Deleting model 'Composer'
        db.delete_table(u'library_composer')

        # Deleting model 'Arranger'
        db.delete_table(u'library_arranger')

        # Deleting model 'Piece'
        db.delete_table(u'library_piece')

        # Removing M2M table for field composer on 'Piece'
        db.delete_table('library_piece_composer')

        # Removing M2M table for field arranger on 'Piece'
        db.delete_table('library_piece_arranger')

        # Deleting model 'ScoreType'
        db.delete_table(u'library_scoretype')

        # Deleting model 'CabinetGroup'
        db.delete_table(u'library_cabinetgroup')

        # Deleting model 'Cabinet'
        db.delete_table(u'library_cabinet')

        # Deleting model 'Drawer'
        db.delete_table(u'library_drawer')

        # Deleting model 'Orchestra'
        db.delete_table(u'library_orchestra')

        # Deleting model 'Performance'
        db.delete_table(u'library_performance')

        # Removing M2M table for field orchestra on 'Performance'
        db.delete_table('library_performance_orchestra')

        # Removing M2M table for field piece on 'Performance'
        db.delete_table('library_performance_piece')


    models = {
        u'library.arranger': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Arranger'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
        u'library.composer': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Composer'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
            'arranger': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['library.Arranger']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'composer': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['library.Composer']", 'symmetrical': 'False'}),
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