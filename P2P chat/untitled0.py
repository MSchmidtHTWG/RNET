# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:27:48 2022

@author: ma746sch
"""

import socket
from struct import unpack, pack

ip = '172.20.155.201'
port = 5079
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip, port))
sock.send(registerRequest(input("Nickname:")))
data = sock.rcv(1024)
print(data)

sock.close()
 
def registerRequest(text):
    x = len(text)
    return pack(f'B{x}s', x, text.encode('utf-8'))