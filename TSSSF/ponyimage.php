<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

function sanitize($str)
{
  $retval = str_replace("`", "", $str);
  $retval = preg_replace("/(\r?\n)/", '\n', $retval);
  return $retval;
}

function dieError($error,$details,$allowed=NULL){
  if (is_null($allowed)) {
    die(json_encode(Array(
      "error"=>$error,
      "details"=>$details
    )));
  } else {
    die(json_encode(Array(
      "error"=>$error,
      "details"=>$details,
      "allowed"=>$allowed
    )));
  }
}

$http_origin = $_SERVER['HTTP_ORIGIN'];
//Add your domain here if you want to be able to do CORS cross-domain requests
$origin_array = array("http://latent-logic.github.io",
                      "http://coandco.github.io");

if (in_array($http_origin, $origin_array))
{
    header("Access-Control-Allow-Origin: $http_origin");
}

//Uncomment to turn this script into a POST reflector for debug purposes
//die(json_encode($_POST));

$imagetype = isset($_POST["imagetype"]) ? $_POST["imagetype"] : "cropped";
$returntype = isset($_POST["returntype"]) ? $_POST["returntype"] : "encoded_url";

if(isset($_POST["pycard"])) {
  $pycard_arr = explode("`", $_POST["pycard"]);
  if (count($pycard_arr) < 7)
    dieError("Pycard string failed basic sanity check (at least 6 backticks)", 
             $_POST["pycard"]);

  //Type check
  $valid_types = array("Pony", "Ship", "Goal", "Start");
  if (!in_array($pycard_arr[0], $valid_types))
    dieError("Invalid card type", $pycard_arr[0]);

  //Art check
  $allowed_sites = ['/^https?:\/\/i\.imgur\.com\//',
                    '/^https?:\/\/img\.booru\.org\/secretshipfic\//',
                    '/^https?:\/\/derpicdn.net\//'];
  $found = false;
  foreach ($allowed_sites as $regex) {
    if (preg_match($regex, $pycard_arr[1])) {
      $found = true;
      break;
    }
  }
  if ($found === false && $pycard_arr[1] != "")
    dieError("Art URL not on allowed list",
             array("allowed_sites" => $allowed_sites,
                   "art_url" => $pycard_arr[1]));

  //Symbols check
  $valid_symbols = array("male", "female", "malefemale",
                         "earthpony", "unicorn", "pegasus", "alicorn",
                         "changelingearthpony", "changelingunicorn",
                         "changelingpegasus", "changelingalicorn",
                         "dystopian", "ship", "goal",
                         "0", "1", "2", "3", "4", "3-4", "2-3");
  $symbols_array = explode("!", str_replace(" ", "", strtolower($pycard_arr[2])));
  foreach ($symbols_array as $symbol) {
    if (!in_array($symbol, $valid_symbols))
      dieError("Unrecognized symbol", $symbol);
  }

  //Modes check
  if (!in_array($imagetype, array("bleed", "cropped", "vassal")))
    dieError("Invalid image type", $imagetype);
  if (!in_array($returntype, array("file", "encoded_url", "imgur")))
    dieError("Invalid return type", $return);
  $outstr = '';
  if ($returntype == "file")
    $outstr = '-o "TSSSF/' . uniqid() . '.png"';

  $card_str = implode("`", $pycard_arr);
  $encoded_str = base64_encode(utf8_encode($card_str));

  chdir("../");

  $cmd_str = './single_card.py -c "' . $encoded_str . '"' . " -i $imagetype -r $returntype " . $outstr;

  exec($cmd_str, $cmd_out, $cmd_retval);

  if ($cmd_retval == 0) {
    switch($returntype) {
      case "file":
        $img_url = "http://" . $_SERVER["HTTP_HOST"] . "/" . $cmd_out[0];
        break;
      case "imgur":
        $img_url = "http://imgur.com/" . $cmd_out[0];
        break;
      case "encoded_url":
        $img_url = $cmd_out[0];
        break;
    }
    die(json_encode(array("image" => $img_url,
                          "card_str" => $card_str)));
  } else {
    dieError("Card build failed!", $cmd_str);
  }
} else {
  dieError("No pycard string found", $_POST);
}

?>
