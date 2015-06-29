<html>
<head>
<title>Generator Card Gallery</title>
</head>
<body>
<?php

$perpage = 30;
$per_row = 3;
$fp = fopen('../imgur_out.txt', 'r');
$filesize = fstat($fp)["size"];
$numcards = floor($filesize / 8);



if (isset($_GET['p'])) {
  $startpage = $_GET['p'];
} else {
 $startpage = '1';
}

print '<a href="cardgallery.php?p=1">First Page</a> ';

if ($startpage > 1) {
  print '<a href="cardgallery.php?p=' . ($startpage - 1) . '">Previous Page</a> ';
}

if ($startpage < ceil($numcards/$perpage)) {
  print '<a href="cardgallery.php?p=' . ($startpage + 1) . '">Next Page</a> ';
}

print '<a href="cardgallery.php?p=' . ceil($numcards/$perpage) . '">Last Page</a>';
print "<br />\n";
print '<table cellspacing="0" cellpadding="0" border="0">' . "\n";

$currentcard = (($startpage - 1) * $perpage) + 1;
$colnum = 0;
fseek($fp, ($currentcard - 1) * 8);
for ($i = 1; $i <= $perpage; $i++) {
  if ($currentcard > $numcards) {
    if ($colnum != 0)
      print "  </tr>\n";
    break;
  }
  if ($colnum == 0)
  	print "  <tr>\n";
  
  //print "currentcard is $currentcard and numcards is $numcards <br />\n";
  $imgur_id = trim(fgets($fp));
  $imgur_img = "https://i.imgur.com/" . $imgur_id . ".png";
  $imgur_url = "https://imgur.com/" . $imgur_id;
  print '    <td width="260px">';
  print '<a href="' . $imgur_url . '">';
  print '<img src="' . $imgur_img . '" width="260px"/></a></td>' . "\n";
  if ($colnum == ($per_row - 1))
  	print "  </tr>\n";
  $currentcard++;
  $colnum = ($colnum + 1) % $per_row;
}

fclose($fp);
//die(print_r($numcards, true));


print "</table>\n";
print '<a href="cardgallery.php?p=1">First Page</a> ';

if ($startpage > 1) {
  print '<a href="cardgallery.php?p=' . ($startpage - 1) . '">Previous Page</a> ';
}

if ($startpage < ceil($numcards/$perpage)) {
  print '<a href="cardgallery.php?p=' . ($startpage + 1) . '">Next Page</a> ';
}

print '<a href="cardgallery.php?p=' . ceil($numcards/$perpage) . '">Last Page</a>';
?>
</body>
</html>
