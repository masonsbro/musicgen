# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MusicGenUser.resetCode'
        db.add_column(u'musicgenapp_musicgenuser', 'resetCode',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MusicGenUser.resetCode'
        db.delete_column(u'musicgenapp_musicgenuser', 'resetCode')


    models = {
        u'musicgenapp.musicgenuser': {
            'Meta': {'object_name': 'MusicGenUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwordHash': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'passwordSalt': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'resetCode': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['musicgenapp']