<?php
  require("secret.php");

  function encrypt($data) {
    global $iv, $key;

    return base64_encode(openssl_encrypt($data, "aes-128-ctr", $key, OPENSSL_RAW_DATA, $iv));
  }

  function decrypt($data) {
    global $iv, $key;

    return openssl_decrypt(base64_decode($data), "aes-128-ctr", $key,  OPENSSL_RAW_DATA, $iv);
  }

  if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit();
  }

  if (!isset($_COOKIE['auth'])) {
    $struct = new stdClass();
    $struct->allowed = false;
    $data = encrypt(json_encode($struct));
    setcookie("auth", $data); 
  } else {
    $struct = json_decode(decrypt($_COOKIE['auth']));
  }
?>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>

  <body>
    <div class="container">
      <br /><br />
      <?php
        if (isset($struct->allowed) && $struct->allowed === true) {
      ?>
      <div class="alert alert-success"><?php echo $flag; ?></div>
      <?php
        } else {
      ?>
      <div class="alert alert-danger">You are not allowed to view the flag.</div>
      <?php  
        }
      ?>

      <br /> 
      <br />
      <a href="index.php?source=">View the source</a> 
    </div>
  </body>
</html>
