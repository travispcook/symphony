<?

$action = $_POST['action'];
$id = $_POST['id'];
$cabinetgroup = $_POST['cabinetgroup'];
$cabinetid = $_POST['cabinetid'];
$drawerid = $_POST['drawerid'];
$folderid = $_POST['folderid'];
$title = $_POST['title'];
$composer = $_POST['composer'];
$arranger = $_POST['arranger'];
$lys = $_POST['lys'];
$lbcs = $_POST['lcbs'];
$lyco = $_POST['lyco'];
$inst = $_POST['inst'];
$score = $_POST['score'];
$rating = $_POST['rating'];

#print("inst: $inst<br>");


$page_top = "<html><head><title>Search Inventory</title></head><body bgcolor='white'><table cellspacing=10><tr>
<td><img src='note.jpg'></img></td>
<td valign=center><font size=6><b>Music Library Catalog</b></font></td>
<td><img src='note.jpg'></img></td></tr></table>
<p><small><a href='.'>Home</a> | <a href='input'>Add Music</a> | <a href='browse'>Browse</a> | Search</small></p>
";

$search_box = "<br>Enter the criteria to search on in the box below and click 'search'.
<br><form method='POST' action='$PHP_SELF'>
<table border='1' cellpadding=3 style='border-collapse: collapse;' bordercolor='666666'>
<tr><td colspan=5 align=left bgcolor='#202080'><font color=white> Search Criteria </font></td>
</tr>
<tr>
<td>ID#<br><input name='id' type='text' value='$id'/>  </td><td> Cabinet Group<br><input name='cabinetgroup' type='text' value='$cabinetgroup'/> </td>
<td>Cabinet Number<br><input name='cabinetid' type='text' value='$cabinetid'/></td> <td> Drawer Number<br><input name='drawerid' type='text' value='$drawerid'/> </td>
<td>Folder Number<br><input name='folderid' type='text' value='$folderid' /></td>
</tr>
<tr><td>  Title<br><input name='title' type='text' value='$title'/></td><td> Composer<br> <input name='composer' value='$composer'/></td>
<td> Arranger<br><input name='arranger' value='$arranger'/> <td>Score Type<br><input name='score' value='$score'/></td></td><td><small><small>This slot left blank for<br />formatting purposes.</small></small></td>
</tr>
<tr><td> LYS History<br><input name='lys' value='$lys'/> </td><td> LBCS History<br><input name='lbcs' value='$lbcs' /> </td>
<td> LYCO History<br><input name='lyco' value='$lyco'/></td><td>Rating<br><input name='rating' value='$rating'/></td>
<td><small><small>This slot left blank for<br /> formatting purposes.</small></small></td>
</tr>
<tr><td colspan=5 align=left> <input value='Search' type='submit'/></td>
</table>
<input type='hidden' name='action' value='search'>
</form>
";


