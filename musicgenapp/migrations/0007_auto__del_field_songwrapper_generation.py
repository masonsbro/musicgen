# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SongWrapper.generation'
        db.delete_column(u'musicgenapp_songwrapper', 'generation')


    def backwards(self, orm):
        # Adding field 'SongWrapper.generation'
        db.add_column(u'musicgenapp_songwrapper', 'generation',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    models = {
        u'musicgenapp.musicgenuser': {
            'Meta': {'object_name': 'MusicGenUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passwordHash': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'passwordSalt': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'resetCode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'musicgenapp.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['musicgenapp.Song']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['musicgenapp.MusicGenUser']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'musicgenapp.song': {
            'Meta': {'object_name': 'Song'},
            'avgRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'durations': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'generation': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'numRatings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pitches': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'wav': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'wrapper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['musicgenapp.SongWrapper']"})
        },
        u'musicgenapp.songwrapper': {
            'Meta': {'object_name': 'SongWrapper'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['musicgenapp.Song']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['musicgenapp']