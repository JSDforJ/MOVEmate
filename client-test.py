import socket
import struct
import numpy as np

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 6712  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    while True:
        data = s.recv(1024)
        poses = []
        offset = 0
        while len(data) >= offset + 8:
            poses.append(np.frombuffer(data, dtype=np.float64, count=1, offset=offset)[0])
            offset += 8
        print(poses)
