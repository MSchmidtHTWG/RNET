import itertools
from heapq import heappush, heappop
from typing import List, Any



heap = []
counter = itertools.count()
UserDoc = open('supermarkt_customer.txt', 'w+') 
supermarktDoc = open('supermarkt.txt', 'w+') 
StationDoc = open('supermarkt_station.txt', 'w+')

class Station:

    def __init__(self, Dauer, Liste, name="leer", bEmpty = 0):
        self.Warteschlange = Liste
        self.Name = name
        self.bEmpty = bEmpty
        self.Dauer = Dauer

    def isEmpty(self):
        return self.bEmpty

    def add(self, Kunde):
        self.bEmpty = 1
        self.Warteschlange.append(Kunde.Name)


    def isMyTurn(self, Kundename):
        if(self.Warteschlange[0] == Kundename):
            return True
        return False

    def remove(self, Kunde):
        if(len(self.Warteschlange) == 1 and self.Warteschlange.count(Kunde.Name) > 0):
            self.bEmpty = 0
            self.Warteschlange.remove(Kunde.Name)
        elif(len(self.Warteschlange) > 1 and self.Warteschlange.count(Kunde.Name) > 0):
            self.Warteschlange.remove(Kunde.Name)

Theken = []
Theken.append(Station(10, [], "Bäcker"))
Theken.append(Station(60, [], "Käse"))
Theken.append(Station(30, [], "Metzger"))
Theken.append(Station(5, [], "Kasse"))
NamenNichtVollstaendigBedienterKunden = []
StartZeiten = []
EndZeiten = []
BaeckerKunden = 0
MetzgerKunden = 0
KaeseKunden = 0
KasseKunden = 0
BaeckerKundenDropp = 0
MetzgerKundenDropp = 0
KaeseKundenDropp = 0
KasseKundenDropp = 0


class User:
    def __init__(self, TypInformation, Name = ""):
        self.Name = Name
        self.Position = -1
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
        #print(self.Name,self.Position, self.Laufen[self.Position])
        return self.Laufen[self.Position]

    def getWarteschlangeMax(self):
        if(self.Position < self.anzahlDerEinkaeufe()):
            return self.WarteschlangeMax[self.Position]
        else:
            return -1


class Ordering:
    def __init__(self, ):
        self.Prio = 1
    def __lt__(self, other):
        return True



