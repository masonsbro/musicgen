# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rating'
        db.create_table(u'musicgenapp_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['musicgenapp.Song'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['musicgenapp.MusicGenUser'])),
            ('generation', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'musicgenapp', ['Rating'])

        # Adding model 'SongWrapper'
        db.create_table(u'musicgenapp_songwrapper', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('latest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['musicgenapp.Song'], null=True, blank=True)),
            ('generation', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'musicgenapp', ['SongWrapper'])

        # Adding model 'Song'
        db.create_table(u'musicgenapp_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pitches', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('durations', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('generation', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('numRatings', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avgRating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('wrapper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['musicgenapp.SongWrapper'])),
            ('latest', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wav', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'musicgenapp', ['Song'])


    def backwards(self, orm):
        # Deleting model 'Rating'
        db.delete_table(u'musicgenapp_rating')

        # Deleting model 'SongWrapper'
        db.delete_table(u'musicgenapp_songwrapper')

        # Deleting model 'Song'
        db.delete_table(u'musicgenapp_song')


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
            'generation': ('django.db.models.fields.IntegerField', [], {}),
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
            'generation': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['musicgenapp.Song']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['musicgenapp']