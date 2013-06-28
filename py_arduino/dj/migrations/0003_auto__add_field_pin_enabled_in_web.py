# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Pin.enabled_in_web'
        db.add_column(u'dj_pin', 'enabled_in_web',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Pin.enabled_in_web'
        db.delete_column(u'dj_pin', 'enabled_in_web')


    models = {
        u'dj.pin': {
            'Meta': {'unique_together': "(('pin', 'digital'),)", 'object_name': 'Pin'},
            'digital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled_in_web': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pin': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pin_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['dj']