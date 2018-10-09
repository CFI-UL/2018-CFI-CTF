<?php
include('./application/config/config.php');

$page = $config['default-page'];
if (isset($_GET['page']) && strlen($_GET['page']) > 0) {
	$page = $_GET['page'];
}

if ($config['secure']) {
	$page = str_replace('../', '', $page);
}

$pagePath = './application/views/' . $page;
?>


<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Cheese Factory</title>

	 <style media="screen">
	 	.main {
			margin-top: 16px;
		}
		.cheese-image {
			width: 100%;
		}
	 </style>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>

	  <div class="container main">
       <div class="header clearfix">
         <nav>
           <ul class="nav nav-pills pull-right">
				  <?php foreach ($config['pages'] as $name) { ?>
					  <?php $pageTitle = explode('.', $name)[0]; ?>
				  		<li role="presentation">
							<a href="/?page=<?php echo $name ?>">
								<?php echo ucfirst($pageTitle) ?>
							</a>
						</li>
				  <?php } ?>
           </ul>
         </nav>
         <h3 class="text-muted">The Cheese Factory, Inc.</h3>
       </div>

       <div class="jumbotron">
         <h1>The Cheese Factory, Inc.</h1>
         <p class="lead">We make good cheeses, some smell, some don't, in all cases they're good.</p>
       </div>


		 <?php include($pagePath); ?>

       <footer class="footer">
         <p>&copy; The Cheese Factory, Inc.</p>
       </footer>

     </div> <!-- /container -->

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  </body>
</html>
