""" -----------------
*      morpion      *
*                   *
*      Made by:     *
*      Flymeth      *
*                   *
----------------- """
from tools import *
from random import randint
win=3
players=["X","O"]
robotCharactId=0
basePlate=[
"   ",
"   ",
"   "
]
plate=basePlate.copy()
def renderPlate(txt):
  dPlate=plate.copy()
  dPlate[0]+="|"
  dPlate[1]+="|"+txt
  dPlate[2]+="|"
  return "\n".join(dPlate)
def resetPlate():
  global plate
  plate=basePlate.copy()
def newBotPos():
  x=randint(0,len(plate[0])-1)
  y=randint(0,len(plate)-1)
  return [x,y]
# p=plate[string]; s=selection[x,y]
def display(p,s,player):
  lines=["     ___ "]
  x=s[0]
  y=s[1]
  txt=["TIC","TAC","TOE"]
  for i in range(len(p)):
    t=txt[i]+" "
    if i==y:
      t+=">"+p[i]+"<"
    else:
      t+="|"+p[i]+"|"
    lines.append(t)
  row=list("---")
  row[x]="^"
  lines.append("     "+"".join(row))
  lines[2]+=" player: "+player
  for l in lines:
    print(l)
  return
def setCase(coord,player):
  global plate
  x=coord[0]
  y=coord[1]
  if plate[y][x]!=" ":
    return False
  plate[y]=plate[y][:x]+player+plate[y][x+1:]
  return True
def checkTie():
  tie=True
  for l in plate:
    if l.find(" ")!=-1:
      tie=False
  return tie
def checkWin(pos):
  bx=pos[0]
  by=pos[1]
  player=plate[by][bx]
  drct=[
  (1,0),
  (0,1),
  (-1,-1),
  (1,-1)
  ]
  for d in drct:
    s=0
    def check(coef):
      cx=d[0]*coef
      cy=d[1]*coef
      x,y=bx,by
      while x>=0 and y>=0 and x<len(plate[0]) and y<len(plate):
        e=plate[y][x]
        if e==player:
          s+=1
        else:
          break
        x+=cx
        y+=cy
      if s>=win:
        return True
      else:
        return False
    won=check(1)
    if not(won):
      if s>0:
        s-=1
      won=check(-1)
    if won:
      return True
  return won
def tie():
  clear()
  txt=renderPlate("    Egalite!")
  input(txt+"\n\n")
  return resetPlate()
def end(won):
  clear()
  txt=renderPlate("   "+won+" a gagne!")
  quit=menu(["Rejouer","Quitter"],txt)
  clear()
  if not(quit):
    return main()
def main():
  multi=menu(["1","2"],"Nombre de joueurs:")
  if multi==None:
    return clear()
  resetPlate()
  pId=0
  pos=[1,1]
  while 1:
    if pId>=len(players):
      pId=0
    robotLap=not(multi) and pId==robotCharactId
    clear()
    display(plate,pos,players[pId])
    if robotLap:
      pos=newBotPos()
      drct=True
    else:
      key=getKey("Move key:\n>>> ")
      drct=getDirection(key)
    if drct==True:
      done=setCase(pos,players[pId])
      if done:
        won=checkWin(pos)
        if won:
          return end(players[pId])
        elif checkTie():
          tie()
        pId+=1
      continue
    elif drct==None:
      return main()
    elif not(drct):
      continue
    pos[0]+=drct[0]
    pos[1]+=drct[1]*-1
    for i in range(len(pos)):
      if pos[i]>=len(plate[0]):
        pos[i]=len(plate[0])-1
      elif pos[i]<0:
        pos[i]=0
main()
