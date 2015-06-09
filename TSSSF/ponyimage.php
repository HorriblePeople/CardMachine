<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

function sanitize($str)
{
  $retval = str_replace("`", "", $str);
  $retval = preg_replace("/(\r?\n)/", '\n', $retval);
  return $retval;
}

if (count($_POST) == 0) {
  $output = <<<EOF
<html>
<head>
<title>Make a pony card!</title>
</head>
<body>
<form name="pony_definition" action="" method="POST">
What card type do you want?<br />
  <input type="radio" name="card_type" value="Pony" checked="checked">Pony<br />
  <input type="radio" name="card_type" value="START">Start Card<br />
  <input type="radio" name="card_type" value="Ship">Ship<br />
  <input type="radio" name="card_type" value="Goal">Goal<br />
<br />
What image do you want the card to have?<br />
This can either be NOART to leave it blank or a URL to specify outside art.<br />
Only images from imgur or the secretshipfic booru are allowed.<br />
  <input type="text" name="card_art" value="Placeholder.png" size="100"><br />
<br />
What race symbol do you want?<br />
  <input type="radio" name="card_race" value="Earth Pony">Earth Pony<br />
  <input type="radio" name="card_race" value="Unicorn">Unicorn<br />
  <input type="radio" name="card_race" value="Pegasus">Pegasus<br />
  <input type="radio" name="card_race" value="Alicorn">Alicorn<br />
  <input type="radio" name="card_race" value="ChangelingEarthPony">Changeling Earth Pony<br />
  <input type="radio" name="card_race" value="ChangelingUnicorn">Changeling Unicorn<br />
  <input type="radio" name="card_race" value="ChangelingPegasus">Changeling Pegasus<br />
  <input type="radio" name="card_race" value="ChangelingAlicorn">Changeling Alicorn<br />
  <input type="radio" name="card_race" value="None" checked="checked">None<br />
<br />
What gender symbol do you want?<br />
  <input type="radio" name="card_gender" value="Male">Male<br />
  <input type="radio" name="card_gender" value="Female">Female<br />
  <input type="radio" name="card_gender" value="MaleFemale">Male/Female<br />
  <input type="radio" name="card_gender" value="None" checked="checked">None<br />
<br />
What other miscellaneous symbols do you want?<br />
  <input type="checkbox" name="card_symbols_dystopian">Dystopian Future<br />
<br />
What do you want to name the card?<br />
  <input type="text" name="card_name" value="Test Name" size="100"><br />
<br />
What keywords do you want the card to have?<br />
  <input type="text" name="card_keywords" value="Button Mash, Gamer" size="100"><br />
<br />
What body text do you want the card to have?<br />
  <textarea name="card_body" rows="12" cols="40" wrap="off"></textarea><br />
<br />
What flavor text do you want the card to have?<br />
  <textarea name="card_flavor" rows="12" cols="40" wrap="off"></textarea><br />
<br />
What expansion symbol do you want the card to have? (not currently working)<br />
  <input type="text" name="card_expansion" value="" size="100"><br />
<br />
What set do you want the card to be from?<br />
  <input type="text" name="card_set" value="" size="100"><br />
<br />
Lastly, an override box.  Only use this if you know what you are doing.  If there is anything in this box, the rest of the page will be ignored.<br />
  <input type="text" name="card_override" value="" size="100"><br />
<input type="submit" value="Make me a pony card!"><br />
</form>
</body>
</html>
EOF;
  print $output;
  die;
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
