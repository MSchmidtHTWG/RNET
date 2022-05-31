import socket
from struct import unpack, pack

class Codec:
    def registerRequest_encode(nick, ip, port):
        return pack(f'BB{len(nick)}s{4}sH', 1, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)

    def addUser_encode(nick, ip, port):
        return pack(f'BB{len(nick)}s{4}sH', 3, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)

    def broadcastMsg_encode(msg):
        return pack(f'BB{len(msg)}s', 5, len(msg), msg.encode('utf-8'))

    def broadcast_encode(nick, msg):
        return pack(f'BB{len(nick)}sB{len(msg)}s', 6, len(nick), nick.encode('utf-8'), len(msg), msg.encode('utf-8'))

    def logout_encode():
        return pack(f'B', 7)

    def removeUser_encode(nick):
        return pack(f'BB{len(nick)}s', 8, len(nick), nick.encode('utf-8'))

    def registerRequest_decode(data):
        decoded = unpack(f'BB{len(data)-9}sBBBBH', data)
        nick = decoded[2].decode('utf-8')
        ip = str(decoded[3])+'.'+str(decoded[4])+'.'+str(decoded[5])+'.'+str(decoded[6])
        port = decoded[7]
        return (nick, ip, port)

    def addUser_decode(data):
        decoded = unpack(f'BB{len(data)-9}sBBBBH', data)
        nick = decoded[2].decode('utf-8')
        ip = str(decoded[3])+'.'+str(decoded[4])+'.'+str(decoded[5])+'.'+str(decoded[6])
        port = decoded[7]
        return (nick, ip, port)
    
    def broadcastMsg_decode(data):
        decoded = unpack(f'BB{len(data)-2}s', data)
        return decoded[2].decode('utf-8')
    
    def broadcast_decode(data):
        nicklen = data[1]
        msglen = data[nicklen+2]
        decoded = unpack(f'BB{nicklen}sB{msglen}s', data)
        nick = decoded[2].decode('utf-8')
        msg = decoded[4].decode('utf-8')
        return (nick, msg)
    
    def removeUser_decode(data):
        nicklen = data[1]
        decoded = unpack(f'BB{nicklen}s', data)
        return decoded[2].decode('utf-8')