class Supermarkt:
    Zeit = 0
    A = 200
    B = 60

    #TypInfo: 4xLaufweg, 4xMaxWarteschlabnge, 4xMengeArtikel.
    #Baecker, Kaese, Wurst, Kasse
    TypInfoA = ([10, 30, 45, 60], [11, 11, 6, 21], [10, 5, 3, 30])

    #TypInfo: 3xLaufweg, 3xMaxWarteschlabnge, 3xMengeArtikel.
    #Wurst, Kasse, Baecker
    TypInfoB = ([30, 30, 20], [6, 21, 21], [2, 3, 3])

    def start(self):
        UserA1 = User(self.TypInfoA, "A1")
        UserB1 = User(self.TypInfoB, "B1")
        UserA2 = User(self.TypInfoA, "A2")
        UserB2 = User(self.TypInfoB, "B2")
        UserA3 = User(self.TypInfoA, "A3")
        UserB3 = User(self.TypInfoB, "B3")
        UserA4 = User(self.TypInfoA, "A4")
        UserB4 = User(self.TypInfoB, "B4")
        UserA5 = User(self.TypInfoA, "A5")
        UserB5 = User(self.TypInfoB, "B5")

        UserA6 = User(self.TypInfoA, "A6")
        UserB6 = User(self.TypInfoB, "B6")
        UserA7 = User(self.TypInfoA, "A7")
        UserB7 = User(self.TypInfoB, "B7")
        UserA8 = User(self.TypInfoA, "A8")
        UserB8 = User(self.TypInfoB, "B8")
        UserA9 = User(self.TypInfoA, "A9")
        UserB9 = User(self.TypInfoB, "B9")
        UserA10 = User(self.TypInfoA, "A10")
        UserB10 = User(self.TypInfoB, "B10")

        UserB11 = User(self.TypInfoB, "B11")
        UserB12 = User(self.TypInfoB, "B12")
        UserB13 = User(self.TypInfoB, "B13")
        UserB14 = User(self.TypInfoB, "B14")
        UserB15 = User(self.TypInfoB, "B15")
        UserB16 = User(self.TypInfoB, "B16")
        UserB17 = User(self.TypInfoB, "B17")
        UserB18 = User(self.TypInfoB, "B18")
        UserB19 = User(self.TypInfoB, "B19")
        UserB20 = User(self.TypInfoB, "B20")

        UserB21 = User(self.TypInfoB, "B21")
        UserB22 = User(self.TypInfoB, "B22")
        UserB23 = User(self.TypInfoB, "B23")
        UserB24 = User(self.TypInfoB, "B24")
        UserB25 = User(self.TypInfoB, "B25")
        UserB26 = User(self.TypInfoB, "B26")
        UserB27 = User(self.TypInfoB, "B27")
        UserB28 = User(self.TypInfoB, "B28")
        UserB29 = User(self.TypInfoB, "B29")
        UserB30 = User(self.TypInfoB, "B30")

        add_Task(0, UserA1, walk, [0, 2, 1, 3])
        add_Task(200, UserA2, walk, [0, 2, 1, 3])
        add_Task(400, UserA3, walk, [0, 2, 1, 3])
        add_Task(600, UserA4, walk, [0, 2, 1, 3])
        add_Task(800, UserA5, walk, [0, 2, 1, 3])
        add_Task(1000, UserA6, walk, [0, 2, 1, 3])
        add_Task(1200, UserA7, walk, [0, 2, 1, 3])
        add_Task(1400, UserA8, walk, [0, 2, 1, 3])
        add_Task(1600, UserA9, walk, [0, 2, 1, 3])
        add_Task(1800, UserA10, walk, [0, 2, 1, 3])

        add_Task(1, UserB1, walk, [2, 3, 0])
        add_Task(61, UserB2, walk, [2, 3, 0])
        add_Task(121, UserB3, walk, [2, 3, 0])
        add_Task(181, UserB4, walk, [2, 3, 0])
        add_Task(241, UserB5, walk, [2, 3, 0])
        add_Task(301, UserB6, walk, [2, 3, 0])
        add_Task(361, UserB7, walk, [2, 3, 0])
        add_Task(421, UserB8, walk, [2, 3, 0])
        add_Task(481, UserB9, walk, [2, 3, 0])
        add_Task(541, UserB10, walk, [2, 3, 0])
        add_Task(601, UserB11, walk, [2, 3, 0])
        add_Task(661, UserB12, walk, [2, 3, 0])
        add_Task(721, UserB13, walk, [2, 3, 0])
        add_Task(781, UserB14, walk, [2, 3, 0])
        add_Task(841, UserB15, walk, [2, 3, 0])
        add_Task(901, UserB16, walk, [2, 3, 0])
        add_Task(961, UserB17, walk, [2, 3, 0])
        add_Task(1021, UserB18, walk, [2, 3, 0])
        add_Task(1081, UserB19, walk, [2, 3, 0])
        add_Task(1141, UserB20, walk, [2, 3, 0])
        add_Task(1201, UserB21, walk, [2, 3, 0])
        add_Task(1261, UserB22, walk, [2, 3, 0])
        add_Task(1321, UserB23, walk, [2, 3, 0])
        add_Task(1381, UserB24, walk, [2, 3, 0])
        add_Task(1441, UserB25, walk, [2, 3, 0])
        add_Task(1501, UserB26, walk, [2, 3, 0])
        add_Task(1561, UserB27, walk, [2, 3, 0])
        add_Task(1621, UserB28, walk, [2, 3, 0])
        add_Task(1681, UserB29, walk, [2, 3, 0])
        add_Task(1741, UserB30, walk, [2, 3, 0])
        
        StartZeiten.append(["A1", 0])
        StartZeiten.append(["A2", 200])
        StartZeiten.append(["A3", 400])
        StartZeiten.append(["A4", 600])
        StartZeiten.append(["A5", 800])
        StartZeiten.append(["A6", 1000])
        StartZeiten.append(["A7", 1200])
        StartZeiten.append(["A8", 1400])
        StartZeiten.append(["A9", 1600])
        StartZeiten.append(["A10", 1800])
        
        StartZeiten.append(["B1", 1])
        StartZeiten.append(["B2", 61])
        StartZeiten.append(["B3", 121])
        StartZeiten.append(["B4", 181])
        StartZeiten.append(["B5", 241])
        StartZeiten.append(["B6", 301])
        StartZeiten.append(["B7", 361])
        StartZeiten.append(["B8", 421])
        StartZeiten.append(["B9", 481])
        StartZeiten.append(["B10", 541])
        StartZeiten.append(["B11", 601])
        StartZeiten.append(["B12", 661])
        StartZeiten.append(["B13", 721])
        StartZeiten.append(["B14", 781])
        StartZeiten.append(["B15", 841])
        StartZeiten.append(["B16", 901])
        StartZeiten.append(["B17", 961])
        StartZeiten.append(["B18", 1021])
        StartZeiten.append(["B19", 1081])
        StartZeiten.append(["B20", 1141])
        StartZeiten.append(["B21", 1201])
        StartZeiten.append(["B22", 1261])
        StartZeiten.append(["B23", 1321])
        StartZeiten.append(["B24", 1381])
        StartZeiten.append(["B25", 1441])
        StartZeiten.append(["B26", 1501])
        StartZeiten.append(["B27", 1561])
        StartZeiten.append(["B28", 1621])
        StartZeiten.append(["B29", 1681])
        StartZeiten.append(["B30", 1741])

        self.EventHandler()

    def EventHandler(self):
        AnzahlDerKunden = 0
        while(heap):
            Zeit, Prio, count, Kunde, func, order = heappop(heap)
            
            tZeit, tfunc, msg = func(Kunde, order) #ruft walk/entry
            if(msg != ""):
                print(msg)
                if(',' in msg):
                    s1, s2 = msg.split(',', 1)
                    UserDoc.write(str(Zeit) + ":" + s1 + "\n")
                    if(',' in s2):
                        s3, s4 = s2.split(',', 1)
                        StationDoc.write(str(Zeit) + ":" + s3 + "\n")
                        if(s4 != ""):
                            StationDoc.write(str(Zeit) + ":" + s4 + "\n")
                    else:
                        StationDoc.write(str(Zeit) + ":" + s2 + "\n")
                else:
                    UserDoc.write(str(Zeit) + ":" + msg + "\n")
            if(tfunc != leave):
                Zeit = Zeit + tZeit
                add_Task(Zeit, Kunde, tfunc, order)
            else:
                AnzahlDerKunden = AnzahlDerKunden + 1
                EndZeiten.append([Kunde.Name, Zeit])
                leave()

        else:
            print("Simulationsende: " + str(Zeit) + "s", file=supermarktDoc)
            print("Anzahl Kunden: " + str(AnzahlDerKunden), file=supermarktDoc)
            print("Anzahl vollständige Einkäufe: " + str(AnzahlDerKunden - len(NamenNichtVollstaendigBedienterKunden)), file=supermarktDoc)
            print("Mittlere Einkaufsdauer: " + str(einkaufslaenge() / len(EndZeiten)) + "s", file=supermarktDoc)
            print("Drop percentage at Bäcker: " + str((BaeckerKundenDropp / BaeckerKunden) * 100), file=supermarktDoc)
            print("Drop percentage at Metzger: " + str((MetzgerKundenDropp / MetzgerKunden) * 100), file=supermarktDoc)
            print("Drop percentage at Käse: " + str((KaeseKundenDropp / KaeseKunden) * 100), file=supermarktDoc)
            print("Drop percentage at Kasse: " + str((KasseKundenDropp / KasseKunden) * 100), file=supermarktDoc)
            UserDoc.close()
            supermarktDoc.close()
            StationDoc.close()

