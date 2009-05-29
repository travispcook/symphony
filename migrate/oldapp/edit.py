#!/usr/bin/env python

import cgitb; cgitb.enable()
import MySQLdb, cgi
from string import Template

def createScoreChooser(choice="No Score"):
	if choice == "Full Score":
		return """
		<option value="Full Score" selected="selected">Full Score</option>
		<option value="Condensed Score">Condensed Score</option>
		<option value="Piano Score">Piano Score</option>
		<option value="No Score">No Score</option>
"""
	elif choice == "Piano Score":
		return """
		<option value="Full Score">Full Score</option>
		<option value="Condensed Score">Condensed Score</option>
		<option value="Piano Score" selected="selected">Piano Score</option>
		<option value="No Score">No Score</option>
"""
	elif choice == "Condensed Score":
		return """
		<option value="Full Score">Full Score</option>
		<option value="Condensed Score" selected="selected">Condensed Score</option>
		<option value="Piano Score">Piano Score</option>
		<option value="No Score">No Score</option>
"""
	elif choice == "No Score":
		return """
		<option value="Full Score">Full Score</option>
		<option value="Condensed Score">Condensed Score</option>
		<option value="Piano Score">Piano Score</option>
		<option value="No Score" selected="selected">No Score</option>
"""
	else:
		return """
		<option value="" selected="selected">Entry Blank</option>
		<option value="Full Score">Full Score</option>
		<option value="Condensed Score">Condensed Score</option>
		<option value="Piano Score">Piano Score</option>
		<option value="No Score">No Score</option>
		
"""

def createRatingChooser(choice=0):
	int(choice)
	if choice == 0:
		return """
Unrated<input type="radio" checked="checked" name="Rating" value="0" /> | 
1 <input type="radio" name="Rating" value="1" />
2 <input type="radio" name="Rating" value="2" />
3 <input type="radio" name="Rating" value="3" />
4 <input type="radio" name="Rating" value="4" />
5 <input type="radio" name="Rating" value="5" />
"""
	elif choice == 1:
		return """
Unrated<input type="radio" name="Rating" value="0" /> | 
1<input type="radio" checked="checked" name="Rating" value="1" />
2<input type="radio" name="Rating" value="2" />
3<input type="radio" name="Rating" value="3" />
4<input type="radio" name="Rating" value="4" />
5<input type="radio" name="Rating" value="5" /> | 
"""
	elif choice == 2:
		return """
Unrated<input type="radio" name="Rating" value="0" /> | 
1<input type="radio" name="Rating" value="1" />
2<input type="radio" checked="checked" name="Rating" value="2" />
3<input type="radio" name="Rating" value="3" />
4<input type="radio" name="Rating" value="4" />
5<input type="radio" name="Rating" value="5" />
"""
	elif choice == 3:
		return """
Unrated<input type="radio" name="Rating" value="0" /> | 
1<input type="radio" name="Rating" value="1" />
2<input type="radio" name="Rating" value="2" />
3<input type="radio" checked="checked" name="Rating" value="3" />
4<input type="radio" name="Rating" value="4" />
5<input type="radio" name="Rating" value="5" /> 
"""
	elif choice == 4:
		return """
Unrated<input type="radio" name="Rating" value="0" /> | 
1<input type="radio" name="Rating" value="1" />
2<input type="radio" name="Rating" value="2" />
3<input type="radio" name="Rating" value="3" />
4<input type="radio" checked="checked" name="Rating" value="4" />
5<input type="radio" name="Rating" value="5" />
"""
	elif choice == 5:
		return """
Unrated<input type="radio" name="Rating" value="0" /> | 
1<input type="radio" name="Rating" value="1" /> 
2<input type="radio" name="Rating" value="2" />
3<input type="radio" name="Rating" value="3" />
4<input type="radio" name="Rating" value="4" />
5<input type="radio" checked="checked" name="Rating" value="5" />
"""

form = cgi.FieldStorage()

id = form.getvalue('id')
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
Rating = form.getvalue('Rating')
LYShistory = form.getvalue('LYShistory')
LBCShistory = form.getvalue('LBCShistory')
LYCOhistory = form.getvalue('LYCOhistory')
Delete = form.getvalue('Delete')

# Print Headers
print 'Content-type: text/html'
print
print "<html><head><title>Edit Catalog</title></head>"
print '<body bgcolor="white">'
print '<a href="http://lakebonnsymph.googlepages.com"><img src="lbss.jpg" style="float:right;" border=0 /></a>'
print '<h1>Edit Catalog</h1>'
print '<p><small><a href=".">Home</a> | <a href="input">Add Music</a> | <a href="browse">Browse</a> | <a href="search">Search</a></small></p>'

# Connect to Database
conn = MySQLdb.connect(
	host="localhost",
	user="symphony",
	passwd="beethoven",
	db="symphony"
)
cursor = conn.cursor()

