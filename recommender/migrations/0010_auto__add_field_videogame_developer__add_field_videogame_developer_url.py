# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VideoGame.developer'
        db.add_column(u'recommender_videogame', 'developer',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.developer_url'
        db.add_column(u'recommender_videogame', 'developer_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.esrb_rating'
        db.add_column(u'recommender_videogame', 'esrb_rating',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.esrb_rating_description'
        db.add_column(u'recommender_videogame', 'esrb_rating_description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.genre'
        db.add_column(u'recommender_videogame', 'genre',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.ign_community_rating'
        db.add_column(u'recommender_videogame', 'ign_community_rating',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.ign_community_rating_count'
        db.add_column(u'recommender_videogame', 'ign_community_rating_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.ign_image'
        db.add_column(u'recommender_videogame', 'ign_image',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.ign_rating'
        db.add_column(u'recommender_videogame', 'ign_rating',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.ign_subheadline'
        db.add_column(u'recommender_videogame', 'ign_subheadline',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.ign_wiki_edits'
        db.add_column(u'recommender_videogame', 'ign_wiki_edits',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.publisher'
        db.add_column(u'recommender_videogame', 'publisher',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.publisher_url'
        db.add_column(u'recommender_videogame', 'publisher_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.release_date'
        db.add_column(u'recommender_videogame', 'release_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.summary'
        db.add_column(u'recommender_videogame', 'summary',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VideoGame.developer'
        db.delete_column(u'recommender_videogame', 'developer')

        # Deleting field 'VideoGame.developer_url'
        db.delete_column(u'recommender_videogame', 'developer_url')

        # Deleting field 'VideoGame.esrb_rating'
        db.delete_column(u'recommender_videogame', 'esrb_rating')

        # Deleting field 'VideoGame.esrb_rating_description'
        db.delete_column(u'recommender_videogame', 'esrb_rating_description')

        # Deleting field 'VideoGame.genre'
        db.delete_column(u'recommender_videogame', 'genre')

        # Deleting field 'VideoGame.ign_community_rating'
        db.delete_column(u'recommender_videogame', 'ign_community_rating')

        # Deleting field 'VideoGame.ign_community_rating_count'
        db.delete_column(u'recommender_videogame', 'ign_community_rating_count')

        # Deleting field 'VideoGame.ign_image'
        db.delete_column(u'recommender_videogame', 'ign_image')

        # Deleting field 'VideoGame.ign_rating'
        db.delete_column(u'recommender_videogame', 'ign_rating')

        # Deleting field 'VideoGame.ign_subheadline'
        db.delete_column(u'recommender_videogame', 'ign_subheadline')

        # Deleting field 'VideoGame.ign_wiki_edits'
        db.delete_column(u'recommender_videogame', 'ign_wiki_edits')

        # Deleting field 'VideoGame.publisher'
        db.delete_column(u'recommender_videogame', 'publisher')

        # Deleting field 'VideoGame.publisher_url'
        db.delete_column(u'recommender_videogame', 'publisher_url')

        # Deleting field 'VideoGame.release_date'
        db.delete_column(u'recommender_videogame', 'release_date')

        # Deleting field 'VideoGame.summary'
        db.delete_column(u'recommender_videogame', 'summary')


    models = {
        u'attributes.attributeoption': {
            'Meta': {'object_name': 'AttributeOption'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'error_message': ('django.db.models.fields.CharField', [], {'default': "u'Invalid Entry'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'validation': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'recommender.review': {
            'Meta': {'object_name': 'Review'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'video_game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.VideoGame']"})
        },
        u'recommender.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'recommender.videogame': {
            'Meta': {'ordering': "('name',)", 'object_name': 'VideoGame'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'developer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'developer_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'esrb_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'esrb_rating_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ign_community_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'ign_community_rating_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ign_image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ign_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'ign_subheadline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ign_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'ign_wiki_edits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publisher_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'recommender.videogameattribute': {
            'Meta': {'ordering': "('option__sort_order',)", 'object_name': 'VideoGameAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['attributes.AttributeOption']"}),
            'value': ('django.db.models.fields.TextField', [], {}),
            'video_game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.VideoGame']"})
        }
    }

    complete_apps = ['recommender']