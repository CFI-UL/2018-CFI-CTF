<?php
$db = new SQLite3('./src/application/database/the-cheese-factory.db');
$sql = <<<QUERY
CREATE TABLE cheeses (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL UNIQUE,
 description TEXT NOT NULL,
 image TEXT NOT NULL,
 secret TINYINT NOT NULL
);
QUERY;

$statement = $db->prepare($sql);
$result = $statement->execute();
var_dump($result);

$raw = file_get_contents("./cheeses.json");
$cheeses = json_decode($raw, true);

foreach ($cheeses as $cheese) {
	$sql = 'INSERT INTO cheeses (name, description, image, secret) VALUES (:name, :description, :image, :secret);';
	$statement = $db->prepare($sql);
	$statement->bindValue(':name', $cheese['name'], SQLITE3_TEXT);
	$statement->bindValue(':description', $cheese['description'], SQLITE3_TEXT);
	$statement->bindValue(':image', $cheese['image'], SQLITE3_TEXT);
	$statement->bindValue(':secret', $cheese['secret'], SQLITE3_INTEGER);
	$result = $statement->execute();
	var_dump($result);
}
