from tools import *
settings={"mines":{"desc":"Taux de mines","accept":(float,[0,1]),"value":.05},
          "sizeX":{"desc":"Longueur de la grille","accept":(int,None),"value":21},
          "sizeY":{"desc":"Hauteur de la grille","accept":(int,None),"value":6},
          "displayStats": {"desc": "Informations de la partie", "accept": ("menu", [True, False]), "value": False}}
chars = {"bomb": "#", "blank": " ", "flag": "X", "hidden": "~", "player": "O"}
coefs = [(1,1),(1,0), (0,1), (1,-1)]
def sets():
  global settings
  names=list(settings.keys())
  edit=menu([n+" ("+str(settings[n]["value"])+")" for n in names],ast("Parametre a editer:"))
  if edit==None: return main()
  infos=settings[names[edit]]
  desc,acp,value=infos["desc"],infos["accept"],infos["value"]
  tpe,cond=acp
  clear()
  if tpe=="menu":
    i=menu(cond,ast(desc))
    if i!=None: value=cond[i]
  else:
    try:
      v=input(ast(desc+":\n-> "))
      if not(v in cancel): v= tpe(v)
      else: v= value
    except:
      dialog(ast("Type invalide!"))
      return sets()
    if type(cond)==list:
      if not(cond[0]<=v<=cond[1]):
        dialog(ast("Cette valeur doit etre comprise entre "+str(cond[0])+" et "+str(cond[1])+"!"))
        return sets()
    value= v
  infos["value"]= value
  settings[names[edit]]=infos
  return sets()
def gridTxt(grid, px, py, discovered=[], lineSep="\n", charSep="", height= 6, width= 21):
    g = deepcopy(grid)
    g[py][px]= chars["player"]
    
    # Y
    interY = round(height / 2)
    mnY = 0 if py < interY else py - interY if interY <= py < len(g) - interY else len(g) - height
    if mnY < 0: mnY = 0
    mxY = mnY + height
    # X
    interX = round(width / 2)
    mnX = 0 if px < interX else px - interX if interX <= px < len(g[0]) - interX else len(g[0]) - width
    if mnX < 0: mnX= 0
    mxX = mnX + (width if width < len(g[0]) else len(g[0]))
    
    txt= []
    for y in range(mnY, mxY):
      txt.append([])
      for x in range(mnX, mxX):
        case = g[y][x]
        if case == chars["flag"] or case == chars["player"]: pass
        elif not(discovered and (x, y) in discovered): case= chars["hidden"]
        txt[-1].append(str(case))
      txt[-1] = charSep.join(txt[-1])

    return lineSep.join(txt)
def initGrid():
  global settings
  settingsVals = {s: settings[s]["value"] for s in settings.keys()}
  grid = [[chars["blank"] for j in range(settingsVals["sizeX"])] for i in range(settingsVals["sizeY"])]
  txMines = settingsVals["mines"]
  def getTxMines():
      tx= 0
      mx= 0
      for i in range(len(grid)):
          for case in grid[i]:
              if case== chars["bomb"]: tx+=1
              mx+=1
      return tx/ mx
  bombs=[]
  while getTxMines() < txMines:
      rX = randint(0, len(grid[0])-1)
      rY = randint(0, len(grid)-1)
      if grid[rY][rX]== chars["bomb"]: continue
      bombs.append((rX,rY))
      grid[rY][rX]= chars["bomb"]
  for x, y in bombs:
      for cx, cy in coefs:
          for sign in range(-1, 2, 2):
              nx, ny = x + cx * sign, y + cy * sign
              if 0<= nx < len(grid[y]) and 0<= ny < len(grid):
                if grid[ny][nx] == chars["blank"]: grid[ny][nx]= 1
                elif type(grid[ny][nx]) == int: grid[ny][nx]+= 1
  return grid, bombs
def play():
  global partyEnd
  grid, bombs= initGrid()
  discovered, flagged= [], {}
  partyEnd= False
  def discover(x,y):
    needToDiscover = [(x, y)]
    while len(needToDiscover): # While there are cases to discover
      for x, y in needToDiscover: # For each cases that need to be discovered
        if not (x,y) in discovered: # If this case hasn't already been discovered
          discovered.append((x,y)) # Set the case as discovered
          if grid[y][x]== chars["blank"]: # If this case is a blank case
            for i in range(-1,2,2): #       For each cases    #
              for cx,cy in coefs:   # around the current case #
                nx,ny= x+cx*i, y+cy*i
                if 0<=nx<len(grid[0]) and 0<=ny<len(grid) and not((nx,ny) in discovered) and (type(grid[ny][nx]) == int or grid[ny][nx] == chars["blank"]): 
                  if grid[ny][nx] == chars["flag"]: unflag(nx, ny) # Unflag because the flag is useless
                  needToDiscover.append((nx, ny)) # Add this case in the queue to be discovered if this one hasn't been discovered and is of type None or int
        needToDiscover.pop(needToDiscover.index((x, y))) # Remove the current case because it has been discovered
  def unflag(x, y):
    if flagged.get((x, y)) == None: return
    grid[y][x] = flagged[(x, y)]
    del flagged[(x, y)]
  def flag(x, y):
    unflag(x, y)
    flagged[(x, y)] = grid[y][x]
    grid[y][x]= chars["flag"]
  def processCase(x, y):
      if (x, y) in discovered: return
      action= menu(["Marqueur", "Creuser"], ast("Que souhaitez-vous faire:"))
      if action== None: return
      elif action == 0:
        if grid[y][x]== chars["flag"]: unflag(x, y); dialog(ast("Marqueur supprime!"))
        else: flag(x, y); dialog(ast("Le marqueur a ete placee"))
      elif action == 1:
        if grid[y][x]== chars["flag"]: return unflag(x, y)
        if grid[y][x]== chars["bomb"]: return loose()
        discover(x,y)
      if checkWin(): return won()
  def checkWin():
    if len(bombs) != len(flagged): return False
    for coords in flagged.keys():
      if not (coords in bombs): return False
    return True
  def discoverAll():
    [unflag(x, y) for x, y in list(flagged.keys())]
    [discovered.append((x,y)) for y in range(len(grid)) for x in range(len(grid[0]))]
  def loose():
    global partyEnd
    dialog(ast("Boom! Tu t'es pris une grosse mine dans la gueule!"))
    discoverAll()
    partyEnd= True
  def won():
    global partyEnd
    dialog(ast("GG! Tu as decouvert l'ensemble des mines!"))
    discoverAll()
    partyEnd= True
  px,py= 0,0
  while 1: # Main
      clear()
      txt= gridTxt(grid, px, py, discovered, charSep=" " if onPC else "", height= 20 if onPC else 6) + "\n"
      if settings["displayStats"]["value"] and not(partyEnd): txt+= "(" + str(len(flagged)) + "/" + str(len(bombs)) + " found) "
      key=input(txt)
      if key=="666":
        discoverAll()
        continue
      d= getDirection(key)
      if d== True and not(partyEnd): processCase(px, py)
      elif d == None: return main()
      if type(d) != tuple: continue
      nx, ny= px+ d[0], py - d[1]
      if 0<= nx <len(grid[0]) and 0<=ny < len(grid): px,py= nx,ny
  return main()
def main():
  do= menu(["Jouer","Parametres","Quitter"],ast(centerTxt("DEMINEUR")))
  if do==2 or do==None: return clear()
  [play,sets][do]()
main()
