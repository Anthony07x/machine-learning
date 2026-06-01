import sys
from collections import deque

#python solution.py resolution small_example.txt
#python solution.py cooking cooking_examples/coffee.txt cooking_examples/coffee_input.txt

def construct_path(myZaklj):
    # myZaklj -----> (tuple) : [set, set] 
    toPrint = []
    
    twoFinalUsed = myZaklj["NIL"] # NIL
    toPrint.append(f"NIL <--- {tuple(twoFinalUsed[0])} |+| {tuple(twoFinalUsed[1])}")
    mojRed = deque() # red setova
    mojRed.append(tuple(twoFinalUsed[0]))
    mojRed.append(tuple(twoFinalUsed[1]))
    
    #for k in myZaklj.keys():
    #    print(f"K: {k}")
        
    visited = set()
    
    while mojRed:
        zaklj = mojRed.popleft()
        if zaklj in myZaklj.keys() and zaklj not in visited: # ako nije iz zakljucaka, onda je iz klauzula (znaci nema prijasnjih roditelja)
            visited.add(zaklj)
            #print(f"Zakljucak {zaklj}")
            toPrint.append(f"{zaklj} <--- {tuple(myZaklj[zaklj][0])} |+| {tuple(myZaklj[zaklj][1])}")
            mojRed.extend(tuple(mySet) for mySet in myZaklj[zaklj])
            #for mySet in myZaklj[zaklj]:
            #    print(tuple(mySet))
    
    toPrint.reverse()  
    return  toPrint
    
def myDiscard(mySet, foundLiteral):
    mySet.discard(foundLiteral[1:])
    mySet.discard(foundLiteral[1:])
    mySet.discard(f"{foundLiteral}")
    mySet.discard(f"{foundLiteral}")
    mySet.discard(f"~{foundLiteral}")
    mySet.discard(f"~{foundLiteral}")
    return mySet    

#provjereno - radi
def negateDedux(dedux):
    negiranDedux = list()
    
    for klauz in dedux[0]:
        if klauz.find("~") == -1:
            negiranDedux.append(set([f"~{klauz}"]))
        else:
            negiranDedux.append(set([klauz[1:]]))
    return negiranDedux

def optimze(clauses):
    
    # optimiziraj za slucaj C1 podskup C2 --> prva petlja
    # optimiziraj za slucaj A v ~A (tautologija) --> druga petlja
    removeSet = set()
    for i in range(len(clauses)):
        for j in range(len(clauses)):
            if i != j and clauses[i].issubset(clauses[j]):
                #print(f"Removing {clauses[j]} because it contains {clauses[i]}")
                removeSet.add(j)
        for literal in clauses[i]:
            if f"~{literal}" in clauses[i]:
                removeSet.add(i)
                break
                
    optimized = [clauses[idx] for idx in range(len(clauses)) if idx not in removeSet]         
    return optimized          
  
def checkTautology(klauzula):
    for literal in klauzula:
        if f"~{literal}" in klauzula: return True
    return False

