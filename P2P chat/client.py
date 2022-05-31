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

class Client:
    def __init__(self) -> None:
        # self.serverIP = input('Server IP:')
        # self.serverPort = int(input('Server port:'))
        self.nick = input('Nickname:')
        self.ip = input('Your IP:')
        # self.tcp_port = int(input('Your tcp port:'))
        # self.udp_port = int(input ('Your udp port:'))
        self.serverIP = '127.0.0.1'
        self.serverPort = 50
        # self.nick = 'max'
        # self.ip = '127.0.0.2'
        self.tcp_port = 51
        self.udp_port = 52
        self.tcp_socket = None
        self.udp_socket = None
        self.users = dict()
        self.lock = threading.Lock()
        
    def connect(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.ip, self.udp_port))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((self.ip, self.tcp_port))
        self.tcp_socket.connect((self.serverIP, self.serverPort))
        self.tcp_socket.send(Codec.registerRequest_encode(self.nick, self.ip, self.udp_port))
        self.tcp_socket.settimeout(1)
        while True:
            try:
                data = self.tcp_socket.recv(1024)
                if data[0] == 2:
                    decoded = Codec.registerResponse_decode(data)
                    self.users.update({decoded[0] : (decoded[1], decoded[2])})
            except:
                self.tcp_socket.settimeout(0)
                break
        start_new_thread(self.listenToServer, ())
            
    def test(self):
        print(self.users)
        while True:
            x = input('list; broadcast; exit\n')
            if x == 'exit':
                self.tcp_socket.send(Codec.logout_encode())
                self.tcp_socket.close()
                self.udp_socket.close()
                return
            elif x == 'list':
                self.lock.acquire()
                print(self.users)
                self.lock.release()
            elif x == 'broadcast':
                msg = input('What message do you want to broadcast?\n')
                self.tcp_socket.send(Codec.broadcastMsg_encode(msg))
            
    def listenToServer(self):
        while True:
            try:
                data = self.tcp_socket.recvfrom(1024)
                if data[0] == 3:
                    self.lock.acquire()
                    nick, ip, port = Codec.addUser_decode(data)
                    self.users.update({nick : (ip, port)})
                    self.lock.release()
                elif data[0] == 6:
                    nick, msg = Codec.broadcast_decode(data)
                    print('Brodcasted message from ' + nick + ': ' + msg)
                elif data[0] == 8:
                    nick = Codec.removeUser_decode(data)
                    self.lock.acquire()
                    self.users.pop(nick)
                    self.lock.release()
            except:
                pass
                
    def listenForRequests(self):
        while True:
            data = self.udp_socket.recv(1024)
        pass
            
client = Client()
client.connect()
client.test()