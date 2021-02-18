#!/usr/bin/env python3

import socket
import time

HOST = '84.104.226.204'  # The server's hostname or IP address
PORT = 50000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        s.sendall(b'Hello, world')
        data = s.recv(1024)
        print('Received', repr(data))
        time.sleep(0.1)
