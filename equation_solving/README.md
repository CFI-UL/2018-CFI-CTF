# equation_solving

> programming

Author: [filedesless](https://github.com/filedesless)

The user is presented with an equation with missing operators. He has to find a combination of operators satisfying the given equation.


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Example for the socket code can be found in `src/solution.py`. The "logic" is in the `solve()` function in `src/equation.py`.

It's basically a brute force of all the possible operator combinations

```python
from itertools import product
# ...

def solve(chall):
    s, _, goal = chall.partition(" => ")
    comb = product(ops.values(), repeat=s.count("?"))
    for guess in comb:
        i = iter(guess)
        attempt = "".join([ c if c is not "?" else next(i) for c in s ])
        e = Expression.fromstring(attempt)
        try: 
            if int(e) == int(goal):
                break
        except ZeroDivisionError:
            pass
```

Here `Expression.fromstring()` parses the string into an `Expression`, basically a binary tree where each nodes has an operator and two sub-expressions left and right.
