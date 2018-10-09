#!/usr/bin/env python3

from equation import challenge, solve, Expression, ops
import os, socketserver, threading, traceback

HOST, PORT = "0.0.0.0", int(os.environ.get("PORT", 24003))
flag = open('flag', 'r').readline()

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.request.settimeout(2)
        chal, _, sol = challenge().partition(" => ")
        self.wfile.write(b"You have to send back a valid expression solving the given equation\n")
        self.wfile.write(b"ex: Given ((((5 ? 1) ? (2 ? 9)) ? ((3 ? 5) ? (0 ? 6))) ? (((3 ? 9) ? (6 ? 3)) ? ((7 ? 1) ? (9 ? 3)))) => -1\n")
        self.wfile.write(b"ex: Reply ((((5 + 1) + (2 + 9)) + ((3 + 5) + (0 + 6))) + (((3 + 9) - (6 + 3)) - ((7 + 1) + (9 * 3))))\n")
        self.wfile.write(f"{chal} => {sol}\n\n".encode())

        self.data = self.rfile.readline().strip()
        print(f"{self.client_address[0]} wrote: {self.data.decode()}")
        try:
            result = Expression.fromstring(self.data.decode())
            exp = solve(f"{chal} => {sol}")
            assert exp.level() == result.level()
        except Exception as e:
            traceback.print_exc()
            self.wfile.write(b"Invalid expression; Try harder\n")
        else:
            n1, n2 = len(chal), len(str(result))
            if n1 != n2:
                self.wfile.write(b"Invalid expression; Input has wrong size\n")
                return
            for c1, c2 in zip(str(exp), str(result)):
                if c1 != c2 and c2 not in ops.values():
                    self.wfile.write(b"Invalid expression; Input mismatch\n")
                    return
            if int(result) == int(sol):
                print("Success!")
                self.wfile.write(f"Congratulations! {flag}\n".encode())
            else:
                print("Failure!")
                self.wfile.write(f"Wrong answer ({int(result)} != {int(sol)}); Try harder!\n".encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
