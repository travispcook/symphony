#!/usr/bin/env python

import cgitb; cgitb.enable()
import MySQLdb, cgi
from string import Template

form = cgi.FieldStorage()

inventoryID = form.getvalue('inventoryID')
CabinetGroup = form.getvalue('CabinetGroup')
CabinetID = form.getvalue('CabinetID')
DrawerID = form.getvalue('DrawerID')
FolderID = form.getvalue('FolderID')
Title = form.getvalue('Title')
Composer = form.getvalue('Composer')
Arranger = form.getvalue('Arranger')
Instrumentation = form.getvalue('Instrumentation')
Score = form.getvalue('Score')
Comments = form.getvalue('Comments')

# Print Headers
print 'Content-type: text/html'
print
print '<html><head><title>Add Information to Catalog</title></head>'
print '<body bgcolor="white">'
print '<a href="http://lakebonnsymph.googlepages.com"><img src="lbss.jpg" style="float:right;" border=0 /></a>'
print '<h1>Add Information to Catalog</h1>'
print '<p><small><a href=".">Home</a> | Add Music | <a href="browse">Browse</a> | <a href="search">Search</a></small></p>'

# Connect to Database
conn = MySQLdb.connect(
	host="localhost",
	user="symphony",
	passwd="beethoven",
	db="symphony")
cursor = conn.cursor()

# Make HTML and SQL template objects. When run as template.substitute() the variables marked with $ in the template get filled with corresponding values passed to the function.
# For example Template("Fill the $liquid pail.").substitute(liquid="water") becomes "Fill the water pail.".
formtemplate = Template('''
<tt>
<form method="post" action="input">
<p>Item ID: <input size="2" name="inventoryID" type="text" value="$inventoryID"> Cabinet Group: <input size="3" name="CabinetGroup" type="text" value="$CabinetGroup"> Cabinet Number: <input size="2" type="text" value="$CabinetID" name="CabinetID" /> Drawer Number: <input size="2" type="text" name="DrawerID" value="$DrawerID" /> <!-- Folder Number: <input size="2" type="text" value="$FolderID" name="FolderID" /> --></p>
<p>Title: <input size="72" name="Title" type="text" value="$Title"></p>
<p>Composer: <input size="34" name="Composer" type="text" value="$Composer"> Arranger: <input size="35" name="Arranger" type="text" value="$Arranger"></p>
<p>Instrumentation: <input size="50" type="text" name="Instrumentation" value="$Instrumentation" />
Score: 
	<select name="Score">
		<option value="Full Score">Full Score</option>
		<option value="Condensed Score">Condensed Score</option>
		<option value="Piano Score">Piano Score</option>
		<option value="No Score">No Score</option>
	</select>
</p>
<p>Comments:<br>
<textarea cols="80" rows="5" name="Comments">$Comments</textarea></p>
<p><input value="Submit" type="submit"></p>
</form></tt>
''')

querytemplate = Template("""INSERT INTO Inventory (
	inventoryID, 
	CabinetGroup,
	CabinetID,
	DrawerID,
	FolderID,
	Title, 
	Composer, 
	Arranger,
	Instrumentation, 
	Score, 
	Comments) 
VALUES (
	$inventoryID, 
	"$CabinetGroup", 
	"$CabinetID",
	"$DrawerID",
	"$FolderID",
	"$Title", 
	"$Composer", 
	"$Arranger",
	"$Instrumentation", 
	"$Score",
	"$Comments")
""")

# If there was no input, display the blank input form.
if inventoryID==None and CabinetID==None and DrawerID==None and FolderID==None and Title==None and Composer==None and Arranger==None and Instrumentation==None and Score==None and Comments==None:
	print '<h2>Input new Item</h2>'
	print formtemplate.substitute(inventoryID='', Title='', CabinetGroup='GSYS', CabinetID='', DrawerID='', FolderID='', Composer='', Arranger='', Instrumentation='', Score='', Comments='')

# If there was input, add it to the MySQL database.
elif inventoryID!=None and (CabinetGroup, CabinetID, DrawerID, FolderID, Title, Composer, Arranger, Instrumentation, Score, Comments)!=None:
	# Escape Double Qoutes
	try: CabinetGroup = CabinetGroup.replace('"', '\\"')
	except AttributeError: pass
	try: CabinetID = CabinetID.replace('"', '\\"')
	except AttributeError: pass
	try: DrawerID = DrawerID.replace('"', '\\"')
	except AttributeError: pass
	try: FolderID = FolderID.replace('"', '\\"')
	except AttributeError: pass
	try: Title = Title.replace('"', '\\"')
	except AttributeError: pass
	try: Composer = Composer.replace('"', '\\"')
	except AttributeError: pass
	try: Arranger = Arranger.replace('"', '\\"')
	except AttributeError: pass
	try: Instrumentation = Instrumentation.replace('"', '\\"')
	except AttributeError: pass
	try: Score = Score.replace('"', '\\"')
	except AttributeError: pass
	try: Comments = Comments.replace('"', '\\"')
	except AttributeError: pass
	# Fill Query template with input.
	query = querytemplate.substitute(inventoryID=inventoryID, CabinetGroup=CabinetGroup, CabinetID=CabinetID, DrawerID=DrawerID, FolderID=FolderID, Title=Title, Composer=Composer, Arranger=Arranger, Instrumentation=Instrumentation, Score=Score, Comments=Comments)
	# Clean up some idiosyncrancies of this method.
	query = query.replace('"None"', '""')
	# Show the query for debugging purposes.
	#print '<p>query= %s</p>' % query
	# Execute the Query
	try:
		cursor.execute(query)
		print '<h2>New Item number %s Added. <small><a href="edit?id=%s">Click here to edit.</a></small></h2>' % (inventoryID, inventoryID)
		# Display the blank input form.
		print '<h2>Input new Item</h2>'
		if Instrumentation == "None": Instrumentation = ""
		print formtemplate.substitute(inventoryID=str(int(inventoryID) + 1), Title='', CabinetGroup=CabinetGroup, CabinetID=CabinetID, DrawerID=DrawerID, FolderID='', Composer='', Arranger='', Instrumentation=Instrumentation, Score='', Comments='')

	except:
		print "<h2>Duplicate Entry. ID Number <a href='edit?id=%s'>%s</a> already used. Pick a different one.</h2>" % (inventoryID, inventoryID)
		form = formtemplate.substitute(inventoryID='', CabinetGroup=CabinetGroup, CabinetID=CabinetID, DrawerID=DrawerID, FolderID=FolderID, Title=Title, Composer=Composer, Arranger=Arranger, Instrumentation=Instrumentation, Score=Score, Comments=Comments)
		print form.replace('"None"', '""').replace('None</textarea>', '</textarea>')

# Check that there was an inventoryID number supplied with other input.
elif inventoryID == None and (CabinetGroup, CabinetID, DrawerID, FolderID, Title, Composer, Arranger, Instrumentation, Score, Comments) != None:
	print '<h1>Error: You <em>must</em> put in an Item ID.</h1>'

else: print "Something went Wrong"

print '</body></html>'
