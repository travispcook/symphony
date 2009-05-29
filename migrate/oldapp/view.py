#!/usr/bin/env python

import cgitb; cgitb.enable()
import MySQLdb, cgi

form = cgi.FieldStorage(); id = form.getvalue('id')

# Connect to Database
conn = MySQLdb.connect(
	host="localhost",
	user="symphony",
	passwd="beethoven",
	db="symphony"
)
cursor = conn.cursor()

print """Content-type: text/html

<html><head><title>Josh's Eagle Project: View %s</title></head>
<body bgcolor="white">""" % id

if id != None:
	try:
		query = 'SELECT * FROM Inventory WHERE inventoryID = %s' % id
		cursor.execute(query)
		data = cursor.fetchone()
	except:
		print '<h1>Error: Item ID number %s not found. Sorry.</h1>' % id
		print '</body></html>'
		exit()
	
	print """
<img src="eaglescoutweb.jpg" style="float: left;" />
<img src="lbss.jpg" style="float: right;" />
<div style="margin-left: 214px;">
<h1>Lake Bonneville Symphonic Society:<br />
<small>Music Library Catalog</small></h1>
<h2>by Josh's Eagle Scout Leadership Project</h2>
<p><small><a href=".">Home</a> | <a href="input">Add Music</a> | <a href="browse">Browse</a> | <a href="search">Search</a></small></p>
"""

	print """<h2>Number %s</h2>
<p><small><a href="edit?id=%s">Edit this item</a> | <a href="view?id=%s">&lt;Previous</a> <a href="view?id=%s">Next&gt;</a></small></p>
<ul>
	<li><strong>Title: </strong>%s</li>
	<li><strong>Composer: </strong>%s</li>""" % (id, id, str(int(id) - 1), str(int(id) + 1), data[5], data[6])

        if data[7] != '':
		print " <li><strong>Arranger: </strong>%s</li>" % data[7]
	
	print """
	<li><strong>Score Type: </strong>%s</li>
	<li><strong>Cabinet Group: </strong>%s</li>
	<li><strong>Cabinet Number: </strong>%s</li>
	<li><strong>Drawer Number: </strong>%s</li>
""" % (data[12], data[1], data[2], data[3])

	if data[8] != '':
		print "	<li><strong>LYS Performance History: </strong>%s</li>" % data[8]

	if data[9] != '':
		print "	<li><strong>LBCS Performance History: </strong>%s</li>" % data[9]

	if data[10] != '':
		print "	<li><strong>LYCO Performance History: </strong>%s</li>" % data[10]
	
	if data[11] != '':
		print "	<li><strong>Instrumentation: </strong>%s</li>" % data[11]

	print """
	<li><strong>Rating: </strong> %s stars</li>
	<li><strong>Comments: </strong><pre>%s</pre></li>
</ul>
""" % (data[14], data[13])

	print "</div></body></html>"

else:
	print '<h2>Item not found.</h2>'
	print '<p><form action="view">Try a different number: <input type="text" name="id" size="2" /><input type="submit" value="Go" /></form></p>'
	print '<p>Or you can <a href="input">add more data</a> or <a href="search">search the database</a>.</p>'
	print '</div></body></html>'
