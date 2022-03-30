import itertools
from heapq import heappush, heappop
from typing import List, Any

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
        if(len(self.Warteschlange) == 1):
            self.bEmpty = 0
            self.Warteschlange.remove(Kunde.Name)
        elif(len(self.Warteschlange) > 1):
            self.Warteschlange.remove(Kunde.Name)

Theken = []
Theken.append(Station(10, [], "Bäcker"))
Theken.append(Station(60, [], "Käse"))
Theken.append(Station(30, [], "Wurst"))
Theken.append(Station(5, [], "Kasse"))


class Kunde:
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
        print(self.Name,self.Position, len(self.Laufen))
        return self.Laufen[self.Position]

    def getWarteschlangeMax(self):
        if(self.Position < self.anzahlDerEinkaeufe()):
            return self.WarteschlangeMax[self.Position]
        else:
            return -1

class Supermarkt:
    AnzahlDerKunden = 0
    Zeit = 0
    A = 200
    B = 60

    #TypInfo: 4xLaufweg, 4xMaxWarteschlabnge, 4xMengeArtikel.
    #Baecker, Kaese, Wurst, Kasse
    TypInfoA = ([10, 30, 45, 60], [11, 11, 6, 21], [10, 5, 3, 30])

    #TypInfo: 3xLaufweg, 3xMaxWarteschlabnge, 3xMengeArtikel.
    #Wurst, Kasse, Baecker
    TypInfoB = ([30, 30, 20], [6, 21, 21], [2, 3, 3])