def selClauses(clauses, sos):
    
    #Strategija SoS -- prvo pokusavamo pronaci oba komplementa u SoS-u
    komp1, komp2, foundLiteral = "", "", ""
    flagSoS, flagPremise = False, False
    for claus in sos:
        for literal in claus:
            
            # provjeri ima li literal u SoS-u
            for klauzula in sos:
                if f"~{literal}" in klauzula:
                    zaklj = tuple(myDiscard(claus.union(klauzula), literal))
                    if (zaklj in provjeraNovog.keys()): #and claus in provjeraNovog[zaklj] and klauzula in provjeraNovog[zaklj]):
                        #print("prvi")
                        #print(f"zaklj {zaklj} | claus: {provjeraNovog[zaklj]}")
                        #print(f"claus {claus} | klauz {klauzula}")
                        continue
                    if len(claus) == 1 and len(klauzula) == 1:
                        #print(f"NIL <-----> {claus} | {klauzula}")
                        provjeraNovog["NIL"] = [claus, klauzula] 
                        return True # pronaden NIL
                    komp1 = claus
                    komp2 = klauzula
                    foundLiteral = literal
                    flagSoS = True
                    break
            if komp1 != "": break
            
            if komp1 == "":
            # provjeri ima li literal u premisama
                for klauzula in clauses:

                    # ode moras provjerit mogucnost F | ~F  i  ~F | F
                    if f"~{literal}" in klauzula or (literal[0] == "~" and f"{literal[1:]}" in klauzula): 
                        zaklj = tuple(myDiscard(claus.union(klauzula), literal))
                        if (zaklj in provjeraNovog.keys()): #and claus in provjeraNovog[zaklj] and klauzula in provjeraNovog[zaklj]):
                            #print("drugi")
                            #print(f"zaklj {zaklj} | claus: {provjeraNovog[zaklj]}")
                            #print(f"claus {claus} | klauz {klauzula}")
                            continue
                        if len(claus) == 1 and len(klauzula) == 1:
                            #print(f"NIL <-----> {claus} | {klauzula}")
                            provjeraNovog["NIL"] = [claus, klauzula]
                            return True # pronaden NIL
                        komp1 = claus # sos
                        komp2 = klauzula # premise
                        foundLiteral = literal
                        flagPremise = True
                        break
            
            if komp1 != "": break
        if komp1 != "": break
    
    if(komp1 != ""):
       
        
        #nova klauzula za dodati ---> pazi moze biti tautologija --> provjeri
        #izbaci pronadene literale iz tih klauzula ( A i ~A )
        toAdd = myDiscard(komp1.union(komp2), foundLiteral)
        #print(f"{toAdd} <--- {komp1} | {komp2} | (Literal: {foundLiteral})\n")
       
        if(tuple(toAdd) not in provjeraNovog.keys()):
            provjeraNovog[tuple(toAdd)] = [komp1, komp2]
        
        zaIzbacitSuperSetove = list()
        superset = False
        if(checkTautology(toAdd) == False):
            for idx, zaklj in enumerate(sos):
                if(toAdd.issuperset(zaklj)):
                    zaIzbacitSuperSetove.clear()
                    break
                elif(toAdd.issubset(zaklj)):
                    zaIzbacitSuperSetove.append(zaklj)
                    
            if(len(zaIzbacitSuperSetove) > 0):
                for mySet in zaIzbacitSuperSetove:
                    sos.remove(mySet)
                    
                sos.append(toAdd)
                #print(f"{toAdd} <--- {komp1} | {komp2} | (Literal: {foundLiteral})\n")
                sos = sorted(sos, key=len)  
            
            if superset == False:    
                sos.append(toAdd)
                #print(f"{toAdd} <--- {komp1} | {komp2} | (Literal: {foundLiteral})\n")
                sos = sorted(sos, key=len)                 
            
        return sos
    
    # literala nema u sos-sos niti u sos-premisa, onda moramo provjeriti u premisa-premisa
    for claus in clauses:
        for literal in claus:
            for klauzula in clauses:
                if f"~{literal}" in klauzula:
                    zaklj = tuple(myDiscard(claus.union(klauzula), literal))
                    if (zaklj in provjeraNovog.keys()): #and claus in provjeraNovog[zaklj] and klauzula in provjeraNovog[zaklj]):
                        #print("treci")
                        #print(f"zaklj {zaklj} | claus: {provjeraNovog[zaklj]}")
                        #print(f"claus {claus} | klauz {klauzula}") 
                        continue
                    if len(claus) == 1 and len(klauzula) == 1:
                        #print(f"NIL <-----> {claus} | {klauzula}")
                        provjeraNovog["NIL"] = [claus, klauzula]
                        return True # pronaden NIL
                    komp1 = claus
                    komp2 = klauzula
                    foundLiteral = literal
                    break
                if komp1 != "": break
        if komp1 != "": break
    
    if(komp1 != ""):
        
        toAdd = myDiscard(komp1.union(komp2), foundLiteral) # nova klauzula za dodati ---> pazi moze biti tautologija --> provjeri
        #print(f"{toAdd} <--- {komp1} | {komp2} | (Literal: {foundLiteral})\n")
        
        if(tuple(toAdd) not in provjeraNovog.keys()):
            provjeraNovog[tuple(toAdd)] = [komp1, komp2]
        
        zaIzbacitSuperSetove = list()
        superset = False
        if(checkTautology(toAdd) == False):
            for idx, zaklj in enumerate(sos):
                if(toAdd.issuperset(zaklj)):
                    zaIzbacitSuperSetove.clear()
                    break
                elif(toAdd.issubset(zaklj)):
                    zaIzbacitSuperSetove.append(zaklj)
                    
            if(len(zaIzbacitSuperSetove) > 0):
                for mySet in zaIzbacitSuperSetove:
                    sos.remove(mySet)
                    
                sos.append(toAdd)
                #print(f"{toAdd} <--- {komp1} | {komp2} | (Literal: {foundLiteral})\n")
                sos = sorted(sos, key=len)  
            
            if superset == False:    
                sos.append(toAdd)
                #print(f"{toAdd} <--- {komp1} | {komp2} | (Literal: {foundLiteral})\n")
                sos = sorted(sos, key=len)                
            
        return sos

    return False
        
