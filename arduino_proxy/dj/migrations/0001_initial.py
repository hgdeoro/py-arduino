# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pin'
        db.create_table(u'dj_pin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pin', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('digital', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'dj', ['Pin'])

        # Adding unique constraint on 'Pin', fields ['pin', 'digital']
        db.create_unique(u'dj_pin', ['pin', 'digital'])


    def backwards(self, orm):
        # Removing unique constraint on 'Pin', fields ['pin', 'digital']
        db.delete_unique(u'dj_pin', ['pin', 'digital'])

        # Deleting model 'Pin'
        db.delete_table(u'dj_pin')


    models = {
        u'dj.pin': {
            'Meta': {'unique_together': "(('pin', 'digital'),)", 'object_name': 'Pin'},
            'digital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pin': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['dj']