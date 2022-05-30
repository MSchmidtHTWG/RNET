import socket
from struct import unpack, pack

def registerRequestB(nick):
    return pack(f'BB{len(nick)}s', 1, len(nick), nick.encode('utf-8'))

def addUserB(nick, ip, port):
    return pack(f'BB{len(nick)}sIH', 3, len(nick), nick.encode('utf-8'), ip, port)

def broadcastMsgB(msg):
    return pack(f'BB{len(msg)}s', 5, len(msg), msg.encode('utf-8'))

def broadcastB(nick, msg):
    return pack(f'BB{len(nick)}sB{len(msg)}s', 6, len(nick), nick.encode('utf-8'), len(msg), msg.encode('utf-8'))

def logoutB():
    return pack(f'B', 7)

def removeUserB(nick):
    return pack(f'BB{len(nick)}s', 8, len(nick), nick.encode('utf-8'))