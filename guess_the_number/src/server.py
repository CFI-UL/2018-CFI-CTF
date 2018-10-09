#!/usr/bin/env python3

import socket
import os
import sys
import traceback
import random
from threading import Thread


PORT = int(os.environ.get("PORT", 24000))
flag = open('flag', 'r').readline()

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    RANDOM_NUMBER = random.randint(0, 2 ** 32)
    tries = 0
    conn.sendall(b"I'm thinking of a number x such that 0 <= x <= 4294967296\n")
    conn.sendall(b"You have 40 tries to guess it :)\n")

    while True:
        # the input is in bytes, so decode it
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

        # MAX_BUFFER_SIZE is how big the message can be
        # this is test if it's sufficiently big
        siz = sys.getsizeof(input_from_client_bytes)
        if  siz >= MAX_BUFFER_SIZE:
            print("The length of input is probably too long: {}".format(siz))

        # decode input and strip the end of line
        try:
            guess = int(input_from_client_bytes.decode("utf8").rstrip())
        except ValueError:
            conn.sendall(b"That's not an int!\n")
            break
        else:
            tries += 1
            if guess < RANDOM_NUMBER:
                conn.sendall(f"Your guess is too low; {40 - tries} tries left\n".encode())
            elif guess > RANDOM_NUMBER:
                conn.sendall(f"Your guess is too high; {40 - tries} tries left\n".encode())
            else:
                conn.sendall(f"You won!\n{flag}\n".encode())
                break

        if tries > 40:
            break

    conn.sendall(b"Bye! o/\n")
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " ended")

def start_server():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(("0.0.0.0", PORT))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            traceback.print_exc()
    soc.close()

start_server()  
