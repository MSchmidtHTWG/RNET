from threading import Thread, Event, Lock
import socket

ip = '127.0.0.2'
portRange = 50
openTCP = 0
openUDP = 0
tcpLock = Lock()
udpLock = Lock()

def countTCPPorts():
    tcpLock.acquire()
    global openTCP
    openTCP += 1
    tcpLock.release()

def countUDPPorts():
    udpLock.acquire()
    global openUDP
    openUDP += 1
    udpLock.release()

def checkUDP(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        skt.sendto("Hello World!".encode('utf-8'), (ip, port))
        data, addr = skt.recvfrom(1024)
        print("udp", data, "port:", port)
        countUDPPorts()
    except WindowsError as we:
        print("UDP: ", we)

    skt.close()


def checkTCP(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        skt.connect((ip, port))
        skt.send("Hello World!".encode('utf-8'))
        data = skt.recv(1024)
        print("tcp", data, "port:", port)
        countTCPPorts()
    except WindowsError as we:
        print("TCP: ", we)

    skt.close()

def checkConnection(port):
    checkTCP(port)
    checkUDP(port)



def startThreads():
    threads = []
    for i in range(portRange):
        t = Thread(target=checkConnection, args=(i+1,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

startThreads()

print(f'Anz. UDP: {openUDP}')
print(f'Anz. TCP: {openTCP}')
