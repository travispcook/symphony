#!/usr/bin/env python

import sys, MySQLdb

from django.core.management import setup_environ
sys.path.insert(0, '/home/josh/Development/Django/symphony')
import settings; setup_environ(settings)

from apps.library.models import\
	Composer,\
	Arranger,\
	Piece,\
	ScoreType,\
	CabinetGroup,\
	Cabinet,\
	Drawer,\
	Orchestra,\
	Performance

conn = MySQLdb.connect(host="cellofellow.homelinux.net", user="symphony", passwd="beethoven", db="symphony2")
cursor = conn.cursor()
cursor.execute('SELECT * FROM Inventory;')
recordset = cursor.fetchall()
records = []
fields = (
	'inventoryID',
	'CabinetGroup',
	'CabinetID',
	'DrawerID',
	'Title',
	'Composer',
	'Arranger',
	'LYShistory',
	'LBCShistory',
	'LYCOhistory',
	'Instrumentation',
	'Score',
	'Comments',
	'Rating'
)
dumpfile = open('inventorydb.p', 'w')

traditional = Composer.objects.create(last_name = 'Traditional', first_name='Traditional')
various = Composer.objects.create(last_name = 'Various', first_name = 'Various')
unknown = Composer.objects.create(last_name='Unknown', first_name='Unknown')

for record in recordset:
	records.append(dict(zip(fields, record)))

for record in records:
	print 'Adding record %d' % record['inventoryID']
	try:
		inventoryid = Piece.objects.get(pk=record['inventoryID'])
		print 'Already added'
		continue
	except: pass

	try: cabinetgroup = CabinetGroup.objects.get(shortname = record['CabinetGroup'])
	except:
		description = raw_input('New group %s found.\nPlease enter a description of this group: ' % record['CabinetGroup'])
		cabinetgroup = CabinetGroup.objects.create(shortname = record['CabinetGroup'], description = description)
	
	try: cabinet = Cabinet.objects.get(number = int(record['CabinetID']), group = cabinetgroup)
	except:
		cabinet = Cabinet.objects.create(number = int(record['CabinetID']), group = cabinetgroup)
	
	try: drawer = Drawer.objects.get(number = int(record['DrawerID']), cabinet = cabinet)
	except:
		drawer = Drawer.objects.create(number = int(record['DrawerID']), cabinet = cabinet)
	
	if record['Score']:
		try: scoretype = ScoreType.objects.get(name=record['Score'])
		except:
			description = raw_input('New score type %s found.\nPlease enter a description of this score type: ' % record['Score'])
			scoretype = ScoreType.objects.create(name = record['Score'], description = description)
	else: scoretype = None
	
	composers = []
	if record['Composer'] == 'Traditional': composers.append(traditional)
	elif record['Composer'] == 'Various': composers.append(various)
	elif record['Composer'] == 'Unknown': composers.append(unknown)
	else:
		for c in record['Composer'].split(' and '):
			c = c.split(', ')
			try: composers.append(Composer.objects.get(last_name=c[0], first_name=c[1]))
			except:
				cc = Composer.objects.create(last_name=c[0], first_name=c[1])
				composers.append(cc)
	
	arrangers = []
	if record['Arranger']:
		for a in record['Arranger'].split(' and '):
			a = a.rsplit(None, 1)
			try: arrangers.append(Arranger.objects.get(last_name=a[1], first_name=a[0]))
			except:
				aa = Arranger.objects.create(last_name=a[1], first_name=a[0])
				arrangers.append(aa)
	
	comment = record['Comments']
	if record['Instrumentation']:
		comment = comment + '\nInstrumentation comments:\n\t%s' % record['Instrumentation']
	if record['LYShistory']:
		comment = comment + '\nLincoln Youth Symphony performance history:\n\t%s' % record['LYShistory']
	
	title = record['Title'].split(': ', 1)
	try: subtitle = title[1]
	except: subtitle = ''
	title = title[0]
	
	piece = Piece.objects.create(pk = record['inventoryID'], drawer = drawer, title = title, subtitle = subtitle, score = scoretype, comment = comment)
	
	for composer in composers:
		piece.composer.add(composer)
	
	for arranger in arrangers:
		piece.arranger.add(arranger)
	
	piece.save()
	
	print 'Success\n'
