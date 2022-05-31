from tools import *
from vars import *
def switchPlayer():
    if gameDatas["temp"].get("currentPlayerIndex") == None: gameDatas["temp"]["currentPlayerIndex"] = 0
    else:
        gameDatas["temp"]["currentPlayerIndex"] += 1
        if gameDatas["temp"]["currentPlayerIndex"] >= len(gameDatas["players"]):
            gameDatas["temp"]["currentPlayerIndex"] = 0
    return gameDatas["temp"]["currentPlayerIndex"]
def move(nb, playerIndex):
    allCases = []
    for i in range(nb):
        gameDatas["players"][playerIndex]["case"]+= 1
        if gameDatas["players"][playerIndex]["case"] >= len(gameDatas["plate"]): gameDatas["players"][playerIndex]["case"] = 0
        allCases.append(gameDatas["plate"][gameDatas["players"][playerIndex]["case"]])
    return allCases
def game_end():
    winner = gameDatas["players"][0] if not(len(gameDatas["players"])) else sorted(gameDatas["players"], key= calcTotalActions, reverse=True)[0]
    dialog(ast(centerTxt(winner["name"] + " vient de gagner la partie avec une fortune de " + moneyStr(calcMoney(0)) + "!")))
    propsValue = sum([calcCardValue(c, 0) for c in winner["cards"]])
    dialog(ast(centerTxt("Avec " + str(len(winner["cards"])) + " propriete pour une valeur totale de " + moneyStr(propsValue) + "!")))
    return restart()
