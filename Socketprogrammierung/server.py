import numpy as np
import socket
from struct import unpack, pack
from _thread import *
import threading

tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

class Server:
    def __init__(self, socketType=tcp):
        self.socketType = socketType
        self.serverSocket = socket.socket(socket.AF_INET, socketType)
        self.serverSocket.bind(('', 5000))
        self.lock = threading.Lock()
        if self.socketType == tcp:
            self.serverSocket.listen(2)

    def close(self, connectionSocket):
        connectionSocket.close()

    def threaded(self, connectionSocket):
        (id, result, clientAddress) = self.getMsg(connectionSocket)
        self.sendMsg(connectionSocket, clientAddress, id, result)
        connectionSocket.close()
            

    def do(self):
        connectionSocket = ''
        addr = ('', '')
        while True:
            if connectionSocket == '':
                if self.socketType == tcp:
                    connectionSocket, addr = self.serverSocket.accept()
                elif self.socketType == udp:
                    connectionSocket = self.serverSocket
            if connectionSocket != '':
                self.lock.acquire()
                start_new_thread(self.threaded, (connectionSocket,))
                connectionSocket = ''
                self.lock.release()

    def sendMsg(self, connectionSocket, clientAddress, id, result):
        formatted = pack("II", id, result)
        if self.socketType == tcp:
            connectionSocket.send(formatted)
        elif self.socketType == udp:
            connectionSocket.sendto(formatted, clientAddress)

    def getMsg(self, connectionSocket):
        clientAddress = ''
        if self.socketType == tcp:
            msg = connectionSocket.recv(2048)
        elif self.socketType == udp:
            msg, clientAddress = self.serverSocket.recvfrom(2048)
        part = unpack('IBB', msg[:6])
        id = int(part[0])
        s = int(part[1])
        n = int(part[2])
        partTwo = unpack(f'{s}s', msg[6: 6 + s])
        calcType = partTwo[0].decode('utf-8')
        values = unpack(f'{n}i', msg[6 + s:])
        result = self.calculate(calcType, values)
        return (id, result, clientAddress)

    def calculate(self, calcType, listOfNum):
        if(calcType == "Summe"):
            return np.sum(listOfNum)
        elif(calcType == "Produkt"):
            return np.prod(listOfNum)
        elif(calcType == "Minimum"):
            return np.min(listOfNum)
        elif(calcType == "Maximum"):
            return np.max(listOfNum)

server = Server()
server.do()