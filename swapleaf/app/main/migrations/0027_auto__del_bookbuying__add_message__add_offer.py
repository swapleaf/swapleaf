# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BookBuying'
        db.delete_table('main_bookbuying')

        # Adding model 'Message'
        db.create_table('main_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_send', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_send', to=orm['auth.User'])),
            ('user_receive', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_receive', to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 22, 0, 0))),
            ('elapse_time', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Message'])

        # Adding model 'Offer'
        db.create_table('main_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user1', to=orm['auth.User'])),
            ('user2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user2', to=orm['auth.User'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('offer_type', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('offer_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 22, 0, 0))),
        ))
        db.send_create_signal('main', ['Offer'])

        # Adding M2M table for field message on 'Offer'
        db.create_table('main_offer_message', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['main.offer'], null=False)),
            ('message', models.ForeignKey(orm['main.message'], null=False))
        ))
        db.create_unique('main_offer_message', ['offer_id', 'message_id'])

        # Adding M2M table for field offer on 'BookTransaction'
        db.create_table('main_booktransaction_offer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('booktransaction', models.ForeignKey(orm['main.booktransaction'], null=False)),
            ('offer', models.ForeignKey(orm['main.offer'], null=False))
        ))
        db.create_unique('main_booktransaction_offer', ['booktransaction_id', 'offer_id'])


    def backwards(self, orm):
        # Adding model 'BookBuying'
        db.create_table('main_bookbuying', (
            ('transaction_partner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transaction_partner', null=True, to=orm['auth.User'], blank=True)),
            ('post_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 22, 0, 0))),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2)),
            ('transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='book_buyer', null=True, to=orm['auth.User'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Book'])),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
        ))
        db.send_create_signal('main', ['BookBuying'])

        # Deleting model 'Message'
        db.delete_table('main_message')

        # Deleting model 'Offer'
        db.delete_table('main_offer')

        # Removing M2M table for field message on 'Offer'
        db.delete_table('main_offer_message')

        # Removing M2M table for field offer on 'BookTransaction'
        db.delete_table('main_booktransaction_offer')


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
            'offer': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Offer']", 'symmetrical': 'False'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 22, 0, 0)'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seller'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '10'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'main.course': {
            'Meta': {'object_name': 'Course'},
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
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'symmetrical': 'False'})
        },
        'main.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 22, 0, 0)'}),
            'elapse_time': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_receive': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_receive'", 'to': "orm['auth.User']"}),
            'user_send': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_send'", 'to': "orm['auth.User']"})
        },
        'main.notify': {
            'Meta': {'ordering': "['date']", 'object_name': 'Notify'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 22, 0, 0)'}),
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
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'message'", 'null': 'True', 'to': "orm['main.Message']"}),
            'offer_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 22, 0, 0)'}),
            'offer_type': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user1'", 'to': "orm['auth.User']"}),
            'user2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user2'", 'to': "orm['auth.User']"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner_status': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['main']