def game(players):
    i = players
    while i > 0:
        clear()
        name= input("Nom du joueur #" + str(players - i + 1) + ":\n>>> ")
        def same_name(p):
            return p["name"] == name
        if not(name) or findPlayer(same_name):
            dialog(ast("Nom de joueur invalide ou deja utilise!"))
            continue
        clear()
        pion= input("Pion du joueur #" + str(players - i + 1) + ":\n>>> ")
        if len(pion) != 1:
            dialog(ast("Le pion ne doit etre qu'un seul charactere!"))
            continue
        gameDatas["players"].append(createPlayer(name, pion))
        i-=1
    def chooseMoney(value):
        global actualValue, groupedMoney
        actualValue, groupedMoney = 0, {}
        def confirm(nb):
            global actualValue, groupedMoney
            actualValue+= nb
            if not(groupedMoney.get(nb)): groupedMoney[nb] = 1
            else: groupedMoney[nb]+= 1
        while actualValue != value:
            rest = value - actualValue
            possibleValues = [nb for nb in gameDatas["settings"]["money"]["values"] if rest%nb == 0]
            if not(len(possibleValues)):
                dialog(ast("Impossible de faire de diviser " + moneyStr(rest) + " en d'autres valeurs du jeu!"))
                return False
            action = menu([moneyStr(nb) + " (" + str((groupedMoney[nb] if groupedMoney.get(nb) else 0)) + ")" for nb in possibleValues], ast(moneyStr(actualValue) + "/" + moneyStr(value) + ":"))
            if action == None: return None
            confirm(possibleValues[action])
        return groupedMoney
    def moneys(pInd):
        total= calcMoney(pInd)
        data = [moneyStr(info["value"]) + " (" + str(info["count"]) + ")" for info in gameDatas["players"][pInd]["money"]]
        action = menu(data, ast("Voici tes economies (" + moneyStr(total) + "):"))
        if action == None: return
        moneyDatas = gameDatas["players"][pInd]["money"]
        m = chooseMoney(moneyDatas[action]["value"] * moneyDatas[action]["count"])
        if m:
            del moneyDatas[action]
            mDict = {d.get("value"): d.get('count') for d in moneyDatas}
            for value in m.keys():
                if mDict.get(value): mDict[value]+= m[value]
                else: mDict[value] = 1
            moneyDatas = [{"value": k, "count": mDict[k]} for k in sorted(list(mDict.keys()))]
            gameDatas["players"][pInd]["money"] = moneyDatas.copy()
        elif m == False: dialog(ast("Nous ne pouvons actuellement pas faire ce genre d'echange."))
        return moneys(pInd)
    def mortgage(pInd, propertyInd):
        if not(menu(["Non", "Oui"], ast("Etes-vous sur de vouloir hypothequer ce bien ?"))): return
        prop = gameDatas["players"][pInd]["cards"][propertyInd]
        prop["active"] = False
        addMoney(pInd, calcMortgaging(prop, pInd))
        dialog(ast("Action effectue!"))
        return True
    def builds(pInd, propertyInd):
        if not(gameDatas["temp"].get("constructions")): return dialog(ast(centerTxt("Les constructions sont pour le moment desactive!")))
        buildSettings = gameDatas["settings"]["constructions"]
        prop = gameDatas["players"][pInd]["cards"][propertyInd]
        def f(c): return c["data"].get("group") == prop["data"].get("group")
        if buildSettings["settings"]["needAllCardsGroupBeforeBuilding"] and len(filterCards(f)) != len(filterCards(f, pInd)): return dialog(ast("Vous devez posseder toute les cartes " + prop["data"].get("group") + " avant de pouvoir contruire!"))
        houses, hotels = prop["data"]["houses"], prop["data"]["hotels"]
        if houses >= buildSettings["houses"]["max"] and hotels >= buildSettings["hotels"]["max"]: return dialog(ast("Cette propriete a ete completement construite!"))
        buyType = 0 | (houses >= buildSettings["houses"]["max"])
        if buyType == 0 and buildSettings["settings"]["needHousesBeforeHotels"] == False:
            buyType = menu(["Maisons", "Hotels"], ast("Que souhaitez-vous construire ?"))
            if buyType == None: return
        key = "houses" if buyType==0 else "hotels"
        maxBought = buildSettings[key]["max"] - [houses, hotels][buyType]
        price = buildSettings[key]["price"]
        playerMoney = calcMoney(pInd)
        nbs = list(range(1, maxBought + 1))
        item = menu([str(nb) + " (" + moneyStr(prop["data"]["money"] * nb * price) + ")" for nb in nbs if prop["data"]["money"] * nb * price <= playerMoney], ast("Combien veux-tu acheter " + ("de maisons" if buyType == 0 else "d'hotels") + " ? (tu possedes " + moneyStr(playerMoney) + ")")) if len(nbs) else None
        if item == None: return
        needBuy = prop["data"]["money"] * nbs[item] * price
        rest = addMoney(pInd, -needBuy)
        if rest < 0 and not(needMoneys(pInd, abs(rest))): return
        prop["data"][key]+= nbs[item]
        gameDatas["players"][pInd]["cards"][propertyInd] = prop
        return builds(pInd, propertyInd)
    def property_actions(pInd, index): # hypotheque; buy houses; ...
        prop = gameDatas["players"][pInd]["cards"][index]
        if not(prop.get("active")):
            value = prop["data"]["money"]
            pMoney = calcMoney(pInd)
            if pMoney < value: return dialog(ast("Carte hypotheque. Vous n'avez pas assez d'argent pour la racheter!"))
            rebuy = menu(["Non", "Oui"], ast("Cette carte a ete hypotheque. Voulez-vous la racheter ?"))
            if rebuy:
                addMoney(pInd, -value)
                gameDatas["players"][pInd]["cards"].pop(index)
                newIndex = addCardToPlayer(pInd, prop["name"])
                if type(newIndex) == bool and newIndex == False: return dialog(ast("Erreur dans l'achat de ce bien!"))
                return property_actions(pInd, newIndex)
            else: return
        actions = {"Hypothequer": mortgage, "Batir": builds}
        if not(prop["data"]["allowConstructions"]): del actions["Batir"]
        action = menu(list(actions.keys()), ast(centerTxt(prop["name"])))
        if action == None: return
        if index != None: actions[list(actions.keys())[action]](pInd, index)
    def properties(pInd):
        props = gameDatas["players"][pInd]["cards"]
        if not(len(props)): return dialog(ast("Vous ne possedez pas encore de biens!"))
        l = []
        for p in props:
            group = p.get("data").get("group")
            if not(group): group = "ungrouped"
            if not(l.count(capitalize(group))): l.append(capitalize(group))
        choosedGrp = menu(l, ast("Voici vos biens (" + str(len(props)) + "):"))
        if choosedGrp == None: return
        groupName = l[choosedGrp]
        def f(c): return c["data"]["group"] == groupName.lower() if groupName.lower() != "ungrouped" else None
        wells = filterCards(f, pInd)
        if not(len(wells)): return dialog(ast("Une erreur est survenu avec ce type de bien...")) and properties(pInd)
        choosedCard = menu([ast(well["name"] if well["active"] else "*" + well["name"] + "*", (10000 if onPC else 18)) for well in wells], ast("Voici vos bien appartenant a la categorie des " + groupName + ":"))
        if choosedCard == None: return properties(pInd)
        index = gameDatas["players"][pInd]["cards"].index(findCard(f, pInd))
        property_actions(pInd, index)
        return properties(pInd)
    def needMoneys(pInd, needAchieve):
        pData, canPay = gameDatas["players"][pInd], 0
        for prop in pData["cards"]: canPay+= calcMortgaging(prop, pInd) if prop.get("active") else 0
        if canPay < needAchieve: return dialog(ast("Vous n'avez pas cette somme d'argent... (et avez hypothequer tous vos biens)")) and faillite(pInd) and 0
        while needAchieve > 0:
            def f(c): return c.get("active")
            validCards = filterCards(f, pInd)
            l = [card["name"] + " (" + moneyStr(calcMortgaging(card, pInd)) + ")" for card in validCards]
            action = menu(l, ast("Vous devez debloquer " + moneyStr(needAchieve) + ":"))
            if type(action) == int:
                card = validCards[action]
                if mortgage(pInd, pData["cards"].index(card)): needAchieve-= calcMortgaging(card, pInd)
        return True
    def faillite(pInd):
        for prop in gameDatas["players"][pInd]["cards"]:
            def f(c): return c["name"] == prop["name"]
            indexReset = gameDatas["plate"].index(findCard(f))
            gameDatas["plate"][indexReset] = initDatas["plate"][indexReset].copy()
        del gameDatas["players"][pInd]
        return dialog(ast("Vous venez de faire faillite! Votre pion a ete supprime du plateau..."))
    def case_owned_property(case, ownerIndex, playerIndex):
        ownerData, playerData = gameDatas["players"][ownerIndex], gameDatas["players"][playerIndex]
        dialog(ast("Vous venez d'entrer dans le domaine de "  + ownerData["name"] + "!"))
        def f(c): return c["name"] == case["name"]
        card = findCard(f, ownerIndex)
        if card["active"] == False: return dialog(ast("Mais ce dernier a hypotheque ce bien! Vous n'avez rien a paye!"))
        value = calcCardValue(card, ownerIndex)
        now = addMoney(playerIndex, -value) # Enleve l'argent au joueur
        if now < 0 and not(needMoneys(playerIndex, abs(now))): return dialog(ast(playerData["name"] + " n'a pas pu payer " + moneyStr(value) + " a " + ownerData["name"] + "!"))
        addMoney(ownerIndex, value) # Ajoute l'argent au proprio
        return dialog(ast(moneyStr(value) + " viennent d'etre verse a " + ownerData["name"] + "."))
    def case_property(case, pInd):
        def playerGet(p):
            for c in p.get("cards"):
                if c and c.get("name") == case["name"]: return True
        hasCase = findPlayer(playerGet)
        if hasCase and hasCase["name"] == gameDatas["players"][pInd]["name"]: return dialog(ast("Vous etes chez-vous!"))
        if hasCase: return case_owned_property(case, hasCase["index"], pInd)
        price = case["data"].get("money")
        playerMoney = calcMoney(pInd)
        if price > playerMoney: return dialog(ast(centerTxt(case["name"] + " est a vendre pour " + moneyStr(price) + ", mais vous n'avez que " + moneyStr(playerMoney) + ".")))
        if menu(["Passer l'offre", "Acheter le bien (" + moneyStr(price) + ")"], ast(case["name"] + " est a vendre. Vous possedez " + moneyStr(playerMoney) + ":")):
            isOk = addCardToPlayer(pInd, case["name"])
            if isOk == False and type(isOk) == bool: return dialog(ast("Erreur dans l'achat de ce bien..."))
            addMoney(pInd, price * -1) and dialog(ast(centerTxt("Achat confirme !")))
    def case_prison(pInd):
        prisonTime = gameDatas["players"][pInd]["prison"] if gameDatas["players"][pInd].get("prison") else gameDatas["settings"]["prisonTime"]
        dialog(ast("Vous filez droit en prison, vous serez blocke pendant " + str(prisonTime) + " tours!"))
        gameDatas["players"][pInd]["prison"] = prisonTime
        gameDatas["players"][pInd]["case"] = gameDatas["settings"]["prisonCaseIndex"]
    def processPacketCard(datas, pInd, isDifferent= False):
        if datas.get("give"):
            addMoney(pInd, datas["give"])
            dialog(ast(moneyStr(abs(datas["give"])) + " viennent d'etre " + ("verse sur" if datas["give"] > 0 else "retire de") + " votre compte!"))
        if datas.get("data"):
            types = datas["data"]
            if types.get("player"):
                for k in types["players"]: gameDatas["players"][pInd][k] = types["players"][k]
        if datas.get("move") and (datas["move"].get("to") or datas["move"].get("add")):
            to, add, moveNB = datas["move"].get("to"), datas["move"].get("add"), 0
            if to:
                index = to.get("index")
                if index==None:
                    def f(c):
                        for k in to: 
                            if c.get(k)!=to[k]: return False
                        return True
                    index = findCase(f)["index"]
                if index < gameDatas["players"][pInd]["case"]: moveNB = len(gameDatas["plate"]) - gameDatas["players"][pInd]["case"] + index
                else: moveNB = index - gameDatas["players"][pInd]["case"]
            elif add:
                index= gameDatas["players"][pInd]["case"] + add if gameDatas["players"][pInd]["case"] + add < len(gameDatas["plate"]) else len(gameDatas["plate"]) - gameDatas["players"][pInd]["case"] + add
                moveNB = add
            else: pass
            if datas["move"].get("instant"): gameDatas["players"][pInd]["case"]= index
            else:
                cases= move(moveNB, pInd)
                if(not(isDifferent)): process_moves(cases, pInd)
        if datas.get("players"): [processPacketCard(datas["players"], p, True) for p in range(len(gameDatas["players"])) if p != pInd]
        if datas.get("datas"):
            datas = datas["datas"]
            if datas.get("player"): 
                for key in datas["player"].keys(): gameDatas["players"][pInd][key] = datas["player"][key]
    def case_packet(data, pInd):
        packetType = data.get("type")
        packetList = gameDatas["packets"].get(packetType)
        if not(packetList): return dialog(ast("Une erreur est survenue avec ce type de carte!"))
        card = randItem(packetList)
        dialog(ast(centerTxt(card["title"]) + "\n> " + card["description"]))
        datas = card["data"]
        return processPacketCard(datas, pInd)
    def process_moves(cases, playerIndex):
        lastCase = cases.pop(len(cases)-1)
        case_type = lastCase.get("type")
        if case_type == "starting": addMoney(playerIndex, lastCase["data"]["money"])
        if case_type == "prison": return case_prison(playerIndex)
        for c in cases: 
            if c.get("type") == "starting":
                addMoney(playerIndex, c["data"]["money"])
                dialog(ast(centerTxt("Vous etes passe par la case depart! Vous avez recu " + moneyStr(c["data"]["money"]) + "!")))
                break
        if case_type == "property": case_property(lastCase, playerIndex)
        if case_type == "packet": case_packet(lastCase["data"], playerIndex)
        if case_type == "take":
            take = lastCase["data"]["money"]
            now = addMoney(playerIndex, take * -1)
            if now < 0 and not(needMoneys(playerIndex, abs(now))): return
            dialog(ast(centerTxt(moneyStr(take) +  " viennent d'etre retires de votre compte en bancque.")))
    def doAction(pInd):
        action = menu(["Lancer le de", "Biens", "Economies"], ast(centerTxt("Que souhaites-tu faire ?")))
        if action == 0: return
        if type(action) == int: [properties, moneys][action - 1](pInd)
        else: return False
        return doAction(pInd)
    def doGlobalAction():
        actions = ["Continuer", "Activer constructions", "Arreter le jeu"]
        if gameDatas["temp"].get("constructions") == True: del actions[1]
        action = menu(actions, ast("Le tour vient d'etre acheve!"))
        if not(action): return
        if action == len(actions)-1: return True
        if action == 1 and not(gameDatas["temp"].get("constructions")): gameDatas["temp"]["constructions"] = True
        return doGlobalAction()
    unSwitch= False
    while 1:
        if len(gameDatas["players"]) == 1: return game_end()
        if not(unSwitch): playerIndex = switchPlayer()
        playerData = gameDatas["players"][playerIndex]
        if playerData.get("prison"):
            dialog(centerTxt(ast(playerData["name"] + " est en prison pour encore " + str(playerData["prison"]) + " tours!")))
            gameDatas["players"][playerIndex]["prison"] -= 1
            continue
        globalActions = not(unSwitch) and dialog(centerTxt(ast("C'est au tour de " + playerData["name"] + " de jouer!"))) in cancel
        if globalActions and doGlobalAction(): return game_end()
        if doAction(playerIndex) == False:
            if doGlobalAction(): return game_end()
            else:
                unSwitch= True
                continue
        unSwitch = False
        minDice, maxDice = gameDatas["settings"]["dice"]
        gameDatas["temp"]["dice"] = randint(minDice, maxDice)
        cases = move(gameDatas["temp"]["dice"], playerIndex)
        dialog(ast(playerData["name"] + " avance de " + str(gameDatas["temp"]["dice"]) + " cases.") + "\n\n" + ast(centerTxt(cases[-1]["name"])))
        process_moves(cases, playerIndex)
def restart(): (main if menu(["Non", "Oui"], "Recommencer ?") else clear)()
def main():
    resetGameDatas()
    minPlayers,maxPlayers = gameDatas["settings"]["players"]
    clear()
    players = int(input("Nombre de joueurs:\n>>> "))
    if not(minPlayers <= players <= maxPlayers):
        dialog(ast("Le nombre de joueur doit etre compris entre " + str(minPlayers) + " et " + str(maxPlayers) + "!"))
        return restart()
    return game(players)
main()