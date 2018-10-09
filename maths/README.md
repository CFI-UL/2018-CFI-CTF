# maths

> programming

Author: [filedesless](https://github.com/filedesless)

Find the product of the digits of the sum of the first 10000 prime numbers


## Writeup

```haskell
import Data.Char

-- stolen prime generator
primes :: [Int]
primes = 2: 3: sieve (tail primes) [5,7..]
  where 
    sieve (p:ps) xs = h ++ sieve ps [x | x <- t, x `rem` p /= 0]  
      where (h,~(_:t)) = span (< p*p) xs

-- gets digits from string
digits :: String -> [Int]
digits s = map digitToInt s

-- find products of digits of the sum of ints
solve :: [Int] -> Int
solve p = product . digits . show $ sum p

-- enjoy
main = putStrLn . show . solve $ take 10000 primes
```
