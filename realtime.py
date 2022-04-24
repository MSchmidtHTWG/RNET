import itertools
from threading import Thread
from threading import Event
from threading import Lock
import time
from time import sleep


heap = []  #Zeitpunkt, Prio, Nr, Funktion
counter = itertools.count()

teiler = 1000

# Output Text Declare
UserDoc = open('supermarkt_customer.txt', 'w+') 
stationDoc = open('supermarkt_station.txt', 'w+') 
supermarktDoc = open('supermarkt.txt', 'w+') 
writeLock = Lock()


def getTimer():
    return (time.time() - StartZeit) * teiler

class Station(Thread):

    def __init__(self, Dauer, Liste, name="leer", nummer=0, stopEv=Event()):
        Thread.__init__(self)
        self.Warteschlange = Liste
        self.Name = name
        self.nummer = nummer
        self.Dauer = Dauer
        self.WarteschlangeLock = Lock()
        self.stopEv = stopEv

    def setListe(self, amount, Event, Name):
        self.WarteschlangeLock.acquire()
        self.Warteschlange.append([Name, Event, amount])
        self.WarteschlangeLock.release()
        
    def run(self):
        while(not self.stopEv.is_set()):
            arrEv[self.nummer].wait()
            if(arrEv[self.nummer].is_set()):
                while(len(self.Warteschlange) > 0):
                    self.WarteschlangeLock.acquire()
                    username, serveEv, servings = self.Warteschlange.pop()
                    self.WarteschlangeLock.release()
                    writeLock.acquire()
                    stationDoc.write(str(getTimer()) + ":" + str(self.Name) + " serving customer " + str(username) + "\n")
                    writeLock.release()
                    sleep(servings * self.Dauer)
                    serveEv.set()
                arrEv[self.nummer].clear()


arrEv = []
arrEv.append(Event()) 
arrEv.append(Event())      
arrEv.append(Event()) 
arrEv.append(Event())
arrEvLock = Lock()

stopEv = Event()
Theken = []
# Theke[0] = Baecker, [1] = kaese, [2] = Wurst, [3] = kasse
Theken.append(Station(10/teiler, [], "Bäcker", 0, stopEv))
Theken.append(Station(60/teiler, [], "Käse", 1, stopEv))
Theken.append(Station(30/teiler, [], "Metzger", 2, stopEv))
Theken.append(Station(5/teiler, [], "Kasse", 3, stopEv))
AnzahlDerKunden = 0
AnzahlderKundenLock = Lock()
NamenNichtVollstaendigBedienterKunden = []
NamenNichtVollstaendigBedienterKundenLock = Lock()
StartZeiten = []
StartZeitenLock = Lock()
EndZeiten = []
EndZeitenLock = Lock()
BaeckerKunden = 0
BaeckerKundenLock = Lock()
MetzgerKunden = 0
MetzgerKundenLock = Lock()
KaeseKunden = 0
KaeseKundenLock = Lock()
KasseKunden = 0
KasseKundenLock = Lock()
BaeckerKundenDropp = 0
BaeckerKundenDroppLock = Lock()
MetzgerKundenDropp = 0
MetzgerKundenDroppLock = Lock()
KaeseKundenDropp = 0
KaeseKundenDroppLock = Lock()
KasseKundenDropp = 0
KasseKundenDroppLock = Lock()



