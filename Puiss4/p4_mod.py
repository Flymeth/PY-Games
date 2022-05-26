from tools import clear, menu, colors
players=["*","O"]
playersColors=[colors.blue, colors.red]
right="6"
left="4"
reset="7"
stop="/"
keys=[left,right,reset,stop]
types=[
  [-1,1],
  [1,1],
  [0,1],
  [1,0],
]
charForTypes=[
  "/",
  "\\",
  "|",
  "-"
]
# ne doit pas etre < 2s
preshot_before=2

extras= {"move": 0}

# calc: Mode calculatrice
# desk: Mode pc
displayMode= "calc"

def setDisplayMode():
  global displayMode
  mode=menu(["Calculatrice", "Ordinateur"], "Mode d'affichage:")
  if mode==None:
    return ["calc", "desk"][mode]
  displayMode= ["calc", "desk"][mode]
  return ["calc", "desk"][mode]

def setExtras():
  names=[]
  txt=[]
  for key in extras:
    names.append(key)
    txt.append(key+[" (no)", " (yes)"][extras[key]])
  extraIndex=menu(txt, "Extras:")
  if extraIndex==None:
    return
  name=names[extraIndex]
  if extras[name]:
    extras[name]=0
  else:
    extras[name]=1
  return setExtras()

def display(m):
  txt=""
  if displayMode=="calc":
    for row in m:
      if len(txt):
        txt+="\n"
      for case in row:
        if len(case)==0:
          txt+=" "
        else:
          txt+=case
  else:
    gridColor= colors.bold+colors.green
    for row in m:
      if len(txt):
        txt+="\n"
      txt+=gridColor+ "|"
      for case in row:
        if not(len(case)):
          txt+="   |"
        else:
          caseColor=colors.yellow
          if players.count(case):
            caseColor=playersColors[players.index(case)]
          txt+=" "+caseColor+case+gridColor+" |"
      if m.index(row)==len(m)-1:
        txt+="\n\\"+"="*(len(m[0])*4-1)+"/"
      else:
        txt+="\n|"+"="*(len(m[0])*4-1)+"|"
    txt+=colors.reset
  return txt

def getKey(txt):
  clear()
  k=input(txt)
  if len(k)>2:
    k=list(k)[-1]
  if k in keys:
    return keys.index(k)
  elif len(k)>=1:
    return getKey(txt)
  else:
    return None

def getSortedValues(els, grille, bannedPositions, winScore,case):
  maxY=len(grille)-1
  canBePlaced=[]
  cantBePlaced=[]
  for key in sorted(els, reverse=True):
    score=int(key)
    canBlanks=[]
    cantBlanks=[]
    for (x,y) in sortByLong(els[key],case):
      if x in bannedPositions and score<winScore-1:
        continue
      if y+1<=maxY and grille[y+1][x]=="":
        cantBlanks.append((x,y))
      else:
        canBlanks.append((x,y))
    if len(canBlanks):
      canBePlaced.append((score, canBlanks))
    if len(cantBlanks):
      cantBePlaced.append((score, cantBlanks))
  return canBePlaced+cantBePlaced
def sortByLong(e,case):
  def sort(e2):
    cX,cY=case
    x,y=e2
    return abs(((cX-x)**2+(cY-y)**2)**0.5)
  return sorted(e,key=sort)

def informations():
  return ""

def endprm():
  return clear()

def doExtras(grille, players):
  if extras["move"]:
    if 1:
      for row in range(len(grille)):
        grille[row]=[grille[row][i-1] for i in range(len(grille[row]))]
  return grille, players