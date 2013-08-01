# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BookBuying'
        db.create_table('main_bookbuying', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Book'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='book_buyer', null=True, to=orm['auth.User'])),
            ('transaction_partner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='transaction_partner', null=True, to=orm['auth.User'])),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('post_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 5, 0, 0))),
        ))
        db.send_create_signal('main', ['BookBuying'])


        # Changing field 'BookGiving.transaction_time'
        db.alter_column('main_bookgiving', 'transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'BookTrading.price_book1'
        db.alter_column('main_booktrading', 'price_book1', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'BookTrading.price_book2'
        db.alter_column('main_booktrading', 'price_book2', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'BookTrading.transaction_time'
        db.alter_column('main_booktrading', 'transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'BookSelling.price'
        db.alter_column('main_bookselling', 'price', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'BookSelling.transaction_time'
        db.alter_column('main_bookselling', 'transaction_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting model 'BookBuying'
        db.delete_table('main_bookbuying')


        # Changing field 'BookGiving.transaction_time'
        db.alter_column('main_bookgiving', 'transaction_time', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'BookTrading.price_book1'
        db.alter_column('main_booktrading', 'price_book1', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'BookTrading.price_book2'
        db.alter_column('main_booktrading', 'price_book2', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'BookTrading.transaction_time'
        db.alter_column('main_booktrading', 'transaction_time', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'BookSelling.price'
        db.alter_column('main_bookselling', 'price', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'BookSelling.transaction_time'
        db.alter_column('main_bookselling', 'transaction_time', self.gf('django.db.models.fields.DateTimeField')())

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
            'author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'cover_image': ('django.db.models.fields.files.ImageField', [], {'default': "'default/img/book_cover_default.jpg'", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'main.bookbuying': {
            'Meta': {'object_name': 'BookBuying'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Book']"}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'book_buyer'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'transaction_partner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transaction_partner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'main.bookgiving': {
            'Meta': {'object_name': 'BookGiving'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Book']"}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'giver'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'receiver'", 'null': 'True', 'to': "orm['auth.User']"}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.bookselling': {
            'Meta': {'object_name': 'BookSelling'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Book']"}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'buyer'", 'null': 'True', 'to': "orm['auth.User']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seller'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.booktrading': {
            'Meta': {'object_name': 'BookTrading'},
            'book_trader1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_trader1'", 'to': "orm['main.Book']"}),
            'book_trader2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'book_trader2'", 'null': 'True', 'to': "orm['main.Book']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'}),
            'price_book1': ('django.db.models.fields.FloatField', [], {}),
            'price_book2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'trader1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trader1'", 'to': "orm['auth.User']"}),
            'trader2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'trader2'", 'null': 'True', 'to': "orm['auth.User']"}),
            'transaction_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.course': {
            'Meta': {'object_name': 'Course'},
            'book': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'course_book'", 'null': 'True', 'to': "orm['main.Book']"}),
            'course_number': ('django.db.models.fields.IntegerField', [], {}),
            'crn': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.institution': {
            'Meta': {'object_name': 'Institution'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'symmetrical': 'False'})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['main']