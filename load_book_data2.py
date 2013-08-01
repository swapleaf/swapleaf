# Full path and name to your csv file
import os
ROOT_PATH = os.path.dirname(__file__)

filepath=os.path.join(ROOT_PATH, 'swapleaf/db/raw/list_isbn.txt')

# Full path to your django project directory
swapleaf_project = os.path.join(ROOT_PATH, 'swapleaf')
import sys,os
sys.path.append(swapleaf_project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from swapleaf.app.main.models import Book
from django.contrib.auth.models import User

f = open(filepath,"r")

import urllib2
import json

hash_isbn = {}

count = 0
for row in f:
	list_word = row.split()
	isbn = list_word[0]
	name = " ".join(list_word[1:])
	print name
	if isbn not in hash_isbn:
		hash_isbn[isbn] = True
		link = "http://openlibrary.org/api/books?bibkeys=ISBN:" + isbn + "&jscmd=details&format=json"
		data = urllib2.urlopen(link)
		a = data.read()
		json_data = json.loads(a)
		isbn_check = Book.objects.filter(isbn10=isbn)
		print isbn
		if len(isbn_check) == 0:
			book = Book()
			if len(json_data) != 0:
				book.title = json_data['ISBN:' + isbn]['details']['title']
				book.isbn10 = isbn
				if "isbn_13" in json_data['ISBN:' + isbn]['details']:
					book.isbn13 = json_data['ISBN:' + isbn]['details']['isbn_13'][0]
				else:
					if count <= 490:
						link2 = "http://isbndb.com/api/books.xml?access_key=2H3HPUXH&results=details&index1=isbn&value1=" + isbn
						data2 = urllib2.urlopen(link2)
						b = data2.read()
						isbn13_pos = a.find("isbn13")
						isbn13 = a[isbn13_pos+8:isbn13_pos+21]
						book.isbn13 = isbn13
						count += 1
				if "authors" in json_data['ISBN:' + isbn]['details']:
					for i in range(0,len(json_data['ISBN:' + isbn]['details']['authors'])):
						if i == 0:
							book.author = book.author + json_data['ISBN:' + isbn]['details']['authors'][i]['name']
						else:
							 book.author = book.author + ", " + json_data['ISBN:' + isbn]['details']['authors'][i]['name']
				else:
					if count <= 490:
						link2 = "http://isbndb.com/api/books.xml?access_key=2H3HPUXH&results=details&index1=isbn&value1=" + isbn
						data2 = urllib2.urlopen(link2)
						b = data2.read()
						dom = parseString(b)
						xmlTag = dom.getElementsByTagName("AuthorsText")
						xmlData= xmlTag.replace("AuthorsText",'').replace("AuthorsText",'')
						book.author = xmlData 
						count += 1
				if "revision" in json_data['ISBN:' + isbn]['details']:
					book.edition = json_data['ISBN:' + isbn]['details']['revision']	
			else:
				book.title = name
				book.isbn10 = isbn
				if count <= 490:
					link2 = "http://isbndb.com/api/books.xml?access_key=2H3HPUXH&results=details&index1=isbn&value1=" + isbn
					data2 = urllib2.urlopen(link2)
					b = data2.read()
					isbn13_pos = a.find("isbn13")
					isbn13 = a[isbn13_pos+8:isbn13_pos+21]
					book.isbn13 = isbn13
					dom = parseString(b)
					xmlTag = dom.getElementsByTagName("AuthorsText")
					xmlData= xmlTag.replace("AuthorsText",'').replace("AuthorsText",'')
					book.author = xmlData 
					count += 1
					print count
			book.save()


books = 

print "Load Book data successfully"