# Make HTML and SQL template objects. When run as template.substitute() the variables marked with $ in the template get filled with corresponding values passed to the function.
# For example Template("Fill the $liquid pail.").substitute(liquid="water") becomes "Fill the water pail.".
formtemplate = Template('''
<tt>
<form method="post" action="edit">
<p>Item ID: <input size="2" name="inventoryID" type="text" value="$inventoryID" readonly="readonly" /> Cabinet Group: <input size="3" name="CabinetGroup" type="text" value="$CabinetGroup"> Cabinet Number: <input size="2" type="text" value="$CabinetID" name="CabinetID" /> Drawer Number: <input size="2" type="text" name="DrawerID" value="$DrawerID" /></p>
<p>Title: <input size="70" name="Title" type="text" value="$Title"></p>
<p>Composer: <input size="35" name="Composer" type="text" value="$Composer"> Arranger: <input size="35" name="Arranger" type="text" value="$Arranger"></p>
<p>Instrumentation: <input size="50" type="text" name="Instrumentation" value="$Instrumentation" />
Score: <select name="Score">$Score</select></p>
<p>Rating: $Rating</p>
<p>Comments:<br>
<textarea cols="80" rows="5" name="Comments">$Comments</textarea></p>
<p><input value="Submit" type="submit"> | <b>Delete this item? <input type="checkbox" name="Delete" value="Delete" /></b></p>
</form></tt>
''')

querytemplate = Template("""UPDATE Inventory SET
	inventoryID = $inventoryID,
	CabinetGroup = "$CabinetGroup",
	CabinetID = "$CabinetID",
	DrawerID = "$DrawerID",
	FolderID = "$FolderID",
	Title = "$Title",
	Composer = "$Composer",
	Arranger = "$Arranger",
	LYShistory = "$LYShistory",
	LBCShistory = "$LBCShistory",
	LYCOhistory = "$LYCOhistory",
	Instrumentation = "$Instrumentation",
	Score = "$Score",
	Comments = "$Comments",
	Rating = "$Rating"
WHERE inventoryID = $inventoryID LIMIT 1;
""")

if id != None:
	print '<h2>Edit Item</h2>'
	print '<p><a href="edit?id=%d">&lt; Previous</a> | <a href="edit?id=%d">Next &gt;</a></p>' % (int(id)-1, int(id)+1)
	try:
		query = 'SELECT * FROM Inventory WHERE inventoryID = %s' % id
		cursor.execute(query)
	except:
		print '<h1>Error: Item ID number %s not found. Sorry.</h1>' % id
	data = cursor.fetchone()
	scorehtml = createScoreChooser(data[12])
	ratinghtml = createRatingChooser(data[14])
	print formtemplate.substitute(inventoryID=data[0], CabinetGroup=data[1], CabinetID=data[2], DrawerID=data[3], FolderID=data[4], Title=data[5], Composer=data[6], Arranger=data[7], LYShistory=data[8], LBCShistory=data[9], LYCOhistory=data[10], Instrumentation=data[11], Score=scorehtml, Comments=data[13], Rating=ratinghtml)


elif inventoryID != None and id == None and Delete == None and (CabinetGroup, CabinetID, DrawerID, FolderID, Title, Composer, Arranger, Instrumentation, Score, Comments) != None:
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
	query = querytemplate.substitute(inventoryID=inventoryID, CabinetGroup=CabinetGroup, CabinetID=CabinetID, DrawerID=DrawerID, FolderID=FolderID, Title=Title, Composer=Composer, Arranger=Arranger, LYShistory=LYShistory, LBCShistory=LBCShistory, LYCOhistory=LYCOhistory, Instrumentation=Instrumentation, Score=Score, Comments=Comments, Rating=Rating)
	# Clean up some idiosyncrancies of this method.
	query = query.replace('"None"', '""')
	# Show the query for debugging purposes.
	#print '<p>query= %s</p>' % query
	# Execute the Query
	cursor.execute(query)
	print '<h2>Item Number %s Updated</h2>' % inventoryID
	print '<p><a href="edit?id=%d">&lt;Previous</a> | <a href="edit?id=%d">Next&gt;</a>' % (int(inventoryID)-1, int(inventoryID)+1)
	print '<p><form action="edit">Edit another item? Item Number: <input type="text" name="id" size="2" /><input type="submit" value="Edit" /></form></p>'
	print '<p>Or you can <a href="input">add more data</a> or <a href="search">search the database</a>.</p>'

elif inventoryID != None and Delete == "Delete":
	query = "DELETE FROM Inventory WHERE inventoryID = %s LIMIT 1;" % inventoryID
	#print '<p>query = %s</p>' % query
	cursor.execute(query)
	print '<h2>Item number %s Deleted</h2>' % inventoryID
	print '<p><form action="edit">Edit another item? Item Number: <input type="text" name="id" size="2" /><input type="submit" value="Edit" /></form></p>'
	print '<p>Or you can <a href="input">add more data</a> or <a href="search">search the database</a>.</p>'

elif id == None:
	print '<h2>Nothing to Edit</h2>'
	print '<p><form action="edit">Pick something to edit. Item Number: <input type="text" name="id" size="2" /><input type="submit" value="Edit" /></form></p>'
	print '<p>Or you can <a href="input">add more data</a> or <a href="search">search the database</a>.</p>'


else: print "<p>Something went Wrong</p>"

print '</body></html>'