if "resolution" in sys.argv:
    idx_resolution = sys.argv.index("resolution")
    putevi_file_path = sys.argv[idx_resolution + 1]
    #print(putevi_file_path)
    file = open(f".\\{putevi_file_path}", "r", encoding="utf-8")
   
    klauzule = list()
    linije = file.readlines()
    duljina = len(linije)
    cilj = list()
    provjeraNovog = dict()
    krajnjiCilj = ""
    for idx, line in enumerate(linije):
        if line.find("#") == -1:
            if idx < duljina - 1:
                klauzule.append(set(line.lower().strip().split(" v ")))
            else: 
                krajnjiCilj = line.lower().strip()
                cilj.append(set(line.lower().strip().split(" v "))) # [{a, c, b, d}]
                #print("Cilj: ", cilj)
     
    cilj = negateDedux(cilj)  
    #print("Negirani cilj", cilj)
            
    for idx, kl in enumerate(klauzule, start=1):
        print(f"{idx}. ({' v '.join(kl)})")
      
    for idx, kl in enumerate(cilj, start=1):
        print(f"{idx}. ({' v '.join(kl)})")
     
    klauzule = optimze(klauzule)
    print("---------OPTIMIZIRANE-----------")
    
    klauzule = sorted(klauzule, key=len) 
    
    for idx, kl in enumerate(klauzule, start=1):
        print(f"{idx}. ({' v '.join(kl)})")  
        
    for idx, kl in enumerate(cilj, start=1):
        print(f"{idx}. ({' v '.join(kl)})")
    print("------------------------------\n--------------PATH----------------")
    
    while True:
        rez = selClauses(klauzule, cilj)
        if(rez == True):
            for path in construct_path(provjeraNovog):
                print(path)
            print("------------------------------")
            print(f"[CONCLUSION]: {''.join(krajnjiCilj)} is true")
            break
        elif(rez == False):
            print("------------------------------\n------------------------------")
            print(f"[CONCLUSION]: {''.join(krajnjiCilj)} is unknown")
            break
        
    file.close()
    
elif "cooking" in sys.argv:
    idx_cooking = sys.argv.index("cooking")
    put_do_klauzula = sys.argv[idx_cooking + 1]
    put_do_naredbi = sys.argv[idx_cooking + 2]
    
    put_do_klauzula = open(f".\\{put_do_klauzula}", "r", encoding="utf-8")
    put_do_naredbi = open(f".\\{put_do_naredbi}", "r", encoding="utf-8")

    linije_klauzule = put_do_klauzula.readlines()
    linije_naredbe = put_do_naredbi.readlines()

    duljina_klauzule = len(linije_klauzule)
    duljina_naredbe = len(linije_naredbe)

    klauzule = list()
    naredbe = list()

    # dodaj obicne klauzule
    for line in linije_klauzule:
            klauzule.append(set(line.lower().strip().split(" v ")))
    # DODANO
    klauzule = optimze(klauzule)        
    klauzule = sorted(klauzule, key=len)

    for line in linije_naredbe:
        if line.find("+") != -1:
            klauzule.append(set(line.lower().strip()[0:-1].strip().split(" v "))) 
            klauzule = sorted(klauzule, key=len)
            print(f"Dodana klauzula {line.strip()[0:-1]}\n")
            
        elif line.find("-") != -1:
            makni = set(line.lower().strip()[0:-1].strip().split(" v "))
            if makni in klauzule:
                klauzule.remove(makni)
                klauzule = sorted(klauzule, key=len)
                print(f"Maknuta klauzula {makni}\n")
                
        elif line.find("?") != -1:  
            provjeraNovog = dict() 
            cilj = list()
            cilj.append(set(line.lower().strip()[0:-1].strip().split(" v ")))
            krajnjiCilj = line.lower().strip()
            cilj = negateDedux(cilj)
            print(f"Provjeri: {krajnjiCilj}")
            while True:
                rez = selClauses(klauzule, cilj)
                if(rez == True):
                    for path in construct_path(provjeraNovog):
                        print(path)
                    print("------------------------------\n------------------------------")
                    print(f"[CONCLUSION]: {krajnjiCilj[0:-1].strip()} is true\n")
                    break
                elif(rez == False):
                    print("------------------------------\n------------------------------")
                    print(f"[CONCLUSION]: {krajnjiCilj[0:-1].strip()} is unknown\n")
                    break

    put_do_klauzula.close()
    put_do_naredbi.close()   
else:
    print("Error u unosu argumenata! Pokušajte ponovno.")