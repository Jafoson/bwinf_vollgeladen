import os, time

#Hotel Klasse, speichert die Attrituben von einem Hotel: Attribute = distance wie auch die Bewertung
class Hotel:
    def __init__(self, distance, rank):
        self.distance: int = int(distance)
        self.rank: float = float(rank)

    def __lt__(self, other):
        return self.rank < other

    def __gt__(self, other):
        return self.rank > other

#speichert eine Referenzliste, wie auch von der Referenzliste das Hotel mit der niedrigsten Bewertung.
class Result:
    def __init__(self,):
        self.hotels: list = []
        self.weakestHotel: float = float(0.0)

    def __lt__(self, other):
        return self.weakestHotel < other

    def __gt__(self, other):
        return self.weakestHotel > other

#liest denn vorgegebenen Input aus
# -> bevor die Information aus dem Input rausgenommen werden wird mit der funktion checkPathExist überprüft ob der Pfad exestiert.
def getInput():
    path = checkPathExist(input("Geben Sie den Pfad an, wo ihre Datei sich befindet: "))
    #path = "hotels7.txt"
    getInformation(checkPathExist(path))


def checkPathExist(path: str):
    if os.path.exists(path):
        return path
    else:
        print("Dieser Pfad existiert nicht, bitte geben sie ein gültigen Pfad ein.")
        getInput()


#die Informationen von der Text Datei werden eingelesen und eingeordnet
def getInformation(path: str):
    global hotels
    global goalDistance
    print(path)
    with open(path, "r") as rawInformation:
        contens = rawInformation.readlines()
        print(type(contens), contens)

    for i in contens[1:]:
        information = i.split(" ")
        if len(information) > 1:
            hotels.append(Hotel(information[0], information[1]))
            removeDuplication(hotels)
        else:
            checkPossibleDistance(int(information[0])) #checkt ob überhaupt die ZielDistance generell in denn 5 Tagen erreichbar ist.
            goalDistance = int(information[0])
    print("Hotelliste: ", hotels)
#Idenfizieren ob das letzte und das vorletzte Hotel die gleiche Distance haben, wenn ja wird das Hotel mit der besten Bewertung genommen.
def removeDuplication(hotels):
    try:
        if hotels[-1].distance == hotels[-2].distance:
            if hotels[-1].rank <= hotels[-2].rank:
                hotels.pop(-1)
            else:
                hotels.pop(-2)
    except IndexError:
        pass


def checkPossibleDistance(goalDistance: int):
    if goalDistance <= 1800:
        return
    else:
        print("Dieser Weg, ist mit den vorgegebenen Zielen, nicht erreichbar!")
        getInput()

#in der Hotelliste wird von dem entfernsteten Hotel bis zum nahsten Hotel geschaut und in Tagen eingeteilt.
#Es für jeden durchlauf ein neue Tagesliste erstellt, Es wird geschaut ob die Distance von Hotel kleiner als die minimale erreichbare Distanz ist,
#Wenn ja wird sie in der Tagesliste eingeführt am Ende werden die Tageslisten in einer zusammengefasste Tagesliste eingepeichert
def declarationDays():
    global hotels
    global goalDistance
    days: list = []
    dayDistance = goalDistance
    hotels.reverse()
    for i in range(4):
        oneDay: list = []
        dayDistance -= 360 #für jeden schleifendurchlauf(ein durchlauf = ein Tag) wird die mindeste erreichbare Tagesdistance berechnet
        for y in hotels:
            if int(y.distance) >= dayDistance: #Untersuchung ob das Hotel größer ist als die mindest erreichbate Distance ist
                oneDay.append(y)
            else:
                break
        #Hotels welche in einem Tag drinne sind werden von der Hotelsliste entfernt
        for z in oneDay:
            hotels.remove(z)
        days.append(oneDay)
        """for z in oneDay:
            print(z, " ", end="")
        print()"""
    declarationHotelDay(days)

#verschachtete Tagesliste werden vertauscht, es fängt von Tag 1(index = 0) bis maximal Tag4(index = 3) am Ende an.
def declarationHotelDay(days: []):
    global goalDistance
    days.reverse()
    for i in days:
        i.reverse()
    result: Result = declarationday1to42(days, Result())
    evaluation(result)


#durchsuchung von denn Hotels und ob der niedrigste Rank von Result(ausgewählte Hotel von Tagen zusammengefasst) am höchsten ist.
def declarationday1to42(days: list, result: Result, goalDistance: int = 360, possibelWay: list=[], day= 0):
    #schleifen durchlauf von einen Tag wo bei jedem durchlauf ein Hotel genommen wird von dem Tag, beginn von nahsten Hotel bis entferntesten Hotel
    for hotel in days[day]:
        #überprüfung ob die Hotel Distance kleiner odr = der maximalen erreichbaren Distance diesen Tages ist und ob überhaupt die bewertung höher ist als von dem schwächsten Hotel, von der Referenzliste.
        #Wenn nicht wird ein neuer Durchlauf stattfinden.
        if hotel.distance <= goalDistance and result.weakestHotel <= hotel.rank:
                #es wird geschaut ob es der letzte Tag ist, wenn ja wird das Hotel in der seperaten referenzliste gespeichert und diese Liste wird als Referenzliste gespeichert
                #und das schlecht Bewerteste Hotel wird herausgefunden, am ende wird geschaut für die weiteren Hotels diesen Tages ob sie eine bessere Bewertung besitzen.
                if day == 3:
                    possibelWay.append(hotel)
                    result.hotels = possibelWay[:]
                    result.weakestHotel = min(possibelWay).rank
                    possibelWay.pop(day)
                #Wenn es irgendein Hotel ist werden sie eingefügt in der seperatenreferenzliste, und die funktion wird erneut aufgerufen mit dem nächsten Tag.
                else:
                    possibelWay.append(hotel)
                    declarationday1to42(days, result, hotel.distance + 360, possibelWay, day + 1)
                    possibelWay.pop(-1)
    return result

#Ausgabe
def evaluation(result: Result):
    for i in range(4):
        print(f"Tag {i+1}: {result.hotels[i].distance} mit einem Rank von {result.hotels[i].rank}")

if __name__ == "__main__":
    hotels = []
    goalDistance = 0

    starttime = time.time()
    getInput()

    declarationDays()
    endtime = time.time() - starttime
    print(endtime)