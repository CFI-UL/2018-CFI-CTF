# The Cheese Factory

Very easy to setup the website. The cheeses are stored in an SQLite database.

## Requirements

- PHP

## Config

The entry point of the website is `./index.php`.

Modify config values in `./application/config/config.php`.

- error reporting level
- database path
- pages
- default page
- security
- etc.


### Current config recap

<!-- Too lazy to write proper sentences, just pasted the current config -->

$config = array();

// Environment
// $config['environment'] = 'production';
$config['environment'] = 'development';

// Security
$config['secure'] = true;

// Error reporting.
if ($config['environment'] === 'production') {
	ini_set('display_errors', 0);
	error_reporting(E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT & ~E_USER_NOTICE & ~E_USER_DEPRECATED);
}


// Database.
$config['database-path'] = dirname(__FILE__) . '/../database/the-cheese-factory.db';
$config['db'] = new SQLite3($config['database-path']);

// Pages
$config['pages'] = array('home.php', 'about.php', 'contact.php');
$config['default-page'] = $config['pages'][0];
