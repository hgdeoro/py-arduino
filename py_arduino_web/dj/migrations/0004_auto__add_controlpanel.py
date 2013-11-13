# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ControlPanel'
        db.create_table(u'dj_controlpanel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'dj', ['ControlPanel'])


    def backwards(self, orm):
        # Deleting model 'ControlPanel'
        db.delete_table(u'dj_controlpanel')


    models = {
        u'dj.controlpanel': {
            'Meta': {'object_name': 'ControlPanel'},
            'code': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'dj.pin': {
            'Meta': {'unique_together': "(('pin', 'digital'),)", 'object_name': 'Pin'},
            'digital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled_in_web': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pin': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pin_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dj']