#!/usr/bin/env python

import cgitb; cgitb.enable()
import MySQLdb

conn = MySQLdb.connect(
	host="localhost",
	user="symphony",
	passwd="beethoven",
	db="symphony"
)
cursor = conn.cursor()

print """Content-type: text/html

<html><head><title>Josh's Eagle Project</title></head>
<body bgcolor="white">
<img src="eaglescoutweb.jpg" style="float: left;" />
<img src="lbss.jpg" style="float: right;" />
<div style="margin-left: 214px;">
<h1>Lake Bonneville Symphonic Society:<br />
<small>Music Library Catalog</small></h1>
<h2>by Josh's Eagle Scout Leadership Project</h2>
<p><small><a href=".">Home</a> | <a href="/input">Add Music</a> | Browse | <a href="search">Search</a></small><p>
<h2>Browse Catalog</h2>
<ul>"""

item = "<li><a href='view?id=%d'>%d</a> <strong>%s</strong> by <em>%s</em></li>"

cursor.execute("SELECT * from Inventory order by inventoryID")
recordset = cursor.fetchall()

for record in recordset:
	print item % (int(record[0]), int(record[0]), str(record[5]), str(record[6]))

print "</ul></div></body></html>"
