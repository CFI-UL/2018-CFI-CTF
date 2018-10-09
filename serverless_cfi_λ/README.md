# serverless\_cfi\_λ

> programming

Author: [filedesless](https://github.com/filedesless)

This is a Haskell programming challenge. The user is required to make a small program that sorts given words (line by line, from stdin) by the sum  of their characters' ASCII values, and output them line by line to stdout. You can test your code in the web interface by pressing `submit` and the input, expected output, and actual output of your program will be sent back to you, or any compilation error that might have occured.


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Here's an example solution:

```haskell
import Data.List( sortOn )

-- computes the value of a given string 
value :: String -> Int
value line = sum $ map fromEnum line

-- sort input lines by their value
main = interact $ unlines . sortOn value . lines
```

Uses the `interact` function which takes a `String -> String` function as a parameters, and applies it to stdin before outputting its result to stdout. The function passed to it (via the `$` right-associative function application operator) is the composition (via the `.` operator) `unlines . sortOn value . lines`. 

`unlines` and `lines` are opposite functions, of respective types `[String] -> String` and `String -> [String]`, and are equivalent to `join` and `split` in other languages.

`sortOn` of type `Ord b => (a -> b) -> [a] -> [a]` from the module `Data.List` sorts a given list based on the application of a given function to all elements of the given list, provided said function returns an orderable.

The function used to sort here is `value`, it does the required task of computing the sum of the ASCII values of the characthers composing a given word.


refs:

* https://www.haskell.org/hoogle/
* http://learnyouahaskell.com/chapters 
