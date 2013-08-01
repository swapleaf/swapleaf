# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('main_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('main', ['UserProfile'])

        # Adding model 'Institution'
        db.create_table('main_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('main', ['Institution'])

        # Adding M2M table for field student on 'Institution'
        db.create_table('main_institution_student', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('institution', models.ForeignKey(orm['main.institution'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('main_institution_student', ['institution_id', 'user_id'])

        # Adding model 'Book'
        db.create_table('main_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('isbn', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0.0, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cover_image', self.gf('django.db.models.fields.files.ImageField')(default='default/img/book_cover_default.jpg', max_length=100, blank=True)),
        ))
        db.send_create_signal('main', ['Book'])

        # Adding model 'BookSelling'
        db.create_table('main_bookselling', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seller', to=orm['auth.User'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='buyer', null=True, to=orm['auth.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Book'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 5, 0, 0))),
        ))
        db.send_create_signal('main', ['BookSelling'])

        # Adding model 'BookTrading'
        db.create_table('main_booktrading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trader1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trader1', to=orm['auth.User'])),
            ('book_trader1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='book_trader1', to=orm['main.Book'])),
            ('price_book1', self.gf('django.db.models.fields.IntegerField')()),
            ('trader2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='trader2', null=True, to=orm['auth.User'])),
            ('book_trader2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='book_trader2', null=True, to=orm['main.Book'])),
            ('price_book2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 5, 0, 0))),
        ))
        db.send_create_signal('main', ['BookTrading'])

        # Adding model 'BookGiving'
        db.create_table('main_bookgiving', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('giver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='giver', to=orm['auth.User'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='receiver', null=True, to=orm['auth.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Book'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 5, 0, 0))),
        ))
        db.send_create_signal('main', ['BookGiving'])

        # Adding model 'Course'
        db.create_table('main_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crn', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('course_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['Course'])

        # Adding M2M table for field book on 'Course'
        db.create_table('main_course_book', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['main.course'], null=False)),
            ('book', models.ForeignKey(orm['main.book'], null=False))
        ))
        db.create_unique('main_course_book', ['course_id', 'book_id'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('main_userprofile')

        # Deleting model 'Institution'
        db.delete_table('main_institution')

        # Removing M2M table for field student on 'Institution'
        db.delete_table('main_institution_student')

        # Deleting model 'Book'
        db.delete_table('main_book')

        # Deleting model 'BookSelling'
        db.delete_table('main_bookselling')

        # Deleting model 'BookTrading'
        db.delete_table('main_booktrading')

        # Deleting model 'BookGiving'
        db.delete_table('main_bookgiving')

        # Deleting model 'Course'
        db.delete_table('main_course')

        # Removing M2M table for field book on 'Course'
        db.delete_table('main_course_book')


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
            'isbn': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'main.bookgiving': {
            'Meta': {'object_name': 'BookGiving'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Book']"}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'giver'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'receiver'", 'null': 'True', 'to': "orm['auth.User']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'})
        },
        'main.bookselling': {
            'Meta': {'object_name': 'BookSelling'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Book']"}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'buyer'", 'null': 'True', 'to': "orm['auth.User']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seller'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'})
        },
        'main.booktrading': {
            'Meta': {'object_name': 'BookTrading'},
            'book_trader1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'book_trader1'", 'to': "orm['main.Book']"}),
            'book_trader2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'book_trader2'", 'null': 'True', 'to': "orm['main.Book']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_book1': ('django.db.models.fields.IntegerField', [], {}),
            'price_book2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 5, 0, 0)'}),
            'trader1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trader1'", 'to': "orm['auth.User']"}),
            'trader2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'trader2'", 'null': 'True', 'to': "orm['auth.User']"})
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