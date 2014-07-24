# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MusicGenUser'
        db.create_table(u'musicgenapp_musicgenuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('passwordHash', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('passwordSalt', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'musicgenapp', ['MusicGenUser'])


    def backwards(self, orm):
        # Deleting model 'MusicGenUser'
        db.delete_table(u'musicgenapp_musicgenuser')


    models = {
        u'musicgenapp.musicgenuser': {
            'Meta': {'object_name': 'MusicGenUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwordHash': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'passwordSalt': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['musicgenapp']