import itertools
from heapq import heappush, heappop
from typing import List, Any
from threading import Thread
from threading import Event
from threading import Timer
import time
from time import sleep


heap = []  #Zeitpunkt, Prio, Nr, Funktion
counter = itertools.count()

teiler = 100

# Output Text Declare
UserDoc = open('supermarkt_customer.txt', 'w+') 
stationDoc = open('supermarkt_station.txt', 'w+') 
supermarktDoc = open('supermarkt.txt', 'w+') 


def getTimer():
    return (time.time() - StartZeit)*teiler

class Station(Thread):

    def __init__(self, Dauer, Liste, name="leer", nummer=0, bEmpty = 0):
        Thread.__init__(self)
        self.Warteschlange = Liste
        self.Name = name
        self.bEmpty = bEmpty
        self.nummer = nummer
        self.Dauer = Dauer
        self.Amount = 0
        self.isService = False

    def isEmpty(self):
        return self.bEmpty

    def setListe(self, amount, Event):
        self.Warteschlange.append([amount*self.Dauer, Event])

    def isMyTurn(self, Kundename):
        if(self.Warteschlange[0] == Kundename):
            return True
        return False
      
    def startservice(self, amount, args):
        arg = [0]*1
        arg[0] = args
        t = Timer(amount, self.doneservice, arg)
        t.start()
      
    def doneservice(self, arg):
        arg.set()
        del self.Warteschlange[0]  # remove bedienten kunden
        self.isService = False

    def remove(self, Kunde):
        if(len(self.Warteschlange) == 1 and self.Warteschlange.count(Kunde.Name) > 0):
            self.bEmpty = 0
            self.Warteschlange.remove(Kunde.Name)
        elif(len(self.Warteschlange) > 1 and self.Warteschlange.count(Kunde.Name) > 0):
            self.Warteschlange.remove(Kunde.Name)
        
    def run(self):
        arrEv[self.nummer].wait()
        while(True):
          if(self.isService != True): #ob keiner bedient wird
            if(len(self.Warteschlange) != 0): #ob mind. einer Wartet
                self.isService = True
                self.startservice(self.Warteschlange[0][0], self.Warteschlange[0][1])

arrEv = []
arrEv.append(Event()) 
arrEv.append(Event())      
arrEv.append(Event()) 
arrEv.append(Event())

Theken = []
# Theke[0] = Baecker, [1] = kaese, [2] = Wurst, [3] = kasse
Theken.append(Station(10/teiler, [], "Bäcker", 0))
Theken.append(Station(60/teiler, [], "Käse", 1))
Theken.append(Station(30/teiler, [], "Metzger", 2))
Theken.append(Station(5/teiler, [], "Kasse", 3))


class User(Thread):
    def __init__(self, TypInformation, order, Name = ""):
        Thread.__init__(self)
        self.Name = Name
        self.Position = -1
        self.Order = order
        self.Laufen = TypInformation[0]
        self.WarteschlangeMax = TypInformation[1]
        self.KaufeAnzahl = TypInformation[2]

    def anzahlDerEinkaeufe(self):
        return len(self.Laufen)

    def getPosition(self):
        return self.Position

    def incPosition(self):
        self.Position += 1

    def walk(self):
        return self.Laufen[self.Position]

    def getWarteschlangeMax(self):
        if(self.Position < self.anzahlDerEinkaeufe()):
            return self.WarteschlangeMax[self.Position]
        else:
            return -1
            
    def run(self): 
        while(self.Position < len(self.Order) - 1):
            self.incPosition()
            sleep(self.walk())
            if(len(Theken[self.Order[self.Position]].Warteschlange) >= self.WarteschlangeMax[self.Position]):
                UserDoc.write(str(getTimer()) + ":" + str(self.Name) + " Dropped at " + Theken[self.Order[self.Position]].Name + "\n")
            else:
                UserDoc.write(str(getTimer()) + ":" + str(self.Name) + " Queueing at " + Theken[self.Order[self.Position]].Name + "\n")
                stationDoc.write(str(getTimer()) + ":" + Theken[self.Order[self.Position]].Name + " adding customer " + str(self.Name) + "\n")
                arrEv[self.Order[self.Position]].set() #wakes a station
                servEv = Event() #event gets triggered when the station is done with
                                 #with the customer
                Theken[self.Order[self.Position]].setListe(self.KaufeAnzahl[self.Position], servEv) #self.Position
                servEv.wait()
                UserDoc.write(str(getTimer()) + ":" + str(self.Name) + " Finished at " + Theken[self.Order[self.Position]].Name + "\n")
                stationDoc.write(str(getTimer()) + ":" + Theken[self.Order[self.Position]].Name + " finished customer " + str(self.Name) + "\n")

class KundeCreateA(Thread):
    TypInfoA = ([10/teiler, 30/teiler, 45/teiler, 60/teiler], [11, 11, 6, 21], [10, 5, 3, 30])
    
    def __init__(self):
        Thread.__init__(self)
        self.counter = 1
        
    def run(self):
        while(self.counter <= 10):
            u1 = User(self.TypInfoA, [0, 2, 1, 3], "A" + str(self.counter))
            u1.start()
            self.counter += 1
            sleep(200/teiler)
            
class KundeCreateB(Thread):
    TypInfoB = ([30/teiler, 30/teiler, 20/teiler], [6, 21, 21], [2, 3, 3])
    
    def __init__(self):
        Thread.__init__(self)
        self.counter = 1
        
    def run(self):
        sleep(1/teiler)
        while(self.counter < 30):
            u1 = User(self.TypInfoB, [2, 3 ,0],  "B" + str(self.counter))
            u1.start()
            self.counter += 1
            sleep(60/teiler)
            


class Ordering:
    def __init__(self, ):
        self.Prio = 1
    def __lt__(self, other):
        return True

def initKundeA():
    typ = KundeCreateA()
    typ.start()

def initKundeB():
    typ = KundeCreateB()
    typ.start()


class Supermarkt:

    def start(self):
        print("start")
        Theken[0].start()
        Theken[1].start()
        Theken[2].start()
        Theken[3].start()
        
        initKundeA()
        initKundeB()

a = Supermarkt()

StartZeit = time.time()
a.start()

eingabe = input("Ihre Eingabe? ")
print(eingabe)
UserDoc.close()
stationDoc.close()
supermarktDoc.close()