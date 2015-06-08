<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

function sanitize($str)
{
  $retval = str_replace("`", "", $str);
  $retval = preg_replace("/(\r?\n)/", '\n', $retval);
  return $retval;
}

$card_str = "";
$card_str .= $_POST["card_type"];

$card_art = sanitize($_POST["card_art"]);
$allowed_sites = ['/^https?:\/\/i\.imgur\.com\//',
                  '/^https?:\/\/img\.booru\.org\/secretshipfic\//'];

// If it's a URL, check it for validity
if (substr($card_art, 0, 4) === "http") {
  $found = false;
  foreach ($allowed_sites as $regex) {
    if (preg_match($regex, $card_art)) {
      // It's good, add it
      $card_str .= "`" . $card_art;
      $found = true;
      break;
    }
  }
  // It's a URL but not an approved one
  if ($found === false) {
    print "<b>Only URLs from imgur or the secretshipfic booru are allowed!</b><br />\n";
    $card_str .= "`NOART";
  }
} else {
  $card_str .= "`" . $_POST["card_art"];
}

$symbols_array = [];
if ($_POST["card_race"] != "None")
  array_push($symbols_array, $_POST["card_race"]);
if ($_POST["card_gender"] != "None")
  array_push($symbols_array, $_POST["card_gender"]);
if ($_POST["card_type"] == "Ship")
  $symbols_array = ["Ship"];
if ($_POST["card_type"] == "Goal")
  $symbols_array = ["Goal"];

if (array_key_exists("card_symbols_dystopian", $_POST))
  array_push($symbols_array, "Dystopian");

$card_str .= "`" . implode("!", $symbols_array);
$card_str .= "`" . sanitize($_POST["card_name"]);
$card_str .= "`" . sanitize($_POST["card_keywords"]);
$card_str .= "`" . sanitize($_POST["card_body"]);
$card_str .= "`" . sanitize($_POST["card_flavor"]);
$card_str .= "`" . sanitize($_POST["card_expansion"]);

if ($_POST["card_override"] != "")
  $card_str = $_POST["card_override"];

$filename = uniqid() . ".png";

print "<br /><br />" . $card_str . "<br />";
chdir("../");
$cmd_str = './single_card.py -c "' . base64_encode($card_str) . '" -s "' . base64_encode($_POST["card_set"]) . '" -o "TSSSF/' . $filename . '"';
exec($cmd_str, $cmd_out, $cmd_retval);
print "<br /> cmd_str is " . $cmd_str . "<br />";
print "<br />";
if ($cmd_retval == 0) {
  print '<img src="' . $filename . '" />';
} else {
  print "<b>Card build failed!</b> Output below:<br />";
  foreach ($cmd_out as $line)
    print $line . "<br />";
}
?>
