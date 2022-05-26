from tools import *
l_upper= [chr(i) for i in range(65,91)]
l_lower= [l.lower() for l in l_upper]
pions=l_upper.copy()
sets_type={"size":range(2,10),"score":["normal","advanced"]}
sets={"size":4,"score":"normal"}
blank=" "
sep= " "
pionsSpawn= [1,2]
winAt=pions[-1]
grid=[]
bestScore=0
def calcScore():
  global bestScore
  cases=[e for l in grid for e in l]
  if sets["score"]=="advanced":
    s=1
    for c in cases:
      if c==blank:
        continue
      s+= 2**pions.index(c)
  else:
    b=sorted(cases,reverse=True)
    s=2**pions.index(b[0])
  if s>bestScore:
    bestScore=s
  return s
def resetGrid():
  global grid
  grid=[[blank for i in range(sets["size"])] for i in range(sets["size"])]
def movePions(d):
  x,y=d[0],d[1]*-1
  ranges=[range(0,sets["size"]),range(sets["size"]-1,-1,-1)]
  rx=ranges[1] if x>0 else ranges[0]
  ry=ranges[1] if y>0 else ranges[0]
  upgraded=[]
  for ey in ry:
    for ex in rx:
      p=grid[ey][ex]
      if p==blank:
        continue
      nx,ny=ex,ey
      while 1:
        nx,ny=nx+x,ny+y
        if nx<0 or ny<0 or nx>=sets["size"] or ny>=sets["size"]:
          nx,ny=nx-x,ny-y
          break
        cp=grid[ny][nx]
        if cp!=blank:
          if cp==p and not((nx,ny) in upgraded):
            ind=pions.index(p)
            if ind<len(pions)-1:
              ind+=1
            p=pions[ind]
            upgraded.append((nx,ny))
          else:
            nx,ny=nx-x,ny-y
          break
      grid[ey][ex]=blank
      grid[ny][nx]=p
def addPions():
  pos=[(x,y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x]==blank]
  if not(len(pos)):
    return False
  mx=randint(pionsSpawn[0],pionsSpawn[1])
  pos=shuffle(pos)[:mx]
  for (x,y) in pos:
    grid[y][x]=pions[0]
  return len(pos)>1
def initGrid():
  resetGrid()
  addPions()
def txtGrid(base=False):
  txt=""
  for line in grid:
    if txt:
      txt+="\n"
    l="".join(line)
    if not(base):
      txt+= ("|" + sep + "".join([c+sep for c in l]) + "|") if onPC else "|" + l + "|"
    else:
      txt+=l
  if not(base):
    txtExtr= "-"*(sets["size"]*(len(sep)+1)+len(sep)) if onPC else "-"*sets["size"]
    txt="/" + txtExtr + "\\\n" + txt
    txt+= "\n\\" + txtExtr + "/"
  return txt
def tuto():
  dialog(ast("Comment jouer au 2048 (modifie) ? C'est super simple:"))
  dialog(ast("A chaque tour, la lettre " + pions[0] + " apparait entre " + str(pionsSpawn[0]) + " et " + str(pionsSpawn[1]) + " sur la grille."))
  dialog(ast("En deplacant tout les pions en meme temps horizontalement et verticalement, vous pourrez les combiner."))
  dialog(ast("Sachant que:\n- "+pions[0]+"+"+pions[0]+"="+pions[1]+"\n- "+pions[1]+"+"+pions[1]+"="+pions[2]+"\n- etc..."))
  dialog(ast("Le but etant d'arriver jusqu'a la lettre "+ pions[-1]+ "!"))
def checkWin():
  for l in grid:
    if len(["" for c in l if c==winAt]):
      return True
  return False
def checkLoose():
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      p= grid[y][x]
      if p==blank:
        return False
      cx,cy=x,y
      for coefx in range(-1,2):
        for coefy in range(-1,2):
          if coefx!=0 and coefy!=0 or coefx==coefy==0:
            continue
          nx,ny= cx+coefx,cy+coefy
          if nx<0 or ny<0 or nx>sets["size"]-1 or ny>sets["size"]-1:
            continue
          cp= grid[ny][nx]
          if cp==blank or cp==p:
            return False
  return True
def endG(txt):
  score= calcScore()
  txtG= txtGrid(True)
  dialog(ast(txt+"\nScore: "+str(score)+"p.\n"+txtG))
def scores():
  dialog(ast("Best score: "+str(bestScore)+"p"))
def game():
  initGrid()
  while 1:
    clear()
    txt=centerTxt(txtGrid())+"\n"
    d=getDirection(getKey(txt))
    if d==(0,0) or d==True:
      continue
    elif d==None:
      return False
    elif type(d)!=tuple:
      continue
    movePions(d)
    full=not(addPions())
    if full and checkLoose():
      return endG("Perdu!")
    if checkWin():
      return endG("Bravo!")
def settings():
  global sets
  p=sets.copy()
  while 1:
    c=menu([k+" ("+str(p[k])+")" for k in p] + ["Enregister"], "Parametre a changer:")
    clear()
    if type(c)!=int or c>=len(list(p.keys())):
      sets=p.copy()
      return
    k=list(p.keys())[c]
    txt=ast("Nouvelle valeur:")+"\n"
    v_type=sets_type[k]
    if v_type in [int,str,float]:
      try:
        v=v_type(input(txt))
      except:
        dialog("Valeur invalide!")
        continue
    elif type(v_type) in [list,range]:
      v=list(v_type)[menu(list(v_type),txt)]
    p[k]=v
def main():
  dialog(centerTxt(ast("Bienvenue sur mon 2048!"+"\n\n"+"CREE PAR Johan - 1C")))
  while 1:
    todo=menu(["Nouveau","Scores","Tuto","Parametres","Quitter"],centerTxt(ast("2048: Le jeu")))
    if todo==0:
      lost= game()
      if lost:
        return loose()
    elif todo==1:
      scores()
    elif todo==2:
      tuto()
    elif todo==3:
      settings()
    else:
      return clear()
main()