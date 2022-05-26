"""-----------------*
*                   *
*    puissance 4    *
*                   *
*    By Flymeth     *
*                   *
*-----------------"""
from tools import *
from p4_mod import *
player=players[randint(0,1)]
winScore=4
rInd=0
grille=[[""]*9 for i in range(6)]
def changePlayer(rand=False):
  global player
  if rand:
    player=shuffle(players)[0]
  player=players[players.index(player)-1]
def settings():
  global winScore, grille, displayMode, players
  edit=menu(["Forme des pions", "Type de jeu", "Taille de la grille", "Mode d'affichage", "Extras", "Sauvegarder"], "Editer: ")
  clear()
  if edit==None or edit==5:
    return dialog("Parametres modifies!")
  if edit==0:
    p1=input("Pion du joueur 1:\n>>> ")
    if p1:
      players[0]=p1[0]
    clear()
    p2=input("Pion du joueur 2:\n>>> ")
    if p2:
      players[1]=p2[0]
  elif edit==1:
    w=int(input(autoSplitTxt("Nombre de pions a aligner pour gagner [3,8]:\n>>>")+" "))
    if 3<=w<=8:
      winScore=w
  elif edit==2:
    w=int(input(autoSplitTxt("Longeur de la grille [3, 9]:\n>>>")+" "))
    h=int(input(autoSplitTxt("Hauteur de la grille [3, 6]:\n>>>")+" "))
    if 3<=w<=9 and 3<=h<=6:
      grille=[[""]*w for i in range(h)]
  elif edit==3:
    displayMode= setDisplayMode()
  elif edit==4:
    setExtras()
  return settings()
def setCase(x,pl):
  y=len(grille)-1
  while y>=0:
    if grille[y][x]== "":
      grille[y][x]=pl
      return [y,x]
    y-=1
  return False
def reset():
  for row in range(len(grille)):
    for i in range(len(grille[row])):
      grille[row][i]=""
def checkWin(case, gr=[]):
  grid=gr.copy()
  y,x=case
  c=grid[y][x]
  for t in types:
    pos=[]
    maxX,maxY=len(grid[0])-1,len(grid)-1
    for i in range(2):
      cx,cy=x,y
      t[0]*=-1
      t[1]*=-1
      while cx>=0 and cy>=0 and cx<=maxX and cy<=maxY:
        if grid[cy][cx]==c:
          if pos.count((cx,cy))==0:
            pos.append((cx,cy))
        else:
          break
        cx+=t[0]
        cy+=t[1]
    if len(pos)>=winScore:
      for p in pos:
        x,y=p
        grille[y][x]=charForTypes[types.index(t)]
      return True
  return False
def IA(iaInfos,playerInfos,case): # [IA] <START>
    iaPos, iaBaits= iaInfos
    playerPos, playerBaits= playerInfos
    maxX=len(grille[0])-1
    maxY=len(grille)-1
    bannedPosition=[]
    for e in playerPos:
      score=int(e)
      for (x,y) in playerPos[e]:
        if score>=winScore-1 and ((y+2<=maxY and grille[y+1][x]=="" and grille[y+2][x]!="") or (y+1==maxY and grille[y+1][x]=="")):
          bannedPosition.append(x)
    iaPos=getSortedValues(iaPos, grille, bannedPosition, winScore, case)
    playerPos=getSortedValues(playerPos, grille, bannedPosition, winScore, case)
    print("IA:",iaPos,"\nPLAYER:",playerPos,"\nBANNED:",bannedPosition)
    def getBetterPosition(els):
      if len(els):
        for (x,y) in els[0][1]:
          if not(x in bannedPosition) or (els[0][0]>=winScore and y+1<len(grille) and grille[y+1][x]==""):
            return x
      if len(bannedPosition)>maxX or len(bannedPosition)==0:
        return None
      return int(randfloat(0,maxX,1,bannedPosition))
    if len(iaPos)==0:
      return getBetterPosition(playerPos)
    for IA in iaPos:
      IAScore, IABlancks=IA
      for (iaX,iaY) in IABlancks:
        if IAScore>=winScore-1:
          return iaX
        for PLAYER in playerPos:
          PlayerScore, PlayerBlanks=PLAYER
          for (playerX,playerY) in PlayerBlanks:
            if (bannedPosition.count(iaX) or bannedPosition.count(playerX)) and IAScore<winScore-1:
              continue
            if PlayerScore>IAScore and PlayerScore>=winScore-1:
              return playerX
            if len(playerBaits) and PlayerScore>IAScore:
              return getBetterPosition([(winScore-1, playerBaits)])
    if len(iaBaits):
      return getBetterPosition([(winScore-1, iaBaits)])
    return getBetterPosition(iaPos)
