import socket
from struct import unpack, pack

def registerRequestB(nick):
    return pack(f'BB{len(nick)}s', 1, len(nick), nick.encode('utf-8'))

def addUserB(nick, ip, port):
    return pack(f'BB{len(nick)}sIH', 3, len(nick), nick.encode('utf-8'), ip, port)

def broadcastMsgB(msg):
    return pack(f'BB{len(msg)}s', 5, len(msg), msg)