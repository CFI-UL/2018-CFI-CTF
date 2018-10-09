<!DOCTYPE HTML>
<?php
  require("flag.php");

  if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    die();
  }

  if (isset($_GET['magic_word'])) {

    $what_he_said = $_GET['magic_word'];
    $what_you_dont_want_to_hear = 'bumfuzzle';
    $what_you_actually_heard = preg_replace(
	    	"/$what_you_dont_want_to_hear/", '', $what_he_said);

    if ($what_you_actually_heard === $what_you_dont_want_to_hear) {
      get_mad_and_give_flag();
    }
  }
?>

<html>
  <head>
    <title>Magic Word</title>
  </head>
  <body>
    <h1>Hacking is all about thinking outside the box</h1>
    <p>Try to reach <code>get_mad_and_give_flag()</code></p>
    <a target="_blank" href="?source">View the source</a>

  </body>
</html>
