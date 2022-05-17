import socket
from struct import unpack, pack

IPadrr = "127.0.0.2"
port = 5000
tcp = socket.SOCK_STREAM
udp = socket.SOCK_DGRAM

class Client:

    def __init__(self, ip=IPadrr, port=port, socketType=tcp) :
        self.clientSocket = socket.socket(socket.AF_INET, socketType)
        self.ip = ip
        self.port = port
        self.socketType = socketType

    def do(self):
        socket.setdefaulttimeout(9.3)
        self.clientSocket.bind(('127.0.0.3', 3000))
        if self.socketType == tcp:
            self.clientSocket.connect((self.ip, self.port))
        ipaddr, port = self.clientSocket.getsockname()
        print(str(ipaddr))
        print(str(port))
        self.sendMsg()
        self.getMsg()
        self.clientSocket.close()

    def formatMsg(self, msg):
        splitMsg = msg.split(" ", 3)
        id = int(splitMsg[0])
        calc = splitMsg[1]
        n = int(splitMsg[2])
        listOfNum = list(map(int, splitMsg[3].split(" ")))
        return pack(f'=IBB{len(calc)}s{n}i', id, len(calc), n, calc.encode('utf-8'), *listOfNum)

    def sendMsg(self):
        print("<ID> <calculation> <numbersOfvalues> <values>")
        msg = input()
        msg = self.formatMsg(msg)
        if self.socketType == tcp:
            self.clientSocket.sendall(msg)
        elif self.socketType == udp:
            self.clientSocket.sendto(msg, (self.ip, self.port))

    def getMsg(self):
        if self.socketType == tcp:
            result = self.clientSocket.recv(2048)
        elif self.socketType == udp:
            result, _ = self.clientSocket.recvfrom(2048)
        result = unpack("II", result)
        print(result[1])

client = Client()
client.do()