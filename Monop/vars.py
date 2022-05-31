from tools import deepcopy, randItem

""" Cases """
# Creation
def createCase(name, tpe, datas={}):
    assert type(name) == type(tpe) == str
    if(datas): assert type(datas) == dict
    return {"name": name, "type": tpe, "data": datas}
def createProperty(name, cost, group=None, allowConstructions= True, more_datas= {}):
    d = {"money": cost, "group": group if group else None, "houses": 0, "hotels": 0, "allowConstructions": allowConstructions}
    for k in more_datas.keys(): d[k] = more_datas[k]
    return createCase(name, "property", d)
def createPacket(packet_type):
    assert packet_type == "community" or packet_type == "luck", "packet_type must be \"community\" or \"luck\""
    return createCase("Chance" if packet_type == "luck" else "Caisse de Communaute", "packet", {"type": packet_type})
# Get
def findCase(fct):
    for i in range(len(gameDatas["plate"])): 
        obj= gameDatas["plate"][i].copy()
        if fct(obj):
            obj["index"]= i
            return obj

""" Players """
# Creation
def createPlayer(name, icon=" "):
    playerObject = {"name": name, "icon": icon, "cards": [], "money": gameDatas["settings"]["money"]["init"], "case": 0, "prison": 0}
    return playerObject
# Get
def findPlayer(fct):
    for i in range(len(gameDatas["players"])): 
        obj= gameDatas["players"][i].copy()
        obj["index"] = i
        if fct(obj):
            return obj
def calcMoney(playerIndex):
    total= 0
    for infos in gameDatas["players"][playerIndex]["money"]:
        total+= infos["value"] * infos["count"]
    return total
def calcTotalActions(playerDatas):
    propsValue = 0
    for c in playerDatas["cards"]: propsValue+= calcCardValue(c, 0)
    return calcMoney(gameDatas["players"].index(playerDatas)) + propsValue
def moneyStr(money):
    return str(money) + gameDatas["settings"]["money"]["symbol"]
# Set
def setMoney(playerIndex, value):
    gameDatas["players"][playerIndex]["money"] = getMoneyPack(value)
    return value
def addMoney(playerIndex, value):
    total = calcMoney(playerIndex) + value
    return setMoney(playerIndex, total)
""" Cards """
# Get
def findCard(fct, pInd = None):
    pack = gameDatas["cards"] if pInd == None else gameDatas["players"][pInd]["cards"]
    for card in pack:
        if fct(card): return card
def filterCards(fct, pInd = None):
    pack = gameDatas["cards"] if pInd == None else gameDatas["players"][pInd]["cards"]
    l=[]
    for card in pack:
        if fct(card): l.append(card)
    return l
def initCard(case):
    case["active"]= True
    return case
def calcCardValue(card, pInd):
    buildDatas = gameDatas["settings"]["constructions"]
    value = card["data"]["money"] + gameDatas["settings"]["propertiesCost"]
    group = card["data"].get("grouped")
    def f(c): return c["data"].get("grouped") == group
    playerHas = len(filterCards(f, pInd))
    if card["data"].get("calcValueBy") == "count": return value * playerHas
    if card["data"].get("calcValueBy") == "dice" and card["data"].get("multiplicator"): return card["data"]["multiplicator"] * (gameDatas["temp"].get("dice") or 1)
    if len(filterCards(f)) == playerHas: value*= 2
    houses = card["data"]["houses"]
    hotels = card["data"]["hotels"]
    rent = card["data"].get("rent")
    house_rent = rent["houses"] if rent else buildDatas["houses"]["rent"]
    hotels_rent = rent["hotels"] if rent else buildDatas["hotels"]["rent"]
    if houses == hotels == 0: return value
    if not(buildDatas["settings"]["accumulatePrices"]):
        hsesp = value * (house_rent[houses] if houses < len(house_rent) else house_rent[-1])
        htlsp= value * (hotels_rent[hotels] if hotels < len(hotels_rent) else hotels_rent[-1])
        if buildDatas["settings"]["priceOfHousesAndHotels"]: return htlsp + hsesp
        elif hotels: return htlsp
        elif houses: return hsesp
    hsesp = 0
    for i in range(houses): price+= value * (house_rent[i] if i < len(house_rent) else house_rent[-1])
    htlsp = 0
    for i in range(hotels): price+= value * (hotels_rent[i] if i < len(hotels_rent) else hotels_rent[-1])
    if buildDatas["settings"]["priceOfHousesAndHotels"]: return htlsp + hsesp
    elif hotels: return htlsp
    elif houses: return hsesp
    return 0