class User(Thread):
    def __init__(self, TypInformation, order, Name = ""):
        Thread.__init__(self)
        self.Name = Name
        self.Position = -1
        self.Order = order
        self.Laufen = TypInformation[0]
        self.WarteschlangeMax = TypInformation[1]
        self.KaufeAnzahl = TypInformation[2]
        self.servEv = Event()

    def incPosition(self):
        self.Position += 1

    def walk(self):
        return self.Laufen[self.Position]
            
    def run(self): 
        global AnzahlDerKunden
        global BaeckerKunden
        global KaeseKunden
        global MetzgerKunden
        global KasseKunden
        global BaeckerKundenDropp
        global KaeseKundenDropp
        global MetzgerKundenDropp
        global KasseKundenDropp
        while(self.Position < len(self.Order) - 1):
            self.incPosition()
            sleep(self.walk())
            if(Theken[self.Order[self.Position]].Name == "Bäcker"):
                BaeckerKundenLock.acquire()
                print(self.Name + " am Bäcker")
                BaeckerKunden = BaeckerKunden + 1
                BaeckerKundenLock.release()
            elif(Theken[self.Order[self.Position]].Name == "Käse"):
                KaeseKundenLock.acquire()
                print(self.Name + " am Käse")
                KaeseKunden = KaeseKunden + 1
                KaeseKundenLock.release()
            elif(Theken[self.Order[self.Position]].Name == "Metzger"):
                MetzgerKundenLock.acquire()
                print(self.Name + " am Metzger")
                MetzgerKunden = MetzgerKunden + 1
                MetzgerKundenLock.release()
            else:
                KasseKundenLock.acquire()
                print(self.Name + " am Kasse")
                KasseKunden = KasseKunden + 1
                KasseKundenLock.release()
            if(len(Theken[self.Order[self.Position]].Warteschlange) >= self.WarteschlangeMax[self.Position]):
                writeLock.acquire()
                UserDoc.write(str(getTimer()) + ":" + str(self.Name) + " Dropped at " + Theken[self.Order[self.Position]].Name + "\n")
                writeLock.release()
                if(Theken[self.Order[self.Position]].Name == "Bäcker"):
                    BaeckerKundenDroppLock.acquire()
                    BaeckerKundenDropp = BaeckerKundenDropp + 1
                    BaeckerKundenDroppLock.release()
                elif(Theken[self.Order[self.Position]].Name == "Käse"):
                    KaeseKundenDroppLock.acquire()
                    KaeseKundenDropp = KaeseKundenDropp + 1
                    KaeseKundenDroppLock.release()
                elif(Theken[self.Order[self.Position]].Name == "Metzger"):
                    MetzgerKundenDroppLock.acquire()
                    MetzgerKundenDropp = MetzgerKundenDropp + 1
                    MetzgerKundenDroppLock.release()
                else:
                    KasseKundenDroppLock.acquire()
                    KasseKundenDropp = KasseKundenDropp + 1
                    KasseKundenDroppLock.release()
                NamenNichtVollstaendigBedienterKundenLock.acquire()
                if self.Name not in NamenNichtVollstaendigBedienterKunden:
                    NamenNichtVollstaendigBedienterKunden.append(self.Name)
                NamenNichtVollstaendigBedienterKundenLock.release()
            else:
                writeLock.acquire()
                UserDoc.write(str(getTimer()) + ":" + str(self.Name) + " Queueing at " + Theken[self.Order[self.Position]].Name + "\n")
                stationDoc.write(str(getTimer()) + ":" + Theken[self.Order[self.Position]].Name + " adding customer " + str(self.Name) + "\n")
                writeLock.release()
                arrEvLock.acquire()
                arrEv[self.Order[self.Position]].set()
                arrEvLock.release()
                Theken[self.Order[self.Position]].setListe(self.KaufeAnzahl[self.Position], self.servEv, self.Name) #self.Position
                self.servEv.wait()
                writeLock.acquire()
                UserDoc.write(str(getTimer()) + ":" + str(self.Name) + " Finished at " + Theken[self.Order[self.Position]].Name + "\n")
                stationDoc.write(str(getTimer()) + ":" + Theken[self.Order[self.Position]].Name + " finished customer " + str(self.Name) + "\n")
                writeLock.release()
        else:
            EndZeitenLock.acquire()
            EndZeiten.append([self.Name, getTimer()])
            EndZeitenLock.release()
            AnzahlderKundenLock.acquire()
            AnzahlDerKunden = AnzahlDerKunden + 1
            print("Ein User verlässt den Supermarkt! " + str(AnzahlDerKunden))
            if(AnzahlDerKunden == 40):
                print("Simulationsende: " + str(getTimer()) + "s", file=supermarktDoc)
                print("Anzahl Kunden: " + str(AnzahlDerKunden), file=supermarktDoc)
                print("Anzahl vollständige Einkäufe: " + str(AnzahlDerKunden - len(NamenNichtVollstaendigBedienterKunden)), file=supermarktDoc)
                print("Mittlere Einkaufsdauer: " + str(einkaufslaenge() / len(EndZeiten)) + "s", file=supermarktDoc)
                print("Drop percentage at Bäcker: " + str((BaeckerKundenDropp / BaeckerKunden) * 100), file=supermarktDoc)
                print("Drop percentage at Metzger: " + str((MetzgerKundenDropp / MetzgerKunden) * 100), file=supermarktDoc)
                print("Drop percentage at Käse: " + str((KaeseKundenDropp / KaeseKunden) * 100), file=supermarktDoc)
                print("Drop percentage at Kasse: " + str((KasseKundenDropp / KasseKunden) * 100), file=supermarktDoc)
                stopEv.set()
                UserDoc.close()
                supermarktDoc.close()
                stationDoc.close()
            AnzahlderKundenLock.release()
            

class KundeCreateA(Thread):
    TypInfoA = ([10/teiler, 30/teiler, 45/teiler, 60/teiler], [11, 11, 6, 21], [10, 5, 3, 30])
    
    def __init__(self):
        Thread.__init__(self)
        self.counter = 1
        
    def run(self):
        while(self.counter <= 10):
            u1 = User(self.TypInfoA, [0, 2, 1, 3], "A" + str(self.counter))
            u1.start()
            StartZeitenLock.acquire()
            StartZeiten.append(["A" + str(self.counter), getTimer()])
            StartZeitenLock.release()
            self.counter += 1
            sleep(200/teiler)
            
class KundeCreateB(Thread):
    TypInfoB = ([30/teiler, 30/teiler, 20/teiler], [6, 21, 21], [2, 3, 3])
    
    def __init__(self):
        Thread.__init__(self)
        self.counter = 1
        
    def run(self):
        sleep(1/teiler)
        while(self.counter <= 30):
            u1 = User(self.TypInfoB, [2, 3 ,0],  "B" + str(self.counter))
            u1.start()
            StartZeitenLock.acquire()
            StartZeiten.append(["B" + str(self.counter), getTimer()])
            StartZeitenLock.release()
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
    
def einkaufslaenge():
    laenge = 0
    for x in StartZeiten:
        for y in EndZeiten:
            if x[0] == y[0]:
                laenge = (y[1] - x[1]) + laenge
    return laenge


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
