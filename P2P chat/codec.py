import socket
from struct import unpack, pack

def registerRequest_encode(nick, ip, port):
    return pack(f'BB{len(nick)}sIH', 1, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)

def addUser_encode(nick, ip, port):
    return pack(f'BB{len(nick)}sIH', 3, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)

def broadcastMsg_encode(msg):
    return pack(f'BB{len(msg)}s', 5, len(msg), msg.encode('utf-8'))

def broadcast_encode(nick, msg):
    return pack(f'BB{len(nick)}sB{len(msg)}s', 6, len(nick), nick.encode('utf-8'), len(msg), msg.encode('utf-8'))

def logout_encode():
    return pack(f'B', 7)

def removeUser_encode(nick):
    return pack(f'BB{len(nick)}s', 8, len(nick), nick.encode('utf-8'))