def add_Task(Zeit, TypInfo, tfunc, order):
    count = next(counter)
    Prio = 3
    if(tfunc == walk):
        Prio = 0
    elif(tfunc == entry):
        Prio = 2
    else:
        Prio = 1
    eantry = [Zeit, Prio, count, TypInfo, tfunc, order]
    heappush(heap, eantry)


def walk(Kunde, order):
    msg= ""
    if(Kunde.getPosition() != -1):
        msg = (Kunde.Name + " Finished at " + Theken[order[Kunde.getPosition()]].Name + "," + Theken[order[Kunde.getPosition()]].Name + " finished customer " + Kunde.Name)
        Theken[order[Kunde.getPosition()]].remove(Kunde)
    Kunde.incPosition()
    return Kunde.walk(), entry, msg

def wait(Kunde, order):
    if(Theken[order[Kunde.getPosition()]].isMyTurn(Kunde.Name)):
        zeit, func, msg = service(Kunde, order)
        return zeit, func, msg
    else:
        return 1, wait, ""

def entry(Kunde, order):
    global BaeckerKunden
    global KaeseKunden
    global MetzgerKunden
    global KasseKunden
    global BaeckerKundenDropp
    global KaeseKundenDropp
    global MetzgerKundenDropp
    global KasseKundenDropp
    if(Theken[order[Kunde.getPosition()]].Name == "Bäcker"):
        BaeckerKunden = BaeckerKunden + 1
    elif(Theken[order[Kunde.getPosition()]].Name == "Käse"):
        KaeseKunden = KaeseKunden + 1
    elif(Theken[order[Kunde.getPosition()]].Name == "Metzger"):
        MetzgerKunden = MetzgerKunden + 1
    else:
        KasseKunden = KasseKunden + 1
    if(Kunde.getWarteschlangeMax() > len(Theken[order[Kunde.getPosition()]].Warteschlange)): #überprüft länge der warteschlange
        msg = (Kunde.Name + " Queueing at " + Theken[order[Kunde.getPosition()]].Name + "," + Theken[order[Kunde.getPosition()]].Name + " adding customer " + Kunde.Name)
        if(Theken[order[Kunde.getPosition()]].bEmpty == 0): # keine warteschlange
             Theken[order[Kunde.getPosition()]].add(Kunde)
             zeit,func,msgtmp = service(Kunde, order)
             return (zeit, func, msg + "," + msgtmp)
        else:                                               # hinten anstellen
            Theken[order[Kunde.getPosition()]].add(Kunde)
            zeit,func,msgtmp = wait(Kunde, order)
            return (zeit, func, msg + "," + msgtmp)
    else:
        msg = (Kunde.Name + " Dropped at " + Theken[order[Kunde.getPosition()]].Name)
        if(Theken[order[Kunde.getPosition()]].Name == "Bäcker"):
            BaeckerKundenDropp = BaeckerKundenDropp + 1
        elif(Theken[order[Kunde.getPosition()]].Name == "Käse"):
            KaeseKundenDropp = KaeseKundenDropp + 1
        elif(Theken[order[Kunde.getPosition()]].Name == "Metzger"):
            MetzgerKundenDropp = MetzgerKundenDropp + 1
        else:
            KasseKundenDropp = KasseKundenDropp + 1
        if Kunde.Name not in NamenNichtVollstaendigBedienterKunden:
            NamenNichtVollstaendigBedienterKunden.append(Kunde.Name)
        zeit, func, msgtmp = walk(Kunde, order)
        return (zeit, func, msg)

def end(Kunde, order):
    msg = (Kunde.Name + " Finished at " + Theken[order[Kunde.getPosition()]].Name + "," + Theken[order[Kunde.getPosition()]].Name + " finished customer " + Kunde.Name)
    Theken[order[Kunde.getPosition()]].remove(Kunde)
    return 9999, leave, msg

def leave():
    return 0

def service(Kunde, order):
    if((Kunde.anzahlDerEinkaeufe() - 1) == Kunde.getPosition()):
        return Theken[order[Kunde.getPosition()]].Dauer * Kunde.KaufeAnzahl[Kunde.getPosition()], end, ""
    else:
        tmp = Theken[order[Kunde.getPosition()]].Dauer * Kunde.KaufeAnzahl[Kunde.getPosition()]
        return tmp, walk, "" + Theken[order[Kunde.getPosition()]].Name + " serving customer " + Kunde.Name

def einkaufslaenge():
    laenge = 0
    for x in StartZeiten:
        for y in EndZeiten:
            if x[0] == y[0]:
                laenge = (y[1] - x[1]) + laenge
    return laenge

a = Supermarkt()
a.start()
