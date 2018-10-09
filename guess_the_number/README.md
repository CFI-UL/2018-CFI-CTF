# Guess the number

> programming

Author: [filedesless](https://github.com/filedesless)

`localhost:24000`

I'm thinking of a number between 0 and 4294967296
You have 40 tries to guess it

Here are some interesting reads: 

 - https://docs.python.org/3/library/socket.html
 - https://en.wikipedia.org/wiki/Algorithm


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

The challenge is a service running on port 24000, the user have to connect to it with a tool like netcat.

```
λ $ nc localhost 24000
I'm thinking of a number x such that 0 <= x <= 4294967296
You have 40 tries to guess it :)
```

A binary search in a range `n = 2**32` can be ran in about `log_2(n)` operations. The idea is to always cut the search space in half like the following pseudo-code<sup>1</sup>:

```
function binary_search(A, n, T):
    L := 0
    R := n − 1
    while L <= R:
        m := floor((L + R) / 2)
        if A[m] < T:
            L := m + 1
        else if A[m] > T:
            R := m - 1
        else:
            return m
    return unsuccessful
```

Here's an example of a working python solution; we basically connect to the server, and start guessing in the middle of the search space, lower bound at 0 and upper bound at 2 ** 32. Then we increase the lower bound or decrease the upper bound by half the remaining search space size per iteration.

```python
#!/usr/bin/env python3

import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 24000))

tries = 0

res = soc.recv(4096).decode()
print(res)
l, r = 0, 2 ** 32 - 1

while l <= r and "CFI" not in res:
    guess = l + (r - l) // 2
    clients_input = f"{guess}".encode()
    print(f"> {clients_input}")

    soc.send(clients_input) # we must encode the string to bytes
    tries += 1
    result_bytes = soc.recv(4096) # the number means how the response can be in bytes
    res = result_bytes.decode("utf8") # the return will be in bytes, so decode
    print(f"< {res}")

    if "high" in res:
        r = guess - 1
    elif "low" in res:
        l = guess + 1
```


Here's a flag for your trouble :)

`CFI{9F1B64A9D28E47B89A110CB360AADABD}`


refs:

  1. https://en.wikipedia.org/wiki/Binary\_search\_algorithm