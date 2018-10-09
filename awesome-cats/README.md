# awesome-cats 🐈

> web

Author: [lilc4t](https://github.com/masterT)

My collection of awesome cats.

http://localhost:12001/


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Go to the `/index.html`, check the source code.

Nothing interesting.

Visit the other pages accessible from `/index.html`, check the source code.

Nothing interesting either.

Do some reconnaissance and you'll find the `robots.txt`:

```
# http://www.robotstxt.org/

User-agent: *

Allow: index.html

# Add pages under construction to start indexing them.
Allow: cats-best.html
Allow: cats-cute.html
Allow: cats-fat.html
Allow: cats-and-mouse.html

# Hide old versions.
Disallow: /index-last.html
Disallow: /index-very-last.html
Disallow: /index2.html
Disallow: /index3.html
Disallow: /index4.html

# Hide dev. stuff.
Disallow: /README.md
Disallow: /LICENSE
Disallow: /src/assets/stylesheets/*.scss

# Hide blast from the past.
Disallow: /static/assets/images/dog-*
Disallow: /index-old.html
Disallow: /old/index.html

# I don't want bots to index my private stuff.
Disallow: /secret/notes.md
Disallow: /secret/secret.md
Disallow: /secret/todo.md
Disallow: /secret/journal.md
Disallow: /secret/javascript.html
```

The flag is in the `/secret/journal.md`:

`CFI{nothing_sensitive_goes_in_robots.txt}`
