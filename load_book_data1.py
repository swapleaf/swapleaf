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

# import csv
# dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

f = open(filepath,"r")

import urllib2
import json

hash_isbn = {}

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
				if "authors" in json_data['ISBN:' + isbn]['details']:
					for i in range(0,len(json_data['ISBN:' + isbn]['details']['authors'])):
						if i == 0:
							book.author = book.author + json_data['ISBN:' + isbn]['details']['authors'][i]['name']
						else:
							 book.author = book.author + ", " + json_data['ISBN:' + isbn]['details']['authors'][i]['name']
				if "revision" in json_data['ISBN:' + isbn]['details']:
					book.edition = json_data['ISBN:' + isbn]['details']['revision']	
			else:
				book.title = name
				book.isbn10 = isbn
			book.save()

books = Book.objects.all()
count = 0
for book in books:
	if book.author == None or book.isbn13 == None:
		if count <= 490:
			link2 = "http://isbndb.com/api/books.xml?access_key=2H3HPUXH&results=details&index1=isbn&value1=" + isbn
			data2 = urllib2.urlopen(link2)
			b = data2.read()
			isbn13_pos = b.find("isbn13")
			isbn13 = b[isbn13_pos+8:isbn13_pos+21]
			book.isbn13 = isbn13
			dom = parseString(b)
			xmlTag = dom.getElementsByTagName("AuthorsText")
			xmlData= xmlTag.replace("AuthorsText",'').replace("AuthorsText",'')
			book.author = xmlData 
			book.save()
			count += 1
			print count
		else:
			break

print "Load Book data successfully"