def processCases(allCases, same, isIA=False):
  outVal, baits={}, []
  take_at=winScore-preshot_before
  if isIA:
    take_at=1
  if len(allCases)==0:
      return (outVal, baits)
  def addEl(score,blankPos):
      if outVal.get(str(score))==None:
        outVal[str(score)]=blankPos
      else:
        alreadyInList= len(["" for p in blankPos if p in outVal[str(score)]])
        if not(alreadyInList):
          outVal[str(score)]+= blankPos
  for (x,y) in allCases:
      maxX=len(grille[0])-1
      maxY=len(grille)-1
      for t in types:
          blankPos=[]
          allPos=[]
          touchBorder=False
          for i in range(2):
              t[0]*=-1
              t[1]*=-1
              cx,cy=x,y
              blanked=False
              while cx>=0 and cy>=0 and cx<=maxX and cy<=maxY:
                  if grille[cy][cx]==same:
                      if allPos.count((cx,cy))==0:
                        allPos.append((cx,cy))
                  elif grille[cy][cx]=="":
                    if blanked:
                      break
                    blanked=True
                    blankPos.append((cx,cy))
                  else:
                    break
                  cx+=t[0]
                  cy+=t[1]
              else:
                touchBorder=True
          score=len(allPos)
          if len(blankPos)>0 and score>=take_at and not(touchBorder and score+len(blankPos)<winScore):
            if score==winScore-2 and len(blankPos) == winScore-2: # = check if it's a bait
              baits.append(blankPos[0])
            addEl(score,blankPos)
  return (outVal, baits)
def processIACase(last):
  positions={"bot":[],"user":[],"blanks":[]}
  ia, user =player, players[players.index(player)-1]
  for y in range(len(grille)):
    for x in range(len(grille[y])):
      if grille[y][x]==ia:
        positions["bot"].append((x,y))
      elif grille[y][x]==user:
        positions["user"].append((x,y))
      else:
        positions["blanks"].append(x)
  if len(positions["blanks"])==1:
      return positions["blanks"][0]
  return IA(processCases(positions["bot"],ia, True),processCases(positions["user"],user),last)
def getBotPos(hardcore=False,lastCase=(0,0)):
  if not(hardcore):
    allowed=[x for x in range(len(grille[0])) if grille[0][x]!=""]
    x= randItem(allowed) if len(allowed) else randint(0,len(grille)-1)
    print("FINAL: set by random (x:",str(x)+")",allowed)
    return x
  x= processIACase(lastCase)
  if x==None: return getBotPos(False)
  print("FINAL: set by ai (x:",str(x)+")")
  return x
# [IA] <END>
def checkTie():
  for y in grille:
    for case in y:
      if case=="":
        return False
  return True
def dispChoice(c):
  global displayMode
  g2=[]
  for i in range(len(grille)):
    line=grille[i].copy()
    if i+1<len(grille):
      nextLine=grille[i+1].copy()
    else:
      nextLine=False
    if len(line[c])==0 and nextLine and len(nextLine[c])==0 and displayMode=="calc":
      line[c]="|"
    elif len(line[c])==0 and (nextLine == False or len(nextLine[c])!=0) and displayMode=="desk":
      line[c]="#"
    g2.append(line)
  return g2
def end():
  if menu(["Recommencer", "Quitter"], "Partie termine!")==0:
    return play()
  return endprm()
def play(editSettings=True):
  global grille, players
  if editSettings:
    editSettings=menu(["Defaut","Modifier"], "Parametres ?")
    if editSettings==None:
      return play()
  if editSettings:
    settings()
  gameType=menu(["IA vs IA","1 Joueur","2 Joueurs", "Informations", "Quitter"],"PUISSANCE 4\nBy Johan J.")
  if gameType==3:
    informations()
    return play(False)
  if gameType==4:
    return endprm()
  if gameType==None:
    return play()
  IAFight=gameType==0
  useBot=gameType==1 or IAFight
  hardcore=False
  if useBot:
    while 1:
      hardcore=menu(["Normal (random)", "Hardcore (IA)"], "Difficulte:")
      if hardcore==None:
        return play(False)
      if hardcore and menu(["Activer quand meme", "Annuler"], autoSplitTxt("Attention: le mode hardcore est mal optimise!")) in [1,None]:
        continue
      break
  i=0
  changePlayer(True)
  reset()
  jump=False
  case=()
  while True:
    clear()
    if i>len(grille[0])-1:
      i=len(grille[0])-1
    if i<0:
      i=0
    g2=dispChoice(i)
    txt=display(g2)
    if displayMode=="calc":
      txt=("-"*i)+"~"+ ("-"*(len(grille[0])-i-1)) +" player: " + player + "\n"+txt+ " >>> "
    else:
      txt=" "*(i*4+2)+ player + "\n" + txt + "\n>>> "
    if IAFight or (useBot and player==players[rInd]):
      i=getBotPos(hardcore,case)
      key=None
      if IAFight and getKey(txt)==3:
        return end()
    elif not(jump):
      key=getKey(txt)
    jump=False
    if key==0:
      i-=1
    elif key==1:
      i+=1
    elif key==2:
      reset()
    elif key==3:
      return end()
    else:
      clear()
      case=setCase(i,player)
      if case:
        if checkWin(case, grille):
          txt=(" "*(len(grille[0])))+" "+player+ " won!\n"+ display(grille) +" ~ "
          if displayMode!="calc":
            txt=(" "*(len(grille[0])*4+1))+"     "+player+ " won!\n"+ display(grille) +"\n ~ "
          return input(txt), end()
        elif checkTie():
          txt=(" "*(len(grille[0])))+" Egalite!\n"+ display(grille) +" ~ "
          if displayMode!="calc":
            txt=(" "*(len(grille[0])*4+1))+"     Egalite!\n"+ display(grille) +"\n~ "
          return input(txt), end()
        changePlayer()
        grille, players= doExtras(grille, players)
      elif IAFight or (useBot and player==players[rInd]):
        jump=True
play()