def calcMortgaging(card,pInd):
    return calcCardValue(card,pInd) + (card["data"]["mortgage"] if card["data"].get("mortgage") else gameDatas["settings"]["mortgageValue"])
# Set
def addCardToPlayer(playerIndex, cardName):
    try:
        def f(c):
            return c["name"] == cardName
        cardIndex = gameDatas["cards"].index(findCard(f))
    except: return False
    gameDatas["players"][playerIndex]["cards"].append(initCard(gameDatas["cards"][cardIndex]))
    gameDatas["cards"][cardIndex]["bought"] = True
    return len(gameDatas["players"][playerIndex]["cards"]) - 1

""" Packets """
# Creation
def createPacketCard(title, description, datas):
    return {"title": title, "description": description, "data": datas}
def createPackets():
    return {
        "luck": [
            createPacketCard("Un imprevu...", "Retournez a la case depart et touchez " + moneyStr(100) + "!", {"give": 100, "move": {"to": {"type": "starting"}, "instant": True}}),
            createPacketCard("Instant boutiques!", "Dirigez-vous vers la rue de la paix!", {"move": {"to": {"index": -1}, "instant": False}}),
            createPacketCard("STOOOPPP!!", "Vous vous retrouver au mileu d'un troupeaux de personnes age! Reculez de 3 cases.", {"move": {"add": -3, "instant": True}}),
            createPacketCard("C'est votre anniversaire!", "Tous les joueurs vous donnes " + moneyStr(50) + "!", {"give": 50, "players": {"give": -50}})
        ],
        "community": [
            createPacketCard("Une ame charitable...", "Vous vous etes occupe de personnes ages et recevez donc " + moneyStr(20) + "!", {"give": 20}),
            createPacketCard("Foncez droit en prison!", "Hier, vos voisins se sont plein de la fete que vous avez organise.", {"move": {"to": {"type": "prison"}}}),
            createPacketCard("Le rouge et le noir.", "Pour reviser votre francais, vous achetez Le Rouge Et Le Noir qui coute " + moneyStr(10) + "!", {"give": -10}),
            createPacketCard("La science avant tout!", "Tout comme retour vers le future, nous revenons dans le passé: tout le monde recule de 3 cases!", {"move": {"add": -3, "instant": True}, "players": {"move": {"add": -3, "instant": True}}})
        ]
    }
# Get
def getRandomPacketCard(pack_type, gameDatas):
    if not(gameDatas["packets"][pack_type]): return None
    return randItem(gameDatas["packets"][pack_type])

""" Other """
def getMoneyPack(value):
    if value <= 0: return []
    pack= {}
    possiblePack = deepcopy(gameDatas["settings"]["money"]["values"])
    possiblePack.reverse()
    while value > 0:
        for possibleValue in possiblePack:
            if value % possibleValue == 0:
                if not(pack.get(possibleValue)): pack[possibleValue] = 0
                pack[possibleValue]+=1
                value-=possibleValue
                break
    finalPack = [{"value": k, "count": pack[k]} for k in sorted(list(pack.keys()))]
    return finalPack

""" Main variable """
gameDatas = None

