# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ESRBRating'
        db.create_table(u'recommender_esrbrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'recommender', ['ESRBRating'])

        # Adding model 'Tick'
        db.create_table(u'recommender_tick', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'recommender', ['Tick'])

        # Adding model 'Company'
        db.create_table(u'recommender_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'recommender', ['Company'])

        # Adding field 'Specification.slug'
        db.add_column(u'recommender_specification', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'VideoGame.developer'
        db.delete_column(u'recommender_videogame', 'developer')

        # Deleting field 'VideoGame.developer_url'
        db.delete_column(u'recommender_videogame', 'developer_url')

        # Deleting field 'VideoGame.publisher_url'
        db.delete_column(u'recommender_videogame', 'publisher_url')

        # Deleting field 'VideoGame.esrb_rating_description'
        db.delete_column(u'recommender_videogame', 'esrb_rating_description')

        # Deleting field 'VideoGame.publisher'
        db.delete_column(u'recommender_videogame', 'publisher')

        # Adding M2M table for field publisher on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_publisher')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('company', models.ForeignKey(orm[u'recommender.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videogame_id', 'company_id'])

        # Adding M2M table for field developer on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_developer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('company', models.ForeignKey(orm[u'recommender.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videogame_id', 'company_id'])


        # Renaming column for 'VideoGame.esrb_rating' to match new field type.
        db.rename_column(u'recommender_videogame', 'esrb_rating', 'esrb_rating_id')
        # Changing field 'VideoGame.esrb_rating'
        db.alter_column(u'recommender_videogame', 'esrb_rating_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recommender.ESRBRating'], null=True))
        # Adding index on 'VideoGame', fields ['esrb_rating']
        db.create_index(u'recommender_videogame', ['esrb_rating_id'])


    def backwards(self, orm):
        # Removing index on 'VideoGame', fields ['esrb_rating']
        db.delete_index(u'recommender_videogame', ['esrb_rating_id'])

        # Deleting model 'ESRBRating'
        db.delete_table(u'recommender_esrbrating')

        # Deleting model 'Tick'
        db.delete_table(u'recommender_tick')

        # Deleting model 'Company'
        db.delete_table(u'recommender_company')

        # Deleting field 'Specification.slug'
        db.delete_column(u'recommender_specification', 'slug')

        # Adding field 'VideoGame.developer'
        db.add_column(u'recommender_videogame', 'developer',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.developer_url'
        db.add_column(u'recommender_videogame', 'developer_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.publisher_url'
        db.add_column(u'recommender_videogame', 'publisher_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.esrb_rating_description'
        db.add_column(u'recommender_videogame', 'esrb_rating_description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'VideoGame.publisher'
        db.add_column(u'recommender_videogame', 'publisher',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field publisher on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_publisher'))

        # Removing M2M table for field developer on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_developer'))


        # Renaming column for 'VideoGame.esrb_rating' to match new field type.
        db.rename_column(u'recommender_videogame', 'esrb_rating_id', 'esrb_rating')
        # Changing field 'VideoGame.esrb_rating'
        db.alter_column(u'recommender_videogame', 'esrb_rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=3))

    models = {
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
        u'recommender.company': {
            'Meta': {'object_name': 'Company'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'recommender.esrbrating': {
            'Meta': {'object_name': 'ESRBRating'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '3', 'blank': 'True'})
        },
        u'recommender.feature': {
            'Meta': {'object_name': 'Feature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        u'recommender.genre': {
            'Meta': {'object_name': 'Genre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'recommender.platform': {
            'Meta': {'object_name': 'Platform'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
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
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'recommender.tick': {
            'Meta': {'object_name': 'Tick'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'recommender.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'recommender.videogame': {
            'Meta': {'ordering': "('-name', '-ign_image', '-ign_rating')", 'object_name': 'VideoGame'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'developer': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'developer'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['recommender.Company']"}),
            'esrb_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.ESRBRating']", 'null': 'True', 'blank': 'True'}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['recommender.Feature']", 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.Genre']", 'null': 'True', 'blank': 'True'}),
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
            'publisher': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'publisher'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['recommender.Company']"}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'release_date_malformed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'specifications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['recommender.Specification']", 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['recommender']