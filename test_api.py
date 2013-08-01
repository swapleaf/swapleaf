# Full path and name to your csv file
import os
ROOT_PATH = os.path.dirname(__file__)

filepath=os.path.join(ROOT_PATH, 'swapleaf/db/raw/disk1.gsd')

# Full path to your django project directory
swapleaf_project = os.path.join(ROOT_PATH, 'swapleaf')
import sys,os
sys.path.append(swapleaf_project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from swapleaf.app.main.models import Book
from swapleaf.helper.book import get_openlibrary_book
from django.contrib.auth.models import User

# import csv
# dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

f = open(filepath,"r")

import urllib2
import json

hash_isbn = {}

for row in f:
	words = row.split()
	get_openlibrary_book(words[1])

print "Load Book data successfully"

