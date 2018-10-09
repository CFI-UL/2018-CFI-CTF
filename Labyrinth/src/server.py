#!/usr/bin/env python3

from __future__ import annotations
from maze import RandomMaze
import os, socketserver, threading
import solver

HOST, PORT = "0.0.0.0", int(os.environ.get("PORT", 24001))
flag = open('flag', 'r').readline()

'''
Main componnent, presents the maze to the user and
verify its answer
'''

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        m = RandomMaze(89, 51)
        self.wfile.write(b"You have 2 seconds to send back a valid path between S and E\n")
        self.wfile.write(b"(ex: RIGHT,RIGHT,RIGHT,DOWN,RIGHT,RIGHT,UP,UP,UP,UP,UP,LEFT)\n")
        self.wfile.write(f"{m}\n\n".encode())

        self.data = self.rfile.readline().strip()
        print(f"{self.client_address[0]} wrote: {self.data.decode()}")
        result = solver.follow_path(m, self.data.decode())
        if result is not None and result.val == "E":
            print("Success!")
            self.wfile.write(f"{flag}\n".encode())
        else:
            print("Failure!")
            self.wfile.write(b"Wrong path; Try harder\n")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
