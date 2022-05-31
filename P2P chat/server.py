import pstats
import socket
import threading
from struct import unpack, pack
from _thread import *

class Codec:
    @staticmethod
    def registerRequest_encode(nick, ip, port):
        return pack(f'=BB{len(nick)}s{4}sH', 1, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)
    @staticmethod
    def registerResponse_encode(nick, ip, port):
        return pack(f'=BB{len(nick)}s{4}sH', 2, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)
    @staticmethod
    def addUser_encode(nick, ip, port):
        return pack(f'=BB{len(nick)}s{4}sH', 3, len(nick), nick.encode('utf-8'), socket.inet_aton(ip), port)
    @staticmethod
    def broadcastMsg_encode(msg):
        return pack(f'=BB{len(msg)}s', 5, len(msg), msg.encode('utf-8'))
    @staticmethod
    def broadcast_encode(nick, msg):
        return pack(f'=BB{len(nick)}sB{len(msg)}s', 6, len(nick), nick.encode('utf-8'), len(msg), msg.encode('utf-8'))
    @staticmethod
    def logout_encode():
        return pack(f'=B', 7)
    @staticmethod
    def removeUser_encode(nick):
        return pack(f'=BB{len(nick)}s', 8, len(nick), nick.encode('utf-8'))
    @staticmethod
    def registerRequest_decode(data):
        decoded = unpack(f'=BB{len(data)-8}sBBBBH', data)
        nick = str(decoded[2].decode('utf-8'))
        ip = str(decoded[3])+'.'+str(decoded[4])+'.'+str(decoded[5])+'.'+str(decoded[6])
        port = decoded[7]
        return (nick, ip, port)
    @staticmethod
    def registerResponse_decode(data):
        decoded = unpack(f'=BB{len(data)-8}sBBBBH', data)
        nick = decoded[2].decode('utf-8')
        ip = str(decoded[3])+'.'+str(decoded[4])+'.'+str(decoded[5])+'.'+str(decoded[6])
        port = decoded[7]
        return (nick, ip, port)
    @staticmethod
    def addUser_decode(data):
        decoded = unpack(f'=BB{len(data)-8}sBBBBH', data)
        nick = decoded[2].decode('utf-8')
        ip = str(decoded[3])+'.'+str(decoded[4])+'.'+str(decoded[5])+'.'+str(decoded[6])
        port = decoded[7]
        return (nick, ip, port)
    @staticmethod
    def broadcastMsg_decode(data):
        decoded = unpack(f'=BB{len(data)-2}s', data)
        return decoded[2].decode('utf-8')
    @staticmethod
    def broadcast_decode(data):
        nicklen = data[1]
        msglen = data[nicklen+2]
        decoded = unpack(f'=BB{nicklen}sB{msglen}s', data)
        nick = decoded[2].decode('utf-8')
        msg = decoded[4].decode('utf-8')
        return (nick, msg)
    @staticmethod
    def removeUser_decode(data):
        nicklen = data[1]
        decoded = unpack(f'=BB{nicklen}s', data)
        return decoded[2].decode('utf-8')

class Server:
    def __init__(self):
        self.port = 50
        self.ip = '127.0.0.1'
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ip, self.port))
        self.lock = threading.Lock()
        self.users = dict()
    
    def listen(self):
        print("server listens")
        while True:
            self.serverSocket.listen(2)
            userSocket, addr = self.serverSocket.accept()
            print("connection accepted")
            start_new_thread(self.user, (userSocket, addr))
            
    def user(self, userSocket, addr):
        data = userSocket.recv(1024)
        nick = ""
        if data[0] == 1:
            decoded = Codec.registerRequest_decode(data)
            nick = decoded[0]
            self.lock.acquire()
            self.users.update({nick : (decoded[1], decoded[2], userSocket)})
            print('added ' + nick)
            self.lock.release()
            self.register_response(userSocket, nick)
        else:
            return
        
        while True:
            data = userSocket.recv(1024)
            if data[0] == 5:
                msg = Codec.broadcastMsg_decode(data)
                self.lock.acquire()
                for user in self.users:
                    if self.users.get(user)[2] != userSocket:
                        self.users.get(user)[2].send(Codec.broadcast_encode(user, msg))
                self.lock.release()
            elif data[0] == 7:
                self.lock.acquire()
                self.users.pop(nick)
                print('removed ' + nick)
                for user in self.users:
                    self.users.get(user)[2].send(Codec.removeUser_encode(nick))
                self.lock.release()
                userSocket.close()
                return
    
    def manageUserList(self):
        pass
    
    def register_response(self, userSocket, nick):
        self.lock.acquire()
        for user in self.users:
            # if user != nick:
            userSocket.send(Codec.registerResponse_encode(user, self.users.get(user)[0], self.users.get(user)[1]))
        self.lock.release()
        return
    
server = Server()
server.listen()