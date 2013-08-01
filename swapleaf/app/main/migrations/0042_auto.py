# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field message on 'Offer'
        db.delete_table('main_offer_message')

        # Adding M2M table for field messages on 'Offer'
        db.create_table('main_offer_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['main.offer'], null=False)),
            ('message', models.ForeignKey(orm['main.message'], null=False))
        ))
        db.create_unique('main_offer_messages', ['offer_id', 'message_id'])


    def backwards(self, orm):
        # Adding M2M table for field message on 'Offer'
        db.create_table('main_offer_message', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['main.offer'], null=False)),
            ('message', models.ForeignKey(orm['main.message'], null=False))
        ))
        db.create_unique('main_offer_message', ['offer_id', 'message_id'])

        # Removing M2M table for field messages on 'Offer'
        db.delete_table('main_offer_messages')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'edition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn10': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'isbn13': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '600'})
        },
        'main.booktransaction': {
            'Meta': {'object_name': 'BookTransaction'},
            'alert_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Book']"}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'buyer'", 'null': 'True', 'to': "orm['auth.User']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Course']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Offer']", 'null': 'True', 'symmetrical': 'False'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 28, 0, 0)'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seller'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '10'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'main.course': {
            'Meta': {'object_name': 'Course'},
            'course_book': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'course_book'", 'null': 'True', 'to': "orm['main.Book']"}),
            'course_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Institution']"})
        },
        'main.institution': {
            'Meta': {'object_name': 'Institution'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'main.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 28, 0, 0)'}),
            'elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['auth.User']"})
        },
        'main.notify': {
            'Meta': {'ordering': "['date']", 'object_name': 'Notify'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 28, 0, 0)'}),
            'elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_from'", 'to': "orm['auth.User']"}),
            'notify_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_to'", 'to': "orm['auth.User']"}),
            'notify_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '3'})
        },
        'main.offer': {
            'Meta': {'object_name': 'Offer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_message'", 'null': 'True', 'to': "orm['main.Message']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'message'", 'null': 'True', 'to': "orm['main.Message']"}),
            'offer_status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'offer_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 28, 0, 0)'}),
            'offer_type': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_offer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_offer'", 'to': "orm['auth.User']"}),
            'user_receive': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_receive'", 'to': "orm['auth.User']"}),
            'view_status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '3'})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner_status': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Institution']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['main']