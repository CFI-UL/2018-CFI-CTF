# Magic Word

> web

Author: [corb3nik](https://github.com/Corb3nik)

Hacking is all about thinking outside the box.

Can you figure out this simple puzzle?

http://localhost:17001


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

This challenge demonstrates a very common bypass that you can find in webapp security.

The gist of the challenge is the following :
- The app takes a word from the user through the `?magic_word=` argument.
- It then replaces all instances of `bumfuzzle` with an empty string
- Finally, it checks if `bumfuzzle` is still there, even after the replacements.

This is the behavior described above :
```
preg_replace("/bumfuzzle/", "", "hello") // Returns "hello"
preg_replace("/bumfuzzle/", "", "hellobumfuzzle") // Returns "hello"
preg_replace("/bumfuzzle/", "", "bumfasdfuzzle") // Returns "bumfasdfuzzle"
```

Since `bumfuzzle` is removed, a simple trick we can use is to embed `bumfuzzle` inside `bumfuzzle`.

The solution is the following :
```
preg_replace("/bumfuzzle/", "", "bumfbumfuzzleuzzle") // Returns "bumfuzzle"
```

You can find the flag by visiting this URL : `http://localhost:17001/?magic_word=bumfbumfuzzleuzzle`.
