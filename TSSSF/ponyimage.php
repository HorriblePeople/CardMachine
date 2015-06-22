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

function pipe_exec($cmd, $input='') {
    $proc = proc_open($cmd, array(array('pipe', 'r'),
                                  array('pipe', 'w'),
                                  array('pipe', 'w')), $pipes);
    fwrite($pipes[0], $input);
    fclose($pipes[0]);

    $stdout = stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    $stderr = stream_get_contents($pipes[2]);
    fclose($pipes[2]);

    $return_code = (int)proc_close($proc);

    return array($return_code, $stdout, $stderr);
}

$http_origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : NULL;
//Add your domain here if you want to be able to do CORS cross-domain requests
$origin_array = array("http://latent-logic.github.io",
                      "http://coandco.github.io");

if (in_array($http_origin, $origin_array) && !is_null($http_origin))
{
    header("Access-Control-Allow-Origin: $http_origin");
}

$content_type = isset($_SERVER["CONTENT_TYPE"]) ? $_SERVER["CONTENT_TYPE"] : "";

//If our content_type string starts with "application/json", decode it
if (substr($content_type, 0, strlen("application/json")) == "application/json"){
  $data = json_decode(file_get_contents('php://input'), true);
} else {
  $data = $_POST;
}

//dieError("Reflector", $data["pycard"]);

//Uncomment to turn this script into a POST reflector for debug purposes
//die(json_encode($_POST));

$imagetype = isset($data["imagetype"]) ? $data["imagetype"] : "cropped";
$returntype = isset($data["returntype"]) ? $data["returntype"] : "encoded_url";
$source_url = isset($data["my_url"]) ? $data["my_url"] : "";

if(isset($data["pycard"])) {
  $pycard_arr = explode("`", $data["pycard"]);
  if (count($pycard_arr) < 7)
    dieError("Pycard string failed basic sanity check (at least 6 backticks)", 
             $data["pycard"]);

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

  if (!preg_match('/TSSSF by Horrible People Games/', $pycard_arr[8])) {
    $pycard_arr[8] .= '; TSSSF by Horrible People Games';
  }

  //Modes check
  if (!in_array($imagetype, array("bleed", "cropped", "vassal")))
    dieError("Invalid image type", $imagetype);
  if (!in_array($returntype, array("file", "encoded_url", "imgur")))
    dieError("Invalid return type", $return);
  $outstr = '';
  if ($returntype == "file")
    $outstr = '-o "TSSSF/' . uniqid() . '.png" ';

  $imgurargs = '';
  if ($source_url != "") {
    //$imgurargs = '-t "' . base64_encode("Card generated by TSSSF Card Generator at " . $source_url) . '" ';
    $imgurargs .= '-d "' . base64_encode("An editable version of this card is available at " . $source_url . '.') . '" ';
  }

  $card_str = implode("`", $pycard_arr);
  $encoded_str = base64_encode($card_str);

  chdir("../");

  $cmd_str = './single_card.py -c "' . $encoded_str . '"' . " -i $imagetype -r $returntype " . $outstr . $imgurargs;

  list($cmd_retval, $cmd_stdout, $cmd_stderr) = pipe_exec($cmd_str);

  if ($cmd_retval == 0) {
    switch($returntype) {
      case "file":
        $img_url = "http://" . $_SERVER["HTTP_HOST"] . "/" . $cmd_stdout;
        break;
      case "imgur":
        $img_url = "http://imgur.com/" . $cmd_stdout;
        break;
      case "encoded_url":
        $img_url = $cmd_stdout;
        break;
    }
    die(json_encode(array("image" => $img_url,
                          "card_str" => $card_str,
                          "output" => $cmd_stderr)));
  } else {
    dieError("Card build failed!", $cmd_stderr);
  }
} else {
  dieError("No pycard string found", $data);
}

?>
