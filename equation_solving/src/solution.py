#!/usr/bin/env python3

import socket
from equation import *

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 24003))

res = ""
while "\n\n" not in res:
    res += soc.recv(4096).decode()
chal = res.strip().split("\n")[-1]
sol = str(solve(chal))
print(sol)
soc.send(f"{sol}\n".encode())

res = ""
while "\n" not in res:
    res += soc.recv(4096).decode()
print(res)
