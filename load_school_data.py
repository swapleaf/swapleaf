# Full path and name to your csv file
import os
ROOT_PATH = os.path.dirname(__file__)

csv_filepathname=os.path.join(ROOT_PATH, 'swapleaf/db/raw/All_US_UniCollCC_Master.csv')

# Full path to your django project directory
swapleaf_project = os.path.join(ROOT_PATH, 'swapleaf')
import sys,os
sys.path.append(swapleaf_project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from swapleaf.app.main.models import Institution
from django.contrib.auth.models import User

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
	if row[0] != 'name': # Ignore the header row, import everything else
		institution = Institution()
		institution.name = row[0]
		institution.state = row[1]
		institution.city = row[2]
		institution.save()

print "Load School data successfully"