if($action=='search')
{
	$sql="select InventoryID, CabinetGroup, CabinetID, DrawerID, FolderID, Title, Composer, Arranger, LYShistory, LBCShistory, LYCOhistory, Score, Instrumentation, Comments, Rating
	from Inventory ";
	
	$addWhere=0;
	$addAnd=0;

	if($id != '')
	{
		$where .= " InventoryID LIKE('%$id%') ";
		$addWhere=1;
		$addAnd=1;
	}
	
	if($cabinetgroup !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " CabinetGroup LIKE('%$cabinetgroup%') ";
		$addAnd = 1;
		$addWhere = 1;
	}
	
	if($cabinetid !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " CabinetID LIKE('%$cabinetid%') ";
		$addAnd = 1;
		$addWhere =1;
	}
	
	if($drawerid !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " DrawerID LIKE('%$drawerid%') ";
		$addAnd = 1;
		$addWhere =1;
	}
	
	if($folderid !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " FolderID LIKE('%$folderid%') ";
		$addAnd = 1;
		$addWhere =1;
	}

	if($title != '')
	{
		if($addAnd) $where .= " and ";
		$where .= " Title LIKE('%$title%') ";
		$addAnd = 1;
		$addWhere = 1;
	}

	if($composer != '')
	{
		if($addAnd) $where .= " and ";
		$where .= " Composer LIKE('%$composer%') ";
		$addAnd = 1;
		$addWhere = 1;
	}

	if($arranger != '')
	{
		if($addAnd) $where .= " and ";
		$where .= " Arranger LIKE('%$arranger%') ";
		$addAnd = 1;
		$addWhere = 1;
	}
	
	if($lys != '')
	{
		if($addAnd) $where .= " and ";
		$where .= " LYShistory LIKE('%$lys%') ";
		$addAnd = 1;
		$addWhere = 1;
	}
	
	if($lbcs != '')
	{
		if($addAnd) $where .= " and ";
		$where .= " LBCShistory LIKE('%$lbcs%') ";
		$addAnd = 1;
		$addWhere = 1;
	}
	
	if($lyco !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " LYCOhistory LIKE('%$lyco%') ";
		$addAnd = 1;
		$addWhere =1;
	}

	if($inst != '')
	{
		if($addAnd) $where .= " and ";
		$where .= " Instrumentation LIKE('%$inst%') ";
		$addAnd = 1;
		$addWhere = 1;
	}
	
	if($score !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " Score LIKE('%$score%') ";
		$addAnd = 1;
		$addWhere =1;
	}
	
	if($rating !='')
	{
		if($addAnd) $where .= " and ";
		$where .= " Rating LIKE('$rating') ";
		$addAnd = 1;
		$addWhere =1;
	}

	if($addWhere) $sql .= " where " . $where;


	$table_data = getTableData($sql);	


}	


print($page_top);
print($search_box);
print($table_data);



function GetTableData($sql)
{
	
        $db = @mysql_pconnect("localhost", "symphony", "beethoven") or exit("couldn't connect.\n");

        mysql_select_db("symphony") or exit("tried unsuccessfully to connect to symphony\n");
	
#	print("sql:$sql<br>");

        $result = mysql_query($sql);

	$data="<table  border='1' cellpadding=3 style='border-collapse: collapse;' bordercolor='666666'>
		<tr><td>ID#</td>
		<td>Cabinet Group</td>
		<td>Cabinet Number</td>
		<td>Drawer Number</td>
		<td>Folder Number</td>
		<td>Title</td>
		<td>Composer</td>
		<td>Arranger</td>
		<td>LYS History</td>
		<td>LBCS History</td>
		<td>LYCO History</td>
		<td>Instrumentation</td>
		<td>Score Type</td>
		<td>Comments</td>
		<td>Rating</td></tr>";

        while($row = mysql_fetch_array($result))
        {
                $id = $row[0];
                $cabinetgroup = $row[1];
		$cabinetid = $row[2];
		$drawerid = $row[3];
		$folderid = $row[4];
                $title = $row[5];
                $composer = $row[6];
                $arranger = $row[7];
                $lys = $row[8];
                $lbcs = $row[9];
		$lyco = $row[10];
		$inst = $row[11];
		$score = $row[12];
                $comments = $row[13];
		$rating = $row[14];

		$data .= "<tr><td><a href='view?id=$id'>$id</a></td>
			<td>$cabinetgroup</td>
			<td>$cabinetid</td>
			<td>$drawerid</td>
			<td>$folderid</td>
			<td>$title</td>
			<td>$composer</td>
			<td>$arranger</td>
			<td>$lys</td>
			<td>$lbcs</td>
			<td>$lyco</td>
			<td>$score</td>
			<td>$inst</td>
			<td>$comments</td>
			<td>$rating</td>
			</tr>";


        }

        mysql_free_result($result);

	$data .="</table>";

	return $data;
	
}

echo '</body></html>'

?>
