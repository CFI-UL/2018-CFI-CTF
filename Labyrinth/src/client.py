#!/usr/bin/env python3

import socket
from maze import CsvMaze
import solver

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 24001))

try:
    msg = ""
    while "\n\n" not in msg:
        part = sock.recv(4096)
        msg += part.decode()

    csv = "\n".join(msg.split("\n")[2:-2])
    m = CsvMaze(csv)
    sock.sendall(f"{solver.get_path(m)}\n".encode())
    print(sock.recv(4096).decode())

finally:
    sock.close()
