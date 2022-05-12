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

def winErrorHandling(we, type, port):
    if we == 10054:
        print(f'{type} port {port} Fehler: server hat nicht geantwortet')
        return
    if we == 10060:
        print(f'{type} port {port} Fehler: server timeout')
        return
    if we == 10061:
        print(f'{type} port {port} Fehler: server hat zurückgewiesen')
        return


def checkUDP(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    type = "UDP"
    try:
        skt.sendto("Hello World!".encode('utf-8'), (ip, port))
        data, addr = skt.recvfrom(1024)
        print("udp", data, "port:", port)
        countUDPPorts()
    except socket.timeout:
        print("")
    except WindowsError as we:
        print("")

    skt.close()


def checkTCP(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    type = "TCP"
    try:
        skt.connect((ip, port))
        skt.send("Hello World!".encode('utf-8'))
        data = skt.recv(1024)
        print("tcp", data, "port:", port)
        countTCPPorts()
    except socket.timeout:
        print("timeout")
    except WindowsError as we:
        print("WindowsError")

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