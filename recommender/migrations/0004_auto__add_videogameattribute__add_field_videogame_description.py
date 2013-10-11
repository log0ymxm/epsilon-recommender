# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoGameAttribute'
        db.create_table(u'recommender_videogameattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video_game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recommender.VideoGame'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attributes.AttributeOption'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'recommender', ['VideoGameAttribute'])

        # Adding field 'VideoGame.description'
        db.add_column(u'recommender_videogame', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Removing M2M table for field attributes on 'VideoGame'
        db.delete_table(db.shorten_name(u'recommender_videogame_attributes'))


    def backwards(self, orm):
        # Deleting model 'VideoGameAttribute'
        db.delete_table(u'recommender_videogameattribute')

        # Deleting field 'VideoGame.description'
        db.delete_column(u'recommender_videogame', 'description')

        # Adding M2M table for field attributes on 'VideoGame'
        m2m_table_name = db.shorten_name(u'recommender_videogame_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('videogame', models.ForeignKey(orm[u'recommender.videogame'], null=False)),
            ('attributeoption', models.ForeignKey(orm[u'attributes.attributeoption'], null=False))
        ))
        db.create_unique(m2m_table_name, ['videogame_id', 'attributeoption_id'])


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'recommender.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'recommender.review': {
            'Meta': {'object_name': 'Review'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.CustomUser']"}),
            'video_game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.VideoGame']"})
        },
        u'recommender.videogame': {
            'Meta': {'object_name': 'VideoGame'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'recommender.videogameattribute': {
            'Meta': {'ordering': "('option__sort_order',)", 'object_name': 'VideoGameAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['attributes.AttributeOption']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'video_game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommender.VideoGame']"})
        }
    }

    complete_apps = ['recommender']