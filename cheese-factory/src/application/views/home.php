<h1>The Cheese Factory</h1>

<h2>Our cheeses</h2>
<?php
	$cheeses = array();
	$results = $config['db']->query('SELECT * FROM cheeses WHERE secret = 0;');
	while ($result = $results->fetchArray(1)) {
		$cheeses[] = $result;
	}
?>
<?php if ($cheeses) { ?>
	<div class="row marketing">
		<?php foreach ($cheeses as $cheese): ?>
			<div class="col-md-3">
		 	 <h4><?php echo $cheese['name']; ?></h4>
			 <img class="cheese-image img-rounded" src="<?php echo $cheese['image']; ?>" alt="Cheese image">
		 	 <p><?php echo $cheese['description']; ?></p>
			 <!-- secret: <?php echo $cheese['secret']; ?> -->
		   </div>
		<?php endforeach; ?>
	</div>
<?php } ?>
