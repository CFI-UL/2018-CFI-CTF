# Fuck

> web

Author: [corb3nik](https://github.com/Corb3nik)

This is the most secure login form on earth.

We use SECURITY BY OBSCURITY in order to prevent hackers from finding our flags.

I dare you to login : http://localhost:17002

## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

This challenge requires us to find the username/password used in the login form.

When checking the source code of the HTML page, you'll see the following function.

```
function validate() {
  [][(![]+[])[+[]]+([![]] ...
}
```

At first, this doesn't seem like valid JavaScript. In fact, this is obfuscated
JavaScript resulting directly from a tool called [JSFuck](http://www.jsfuck.com/).

The gist of JSFuck is : using only 6 characters, we can create any character/string. It is also possible to obtain various objects/constructors through these same
6 characters. This allows us to create full working JavaScript scripts using only 6 chars.

You can see how its done here : https://github.com/aemkei/jsfuck/blob/master/jsfuck.js

To solve the challenge, we can paste the challenge script
into [JSUnfuck](http://codertab.com/JsUnFuck), revealing the following code :

```
if (document.forms[0].username.value == "corb3nik" && document.forms[0].password.value == "chickenachos") document.location = "4d4932602a75414640946d38ea6fefbf.php"
```

The flag is located at http://localhost:17002/4d4932602a75414640946d38ea6fefbf.php
