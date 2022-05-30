import pstats
import socket
import threading
from struct import unpack, pack
from _thread import *

class Server:
    def __init__(self):
        self.port = 5000
        self.ip = '127.0.0.1'
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ip, self.port))
        self.lock = threading.Lock()
        self.users = dict()
        self.listen()
    
    def listen(self):
        while True:
            self.serverSocket.listen(2)
            connectionSocket, addr = self.serverSocket.accept()
            #thread mit socket und addr erstellen
            self.lock.acquire()
            start_new_thread(self.user, (connectionSocket, addr))
            self.lock.release()
            
    def user(self, connectionSocket, addr):
        # rcv reg req
        # update dict
        # wait for new msg
        pass