initDatas = {
    "settings": {
        "players": [2, 10],
        "money": {
            "name": "Monop'",
            "symbol": "M",
            "values": [1, 5, 10, 20, 50, 100, 500],
            "init": [
                {"value": 1, "count": 5},
                {"value": 5, "count": 1},
                {"value": 10, "count": 2},
                {"value": 20, "count": 1},
                {"value": 50, "count": 1},
                {"value": 100, "count": 4},
                {"value": 500, "count": 2},
            ]
        },
        "constructions": {
            "houses": {
                "max": 4,
                "rent": [2, 5, 15, 25],
                "price": .5
            },
            "hotels": {
                "max": 1,
                "rent": [75],
                "price": 2
            },
            "settings": {
                "needAllCardsGroupBeforeBuilding": True,
                "needHousesBeforeHotels": True,
                "accumulatePrices": False,
                "priceOfHousesAndHotels": False
            }
        },
        "dice": [1, 6],
        "mortgageValue": -20,
        "propertiesCost": -50,
        "prisonTime": 3,
        "prisonCaseIndex": 10
    },
    "plate": [
        createCase("Case Depart", "starting", {"money": 200}),
        createProperty("Boulevard de Belleville", 60, "brown"),
        createPacket("community"),
        createProperty("Rue Lecourbe", 60, "brown"),
        createCase("Impot sur le revenu", "take", {"money": 200}),
        createProperty("Gare Montparnasse", 200, "train_station", False, {"calcValueBy": "count"}),
        createProperty("Rue de Vaugirard", 100,"light_blue"),
        createPacket("luck"),
        createProperty("Rue de Courcelles", 100, "light_blue"),
        createProperty("Avenue de la Republique", 120, "light_blue"),
        createCase("Visite Simple", "nothing"),
        createProperty("Boulevard de La Villette", 140, "pink"),
        createProperty("Compagnie de l'electricite", 150, "company", False, {"calcValueBy": "dice", "multiplicator": 15}),
        createProperty("Avenue de Neuilly", 140, "pink"),
        createProperty("Rue de Paradis", 160, "pink"),
        createProperty("Gare de Lyon", 200, "train_station", False, {"calcValueBy": "count"}),
        createProperty("Avenue Mozart", 180, "orange"),
        createPacket("community"),
        createProperty("Boulevard St-Michelle", 180, "orange"),
        createProperty("Place Pigalle", 200, "orange"),
        createCase("Parc gratuit", "nothing"),
        createProperty("Avenue Matignon", 220, "red"),
        createPacket("luck"),
        createProperty("Boulevard Malesherbes", 220, "red"),
        createProperty("Avenue Henri-Martin", 240, "red"),
        createProperty("Gare du Nord", 200, "train_station", False, {"calcValueBy": "count"}),
        createProperty("Faubourg St-Honore", 260, "yellow"),
        createProperty("Place de la bource", 260, "yellow"),
        createProperty("Compagnie des eaux", 150, "company", False, {"calcValueBy": "dice", "multiplicator": 10}),
        createProperty("Rue la Fayette", 280, "yellow"),
        createCase("Allez en prison", "prison"),
        createProperty("Avenue de Breteuil", 300, "green"),
        createProperty("Avenue Foch", 300, "green"),
        createPacket("community"),
        createProperty("Boulevard des Capucines", 320, "green"),
        createProperty("Gare St-Lazare", 200, "train_station", False, {"calcValueBy": "count"}),
        createPacket("luck"),
        createProperty("Avenue des Champs-Elysees", 350, "blue"),
        createCase("Taxe de luxe", "take", {"money": 100}),
        createProperty("Rue de la Paix", 400, "blue")
    ],
    "players": [],
    "cards": [],
    "temp": {}
}
def resetGameDatas():
    global gameDatas
    gameDatas = initDatas.copy()
    gameDatas["packets"] = createPackets()
    gameDatas["cards"] = [prop for prop in gameDatas["plate"] if prop.get("type") == "property"]
resetGameDatas()
