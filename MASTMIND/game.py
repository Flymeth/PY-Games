from tools import *
mindcolors= [('r', colors.red, 'Red'), ('b', colors.blue, 'Blue'), ('g', colors.green, 'Green'), ('y', colors.yellow, 'Yellow'), ('p', colors.pink, 'Pink'), ('c', colors.cyan, 'Cyan')]
sets={"nb_colors":(3,range(2,len(mindcolors)+1)),"nb_fails":(12,range(1,30)),"nb_tofind":(4,range(2,9))}
def settings():
  global sets
  while 1:
    chs=[o+" ("+str(sets[o][0])+")" for o in sets]
    c=menu(chs,"Parametres:")
    if type(c)!=int: return
    key=list(sets.keys())[c]
    val,accept=sets[key]
    txt=ast("Nouvelle valeur pour \""+key+"\":")+"\n"
    if accept in [int,float,str]:
      try:
        val=accept(input(txt))
      except:
        dialog(ast("La valeur entree n'est par valide!"))
        continue
    else:
      try:
        val=list(accept)[menu(list(accept),txt)]
      except:
        dialog(ast("Une erreur est survenue..."))
        continue
    sets[key]=(val,accept)
def getColorGrid(code=[]):
  objs= [e for l in code for e in mindcolors if e[0]==l]
  return (" - " if onPC else "-").join([(obj[1] if onPC else '')+('*' if onPC else obj[0])+(colors.reset if onPC else '') for obj in objs])
def getCode(randomize=True, length=None, preTxt=""):
  if not(length): length=sets["nb_tofind"][0]
  cols= mindcolors[:sets["nb_colors"][0]]
  if(randomize): return [randItem(cols)[0] for i in range(length)]
  code=[]
  letters= [(obj[1] if onPC else "") + obj[2] + (colors.reset if onPC else "") for obj in cols]
  while len(code)<length:
    try:
      code.append(cols[menu(letters, ast(preTxt+"Couleur "+str(len(code)+1)+"/"+str(length)+":\n"+getColorGrid(code)))][0])
    except:
      if len(code): code.pop()
      else: return False
  return code
def game(code):
  global won, fails
  won=False
  fails=0
  attemps= []
  def show_atmps():
    if not(len(attemps)): dialog(ast("Vous n'avez pas encore fait d'essaies")); return False
    first_list= [getColorGrid(attemps[i].get("input"))+" (#"+str(i+1)+")" for i in range(len(attemps))]
    atp_index= menu(first_list, "Essaie a analiser:")
    if type(atp_index)!=int:
      return False
    result=attemps[atp_index].copy().get("result")
    if not(result) or len(result)!=3: dialog("Cet essaie est corrompu..."); return show_atmps()
    obj={"Bien placee": result[0], "Present": result[1], "Non present": result[2]}
    menu([k+": "+str(obj[k]) for k in obj.keys()], getColorGrid(attemps[atp_index].get("input")))
    return show_atmps()
  def try_code():
    global fails, won
    tryCode=getCode(False, preTxt="Choisis ta combinaison!\n", length=len(code))
    if not(tryCode): return False
    if tryCode!=code: fails+= 1 
    else: won=True; return True
    well_placed=just_present=not_present=0
    checker= code.copy()
    res=[]
    for index in range(len(tryCode)):
      pre,pla=tryCode[index] in checker, code[index]==tryCode[index] # (is letter present in the code ?, is letter at the correct position ?)
      if pre and pla: well_placed+=1;just_present+=1
      elif pre: just_present+=1
      else: not_present+=1
      if pre: checker.remove(tryCode[index])
      res.append({"present":pre, "placed":pla})
    attemps.append({"code": code, "input": tryCode, "result": (well_placed,just_present,not_present), "ordered_result": res})
    dialog(getColorGrid(tryCode)+"\n"+ast(str(well_placed)+" bien placee(s)\n"+str(just_present)+" presente(s)\n"+str(not_present)+" invalide(s)"))
    return False
  def forfeit(): return True
  while fails<sets["nb_fails"][0]:
    fcts=[show_atmps, try_code, forfeit]
    todo= menu(["Tentatives", "Essayer un code", "Abandonner"], "Essaie #"+str(len(attemps)+1))
    if type(todo)!=int: continue
    if fcts[todo](): # returns "True" if the game needs to be stopped
      break
  return won, fails, attemps
def play():
  genRand= menu(["Manuel", "Automatique"], "Creation du code:")
  if type(genRand)!=int: return
  code= getCode(genRand)
  if not(code): return
  won, fails, attemps= game(code)
  if won: dialog(ast("Bravo! Le code etait bien:\n"+getColorGrid(code)+"\nTu l'as trouve en "+str(fails+1)+" essaies!"))
  else: 
    ff=fails<sets["nb_fails"][0]
    if ff: dialog(ast("Domage: tu y etais presque:\n"+getColorGrid(code)))
    else: dialog(ast("Aie... Tu n'as plus d'essaie restant. Le code etait:\n"+getColorGrid(code)))
def main():
  fcts=[("Jouer", play), ("Parametres", settings), ("Quitter", clear)]
  todo= menu([e[0] for e in fcts], ast(" MasterMind\n By Johan J."))
  if type(todo)!=int or todo==len(fcts)-1: return clear()
  fcts[todo][1]()
  return main()
main()