from math import *
from random import *
up=["8","n"]
down=["2","v"]
right=["6","r"]
left=["4","p"]
idle=["5"]
cancel=["/","t","}"]
access=[""]
onPC=False
class colors:
  pink = '\033[95m'
  blue = '\033[94m'
  cyan = '\033[96m'
  green = '\033[92m'
  yellow = '\033[93m'
  red = '\033[91m'
  bold = '\033[1m'
  underline = '\033[4m'
  modeBG = "\033[7m"
  reset = '\033[0m'
def deepcopy(obj=[]):
  """
  Copie le contenu de la matrice et renvoi la nouvelle matrice
  """
  assert type(obj) == list, "Ce type n'est pas une liste !"
  def copy(e):
    n=[]
    for i in e:
      if type(i)==list:
        i=copy(i)
      n.append(i)
    return n
  return copy(obj)
def sleep(nb):
  """
  Permet de rajouter la fonction "sleep" sur calculatrice
  """
  assert nb>=0,"nb doit etre positif"
  nb=float(nb)*80000
  for i in range(nb): pass
  return nb
def fixed(number,n=0,forceStr=False):
  val=round(number,n)
  if not(n):
    val=int(val)
  if len(str(val))==len(str(number)) and type(number)!=int:
    t=""
    s=str(number)
    m=0
    for l in range(len(s)):
      if t.find(".")==None:
        m+=1
      elif l-m>n+1:
        break
      t+=s[l]
    if not(forceStr):
      val=float(t)
    else:
      val=t
  if forceStr:
    return str(val)
  return val
def randfloat(mn,mx=None,fixe=2,banned=[]):
  """
  Renvoi un reel aleatoire entre mn & mx (inclu)
  """
  if type(mx)!=int and type(mx)!=float:
    mx=mn
    mn=0
  elif mx<mn:
    mx=mn
  r=(random()*(mx-mn))+mn
  nb= fixed(r,fixe)
  if nb in banned: return randfloat(mn,mx,fixe,banned)
  return nb
def randItem(iterable, banned=[]):
  """
  Renvoi un element au hasard dans l'iterable "iterable"
  """
  assert type(iterable)==list, "iterable doit etre une liste!"
  if not(len(iterable)): return None
  return iterable[randfloat(0,len(iterable)-1,0,banned)]
def clear(height=6):
  """
  Efface le contenu de l'ecran
  """
  return print("\n"*height)
def display(m=[]):
  for line in m: print(line)
def dialog(txt="", height=6):
  """
  Permet de creer une boite de dialog
  """
  messages=txt.split('\n')
  pages=[]
  if len(messages)>=height:
    current=""
    for i in range(len(messages)):
      if current:
        current+="\n"
      current+=messages[i]
      if (i!=0 and i%height==0) or i>=len(messages)-1:
        pages.append(current)
        current=""
  else:
    pages=["\n".join(messages)]
  for txt in pages:
    clear()
    k= input(txt+"\n")
    if k in cancel:
      return k
  clear()
def getKey(txt=""):
  k=input(txt)
  return k[-1] if len(k) else k
def autoSplitTxt(txt,mx=20):
  """
  Permet de couper automatiquement le texte suivant la largeur de l'ecran
  -> Abreviation: ast()
  """
  l,group=[],[]
  word=""
  txtLen=len(str(txt))
  for i in range(txtLen):
    letter=txt[i]
    isBack=letter=="\n"
    if isBack:
      group.append(word + ("\n" if i >= txtLen-1 else ""))
      word=""
    else:
      if letter!= " ":
        word+=letter
      if letter==" " or i >= txtLen - 1:
        group.append(word + (" " if i >= txtLen-1 and letter == " " else ""))
        word=""
    lineTxt= " ".join(group)
    tempSentence=lineTxt+word
    if onPC:
      colorsDict=colors.__dict__
      for key in colorsDict: tempSentence= tempSentence if key.startswith('__') and key.endswith('__') else tempSentence.replace(colorsDict[key], '', tempSentence.count(colorsDict[key])+1)
    if len(tempSentence)>=mx or i>=txtLen-1 or isBack:
      l.append(lineTxt)
      group.clear()
  return "\n".join(l)
ast=autoSplitTxt
def getDirection(k):
  if type(k)!=str:
    return k
  key=k.lower()
  if key in up:
    return (0,1)
  elif key in down:
    return (0,-1)
  elif key in right:
    return (1,0)
  elif key in left:
    return (-1,0)
  elif key in idle:
    return (0,0)
  elif key in cancel:
    return None
  elif key in access:
    return True
  else:
    return ""
