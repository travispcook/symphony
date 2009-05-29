#!/usr/bin/env python

import MySQLdb
from cPickle import dump

conn = MySQLdb.connect(host="cellofellow.homelinux.net", user="symphony", passwd="beethoven", db="symphony2")
cursor = conn.cursor()
cursor.execute('SELECT * FROM Inventory;')
recordset = cursor.fetchall()
recordlist = []
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

for record in recordset:
	recordlist.append(dict(zip(fields, record)))

dump(tuple(recordlist), dumpfile)
dumpfile.close()
