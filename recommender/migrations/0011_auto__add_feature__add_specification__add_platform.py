# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feature'
        db.create_table(u'recommender_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'recommender', ['Feature'])

        # Adding model 'Specification'
        db.create_table(u'recommender_specification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'recommender', ['Specification'])

        # Adding model 'Platform'
        db.create_table(u'recommender_platform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'recommender', ['Platform'])

        # Adding M2M table for field features on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('feature', models.ForeignKey(orm[u'recommender.feature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videogame_id', 'feature_id'])

        # Adding M2M table for field ign_games_you_may_like on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_ign_games_you_may_like')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('to_videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_videogame_id', 'to_videogame_id'])

        # Adding M2M table for field platforms on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_platforms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('platform', models.ForeignKey(orm[u'recommender.platform'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videogame_id', 'platform_id'])

        # Adding M2M table for field specifications on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_specifications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('specification', models.ForeignKey(orm[u'recommender.specification'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videogame_id', 'specification_id'])


    def backwards(self, orm):
        # Deleting model 'Feature'
        db.delete_table(u'recommender_feature')

        # Deleting model 'Specification'
        db.delete_table(u'recommender_specification')

        # Deleting model 'Platform'
        db.delete_table(u'recommender_platform')

        # Removing M2M table for field features on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_features'))

        # Removing M2M table for field ign_games_you_may_like on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_ign_games_you_may_like'))

        # Removing M2M table for field platforms on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_platforms'))

        # Removing M2M table for field specifications on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_specifications'))


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
        u'recommender.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'recommender.platform': {
            'Meta': {'object_name': 'Platform'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'recommender.specification': {
            'Meta': {'object_name': 'Specification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['recommender.Feature']", 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ign_community_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'ign_community_rating_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ign_games_you_may_like': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ign_games_you_may_like_rel_+'", 'null': 'True', 'to': u"orm['recommender.VideoGame']"}),
            'ign_image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ign_rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'}),
            'ign_subheadline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ign_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'ign_wiki_edits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['recommender.Platform']", 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publisher_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'specifications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['recommender.Specification']", 'null': 'True', 'blank': 'True'}),
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