def menu(mChoices=[],txt=""):
  """
  Permet de creer un menu
  """
  nbLines=txt.count("\n")+1
  assert nbLines<5,"Le texte prend trop de place"
  elementsPerPages=(5-nbLines)
  nbPages=ceil(len(mChoices)/elementsPerPages)
  useMultiplePages=nbPages>1
  pages=[]
  if useMultiplePages:
    p=[]
    def app():
        pages.append(p.copy())
        p.clear()
    for i in range(len(mChoices)):
      if (i!=0 and i%elementsPerPages==0):
        app()
      p.append(mChoices[i])
      if i==len(mChoices)-1:
        app()
  else:
    pages.append(mChoices.copy())
  pIndex=0
  c=0
  while True:
    if pIndex<0:
      pIndex=nbPages-1
    elif pIndex>=nbPages:
      pIndex=0
    choices=pages[pIndex].copy()
    if c>len(choices)-1:
      c=0
    elif c<0:
      c=len(choices)-1
    choices[c]="~ "+str(choices[c])
    backCount=5-len(choices)-txt.count("\n")
    extraTxt=""
    if useMultiplePages:
      pre=suf=""
      if pIndex>0:
        pre="< "
      if pIndex<nbPages-1:
        suf=" >"
      extraTxt=" "+pre+"  "+str(pIndex+1)+"/"+str(nbPages)+"  "+suf
    clear()
    if backCount<=0:
      backCount=1
    print(txt+"\n"+extraTxt+"\n"*(backCount-1))
    display(choices)
    key=getKey()
    if key.lower() in up:
      c-=1
    elif key.lower() in down:
      c+=1
    elif key.lower() in right:
      pIndex+=1
      c=0
    elif key.lower() in left:
      pIndex-=1
      c=0
    elif key.lower() in cancel:
      return None
    elif key.lower() in access:
      eID=c+(pIndex*elementsPerPages)
      return eID
def shuffle(iterable):
  """
  Renvoi la liste "iterable" melange
  """
  n=deepcopy(iterable)
  new=[]
  while len(n):
    e=randItem(n)
    n.remove(e)
    new.append(e)
  return new
def centerTxt(txt,mw=20):
  """
  Renvoi le texte aligne horizontalement
  """
  if type(txt)!=str: return txt
  if "\n" in txt: return "\n".join([centerTxt(t) for t in txt.split("\n")])
  if len(txt)>=mw: return txt
  blks=" "*floor((mw-len(txt))/2)
  return blks+txt+blks
def embed(txt,mw=20,mh=5):
  """
  Cree un embed
  """
  allTxt=centerTxt(ast(txt,mw - 2)).split("\n")
  if not(len(allTxt)): return
  blankNB=floor((mh-len(allTxt)))
  displayer = '"""'+"-"*(mw-3)+"*"
  if blankNB>0 and blankNB%2 != 0: displayer += "\n" + "\n".join(["*"+" "*(mw-1)+"*"]* (blankNB%2))
  for t in allTxt: displayer+= "\n*"+t[:mw-1]+(" "*(mw-len(t)-1))+"*"
  if blankNB>0: displayer += "\n" + "\n".join(["*"+" "*(mw-1)+"*"]* (blankNB%2 | 1))
  return dialog(displayer + "\n*"+"-"*(mw-3)+'"""', mh)
def capitalize(txt):
  """
  Renvoi le texte avec la premiere lettre du premier mot en majuscule
  """
  return txt[0].upper() + txt[1:]
def tools_help():
  """Affiche de l'aide sur le module Jtools"""
  sep=","
  helps= ["Merci d'utiliser les Jtools!","Pour quitter ce menu, appuyez sur \""+cancel[0]+"\".",
    "Dans ce programe vous allez surement devoir vous deplacer dans une map.","Pour cela, appuyez sur les touches correspondante au mouvement,",
    "Puis confirmez votre choix en appuyant sur la touche EXE.","Voici toutes les touches que vous pourrez utiliser:",
    sep.join(up)+" pour aller en haut",sep.join(down)+" pour aller en bas",sep.join(right)+" pour aller a droite",
    sep.join(left)+" pour aller a gauche",sep.join(cancel)+" pour annuler/revenir en arriere",
    "Jtools est un module permettant d'ameliorer l'experience python sur calculatrice.",
    "Cree par Johan et utilisable de tous, vous pourrez grace a lui cree...","de meilleurs programes/jeux sur calculatrice.",
    "Vous pourrez grace a lui:","- creer des menus\n- utiliser sleep()\n- couper auto. la taille d'un text",
    "- avoir une direction en fonction d'une touche\n- et bien plus!","Plus d'information: voir Johan"]
  for txt in  helps:
    clear()
    if dialog(autoSplitTxt(txt)) in cancel and menu(["Rester", "Quitter"], "Quitter ce menu?"): return
if __name__ != "__main__": embed("Program created with the help of Jtools!")
if __name__ != "__main__" and menu(["Aide", "Passer"], autoSplitTxt("Ce programme utilise Jtools."))==0: tools_help()
onPC= menu(["Terminal (defaut)", "Powershell"], "Materiel utilise:")