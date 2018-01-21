#!/usr/bin/python3
import os
import unicodedata
import difflib
import sys
#######################
# PROJET PYTHON M1109 #
#######################

#---------------------------------------------------------------#
#                        NOTE                                   #
# Pour des raisons plus ou moins obscure de copie de liste      #
# il faut rajouté '[:]' a la fin d'un .append() afin de pouvoir #
# lui passer une liste a lui aussi                              #
# la syntaxe de sorted :                                        #
#   sorted('liste',key=lambda x: (critère1, critère2))          #
#   ou les critère sont 'liste[0,1,...]'                        #
#                        NOTE 2                                 #
# Le programme accepte que 2 personne avec le meme nom soit     #
# rentré mais pas 2 personne avec le meme prenom ET le meme nom #
# (la date de naissance n'est pas prise en compte)              #
#                        NOTE 3                                 #
# Les chiffres negatifs sont symbolisé par des chiffres         #
# negatifs, (-1,-2,-3,...)                                      #
#---------------------------------------------------------------#

three = [] #liste preincipale = arbre genealogique
parente = [[1,3],[1,4],[0,1],[2,3],[2,4]] #liste pré-rempli pour teste
#parente = [] #liste des liens de parenté, [parent,enfant]

#enregistrement d'une personne
def register(vprenom,vnom,vbirthday,vsexe):
    newone = []
    newone.append(vprenom)
    newone.append(vnom)
    newone.append(vbirthday)
    newone.append(vsexe)
    return newone
                     #   0  , 1 ,    2   ,  3
                     #prenom,nom,birthfay,sexe
#Ajout de personne pour les tests, a commenter plus tard.
three.append(register("elizabeth",'Royal',"19260421","F"))
three.append(register("charles",'Royal',"19481114","H"))
three.append(register("diana",'Royal',"19610701","F"))
three.append(register("harry",'Royal',"19840915","H",))
three.append(register("william",'Royal',"19820621","H"))


#print(three)

def display(ls=three): #afficher toute la liste proprement
    printer = "{:<10} {:<10} {:<2}/{:<2}/{:<4} {:>3}"
    for i in range(0,len(ls)):
        print(printer.format(ls[i][0],ls[i][1],ls[i][2][6:8],ls[i][2][3:5],ls[i][2][:4],ls[i][3]))

#display(three)

def displaybis(ls,three=three): #afficher les personne correspondant aux id contenu dans une liste en entré
        printer = "{:<10} {:<10} {:<2}/{:<2}/{:<4} {:>3}"
        for i in ls:
            print(printer.format(three[i][0],three[i][1],three[i][2][6:8],three[i][2][3:5],three[i][2][:4],three[i][3],))

def displaybisbis(ls,three=three): #afficher les personne correspondant id contenu dans un tableau en entré
    printer = "{:<10} {:<10} {:<2}/{:<2}/{:<4} {:>3}"
    for j in range(0,len(ls)):
        for k in ls[j]:
            i = int(k)
            print(printer.format(three[i][0],three[i][1],three[i][2][6:8],three[i][2][3:5],three[i][2][:4],three[i][3],))
            #print(three[i][0]," ",three[i][1]," ",three[i][2][6:8],"/",three[i][2][3:5],"/",three[i][2][:4]," ",three[i][3],sep='')

def getId_OLD(vprenom,ls): #renvoie l'id du prenom entré OLD ==> getId
    control = 0         # à n'utiliser que si l'orthographe du nom entrer est exact
    vindex = ''
    for i in range(0,len(ls)):
        if(vprenom == ls[i][0]):
            vindex = i
            control = 1
    if(control == 0):
        print("wrong name")
    return vindex

def getId(name,ls=three):
    loop = 0
    result = [] #liste des resultats (id des perosnnes)
    simplename = unicodedata.normalize('NFD', name).encode('ascii','ignore').decode().lower()
    for i in range(0,len(ls)):
        lsname = unicodedata.normalize('NFD', ls[i][0]).encode('ascii','ignore').decode().lower()
        percent = difflib.SequenceMatcher(None, simplename, lsname).ratio()
        if(percent >= 0.75):
            result.append(i)
    if(len(result) == 1):
        print(" 1 Seul resultats trouvé:")
        print('')
        print(" - ",ls[result[0]][0],ls[result[0]][1])
        print('')
        valide = valideyn("Ce resultat est il correct ?")
        if(valide == 0):
            choice = -1
        else:
            choice = result[0]
    elif(len(result) > 1):
        print(len(result),"résultats trouvés :")
        print('')
        for i in range(0,len(result)):
            print(" ",i,")",end=' ')
            print(ls[result[i]][0],end=' ')
            print(ls[result[i]][1])
        while(loop != 1):
            print('')
            print("Lequel correspond a votre recherche ?(Entrer le numeros correspondant ou -1 si aucun choix ne correspond)")
            choice = input("==> ")
            try:
                int(choice)
            except ValueError:
                loop = 0
            if(int(choice) in range(-1,len(result))):
                loop = 1
    else:
        print("aucun resultat ne correspond a votre recherche.")
        os.system("sleep 1")
        choice = -1
    return int(choice)


#print(getId("Elizabeth",three))

def lienparente(parent,enfant,ls=parente,three=three): #attribu un parent a un enfant, parent et enfant sont des id
    control = 0
    if(int(three[enfant][2][:4]) - int(three[parent][2][:4]) < 13 ): #13 ans de difference minimum entre un parent et un enfant (ca semble acceptable)
        control = -1
    elif([parent,enfant] in ls): #empeche l'ajaout de 2 fois le meme lien de parenté
        control = -1
    nbrparent = 0
    for i in range(0,len(ls)): #pas plus de 2 parents par enfants
        if(ls[i][1] == int(enfant)):
            nbrparent += 1
    if (nbrparent > 2):
        control = -1
    if(control == -1):
        print("Impossible de créer ce lien de parenté.")
        os.system("sleep 1")
    else:
        ls.append([parent,enfant])
        print("Le lien de parent à été ajouter avec succes")
        os.system("sleep 1")

'''
print(three[3])
parent(2,3,three)
print(three[3])
'''
def whosyourparent(enfant,ls=parente): #renvoir l'id des parents dans une liste
    parentsid = []
    for i in range(0,len(ls)):
        if(ls[i][1] == enfant):
            parentsid.append(ls[i][0])
    return parentsid

#print(whosyourparent(3))

def ascendant(parent,ls=parente):#renvoie une liste avec TOUT les ascendant
    ascendanttab = []
    generation = 0
    loop = 0
    ascendanttab.append(whosyourparent(parent))
    while(loop != 1):
        ascendanttabgenplusun = []
        for i in range(0,len(ascendanttab[-1])):
            ascendanttabgenplusun.extend(whosyourparent(ascendanttab[-1][i]))
        ascendanttab.append(ascendanttabgenplusun)
        generation = generation + 1
        if(ascendanttab[-1] == []):
            ascendanttab.remove([])
            loop = 1
    return ascendanttab

#print(ascendant(3))

def simplew(word):
    return unicodedata.normalize('NFD', word).encode('ascii','ignore').decode().lower()

#print(simplew('Roél'))

def sortbyname(lsid,three=three): #tri par prenom puis par nom, pour trier par nom puis par prenom
    ordered = []                                               #inverser les 0 et les 1
    ordered.append(lsid[0])
    for i in range(0,len(lsid)):
        ctl = 0
        while ctl <= len(ordered):
            if simplew(three[lsid[i]][0]) < simplew(three[ordered[ctl]][0]):
                ordered.insert(ctl,lsid[i])
                ctl = len(ordered) + 2
            elif simplew(three[lsid[i]][0]) == simplew(three[ordered[ctl]][0]):
                if simplew(three[lsid[i]][1]) < simplew(three[ordered[ctl]][1]):
                    ordered.insert(ctl,lsid[i])
                elif simplew(three[lsid[i]][1]) > simplew(three[ordered[ctl]][1]):
                    ordered.insert(ctl+1,lsid[i])
                ctl = len(ordered) + 2
            elif simplew(three[lsid[i]][0]) > simplew(three[ordered[-1]][0]):
                ordered.append(lsid[i])
                ctl = len(ordered) + 2
            else :
                ctl += 1
    return ordered

#print(test([3,2,0,4,1]))

'''
#pas utile, la fonction lien de parent suffit
def enfant(parent,enfant,ls): #attribu un enfant a un parent; enfant & parent sont des id
    ls[parent][5].append(enfant)

print(three[2])
enfant(2,3,three)
print(three[2])
'''

def whosyourchildreen(parent,ls=parente): #renvoir l'id des parents dans une liste
    childreensid = []
    for i in range(0,len(ls)):
        if(ls[i][0] == parent):
            childreensid.append(ls[i][1])
    return childreensid
#print(whosyourchildreen(1))

def descendant(parent,ls=parente):#renvoie une liste avec TOUT les descendant
    descendanttab = []
    generation = 0
    loop = 0

    descendanttab.append(whosyourchildreen(parent))
    while(loop != 1):
        descendanttabgenplusun = []
        for i in range(0,len(descendanttab[-1])):
            descendanttabgenplusun.extend(whosyourchildreen(descendanttab[-1][i]))
        descendanttab.append(descendanttabgenplusun)
        generation = generation + 1
        if(descendanttab[-1] == []):
            descendanttab.remove([])
            loop = 1
    return descendanttab

#print(descendant(0))

def desfreresetdessoeurs(personne,ls=parente):
    parent = []
    freresoeur = []
    for i in range(0,len(ls)):
        if(ls[i][1] == personne):
            parent.append(ls[i][0])
    if(parent == []):
        freresoeur.append(-1)
    else:
        for j in range(0,len(parent)):
            for i in range(0,len(ls)):
                if(parent[j] == ls[i][0]) and (ls[i][1] != personne):
                        freresoeur.append(ls[i][1])
    freresoeur = list(set(freresoeur)) #de base set renvoie un dictionnaire, supprime les doublon
    return freresoeur

#print(desfreresetdessoeurs(3))

def sortbyname_OLD(lsid,three=three): #ancienne fonction ==> sortbyname fait à la main
    lsinfo = []
    for i in range(0,len(lsid)):
        lsinfo.append(three[lsid[i]])
    lssort = sorted(lsinfo,key=lambda x: (x[1], x[0]))
    return(lssort)

#display(sortbyname([3,2,0,4,1]))

def sortbydate_OLD(lsid,three=three):
    lsinfo = []
    for i in range(0,len(lsid)):
        lsinfo.append(three[lsid[i]])
    lssort = sorted(lsinfo,key=lambda x: x[2])
    return(lssort)

#display(sortbybdate([3,2,0,4,1]))

def dateFormat(year,month,day,nbtry): #formate la date pour le tri et elimine les erreurs
    loop = 0
    ybxt = 0
    longm = [1,3,5,7,8,10,12]
    courtm = [4,6,9,11]
    while True:
        try:
            int(year)
            int(month)
            int(day)
        except ValueError:
            break
        if(int(year) > 3000):
            break
        if(int(month) < 1) or(int(month) > 12):
            break
        if(int(month) in courtm):
            if(int(day) < 1) or (int(day) > 30):
                break
        if(int(month) in longm):
            if(int(day) < 1) or (int(day) > 31):
                break
        if(int(year) % 400 == 0):
            ybxt = 1
            if(int(day) < 1) or (int(day) > 29):
                break
        if(int(year) % 4 == 0) & (int(year) % 100 != 0):
            ybxt = 1
            if(int(day) < 1) or (int(day) > 29):
                break
        if(ybxt == 0):
            if(int(day) < 1) or (int(day) > 28):
                break
        loop = 1
        break
    while(len(month) < 2):
        month = "0" + month
    while(len(day) < 2):
        day = "0" + day
    nbtry += 1
    birthday = year + month + day
    return birthday, loop, nbtry

def sexeFormat(sexe): #test si le sexe entré est valide, seulement homme et femme pris en compte
    loop = 0
    if(sexe == "F") or (sexe == "f"):
        sexe = "F"
        loop = 1
    elif(sexe == "H") or (sexe == "h"):
        sexe = "H"
        loop = 1
    return sexe, loop

def valideyn(message): #demande une validation a l'utilisateur et renvoie 1 ou 0
    loui = ["oui","yes","y","o"]                                 #selon oui ou non
    lnon = ["non","no","n"]
    loop = 0
    print(message)
    print("(Entrer oui ou non)")
    while(loop != 1):
        choice = input("==> ")
        if(choice in loui):
            valide = 1
            loop = 1
        elif(choice in lnon):
            valide = 0
            loop =  1
    return valide

def valideyninverted(message): #r'envoie l'inverse de la fonction valideyn
    loui = ["oui","yes","y","o"]
    lnon = ["non","no","n"]
    loop = 0
    print(message)
    print("(Entrer oui ou non)")
    while(loop != 1):
        choice = input("==> ")
        if(choice in loui):
            valide = 0
            loop = 1
        elif(choice in lnon):
            valide = 1
            loop = 1
    return valide


def main(three=three):
    bloop = 0
    sloop = 0
    nbtry = 0
    exit = 0
    control = 0

    os.system('clear')
    print("----------------------Programme de généalogie-----------------------")
    print('')
    print(" 1. Ajouter une personne")
    print(" 2. Créer un lien de parenté")
    print(" 3. Afficher l'arbre")
    print(" 4. Afficher les descendant d'une personne")
    print(" 5. Afficher les ascendant d'une personne")
    print(" 6. Afficher les frères et soeurs d'une personne")
    print(" 7. Afficher les personne par ordre alphabetique")
    print(" 8. Afficher les personne par ordre chronologique")
    print(" 9. Quitter le programme")
    #I pour afficher un ID, pour debug
    print('')
    #print("Pour obternir l'id d'une perosnnes taper [I]") #Fonctionnatlité non-demandé pour le programme finale
    choix = input("==> ")
    if(choix == '1') or (choix == 1):
        control = 0
        while control != 1:
            os.system("clear")
            print("-------------------------AJOUT D'UNE PERSONNE----------------------")
            print("Quel est son prenom ?")
            prenom = str(input("==>"))
            print("Quel est son nom?")
            nom = str(input("==>"))
            print('')
            while(bloop == 0):
                if(nbtry == 0):
                    print("Entrer une date de naissance :")
                elif(nbtry != 0):
                    print("Entrer une date de naissance VALIDE :")
                print("Quel est son jour de naissance ?")
                day = input("==>")
                print("Quel est son mois de naissance ? ")
                month = input("==>")
                print("Quelle est son années de naissance ? ")
                years = input("==>")
                anniv, bloop, nbtry = dateFormat(years,month,day,nbtry)
            print('')
            while(sloop == 0):
                print("Sexe :")
                print("Enter [F] pour une femme ou [H] pour un homme.")
                sexe = input("==>")
                sexe, sloop = sexeFormat(sexe)
            three.append(register(prenom,nom,anniv,sexe))
            print('')
            control = valideyninverted("Ajouter une autre personne ?")
    elif(choix == "2") or (choix == 2):
        while(control != 1):
            print("--------------------------LIEN DE PARENTE----------------------")
            os.system("clear")
            print("Quel est le nom de l'ascendant ?")
            p1 = input("==>")
            p1 = getId(p1)
            if(p1 == -1):
                control = valideyn("Abandonner ?")
            if(control == 0):
                print("Quel est le nom du descendant ?")
                p2 = input("==>")
                p2 = getId(p2)
                if(p2 == -1):
                    control = valideyn("Abandonner ?")
                if(control == 0):
                    lienparente(p1,p2)
                    control = valideyninverted("Creer un autre lien de parenté ?")
    elif(choix == "I") or (choix == "i"): #recherche un identifiant
        while(control != 1):
            print("---------------RECHERCHE ID---------------------")
            os.system("clear")
            print("Entrer un nom : ")
            nom = input("==> ")
            id = getId(nom)
            if(id == -1):
                control = valideyninverted("Effectuer une nouvelle recherche ?")
            else:
                print("L'id correspondant a la recherche est :",id)
                print("")
                os.system("sleep 1")
                control = valideyninverted("Effectuer une nouvelle recherche ?")
    elif(choix == "3") or (choix == 3):
        while(control != 1):
            os.system("clear")
            print("----------------------Programme de généalogie-----------------------")
            print('')
            display(three)
            print('')
            os.system("sleep 2")
            print("Pour revenir au menu pricipale taper [Q]")
            qloop = 0
            while(qloop != 1):
                quit = input("==>")
                if(quit == "Q") or (quit == "q"):
                    qloop = 1
            control = 1
    elif(choix == "4") or (choix == 4):
        while(control != 1):
            os.system("clear")
            print("--------------------------DESCENDANT-----------------------")
            print("De qui voulez vous connaitre les descendant ?")
            nom = input("==> ")
            id = getId(nom)
            if(id == -1):
                control = valideyninverted("Effectuer une nouvelle recherche ?")
            else:
                os.system("clear")
                print("--------------------------DESCENDANT-----------------------")
                desclist = descendant(id)
                if desclist[0] != []:
                    print("Les descendant de",three[id][0],"sont :")
                    print('')
                    displaybisbis(desclist)
                    print("")
                    os.system("sleep 2")
                else:
                    print(three[id][0],"n'a pas de descendant")
                    print('')
                print("Pour revenir au menu pricipale taper [Q]")
                qloop = 0
                while(qloop != 1):
                    quit = input("==>")
                    if(quit == "Q") or (quit == "q"):
                        qloop = 1
            control = 1
    elif(choix == "5") or (choix == 5):
        while(control != 1):
            os.system("clear")
            print("--------------------------ASCENDANT-----------------------")
            print("De qui voulez vous connaitre les ascendant ?")
            nom = input("==> ")
            id = getId(nom)
            if(id == -1):
                control = valideyninverted("Effectuer une nouvelle recherche ?")
            else:
                os.system("clear")
                print("--------------------------ASCENDANT-----------------------")
                desclist = ascendant(id)
                if desclist[0] != []:
                    print("Les ascendant de",three[id][0],"sont :")
                    print('')
                    displaybisbis(desclist)
                    print("")
                    os.system("sleep 2")
                else:
                    print(three[id][0],"n'a pas d'ascendant")
                    print('')
                print("Pour revenir au menu pricipale taper [Q]")
                qloop = 0
                while(qloop != 1):
                    quit = input("==>")
                    if(quit == "Q") or (quit == "q"):
                        qloop = 1
            control = 1
    elif(choix == "6") or (choix == 6):
        while(control != 1):
            os.system("clear")
            print("--------------------------FRERE&SOEUR-----------------------")
            print("De qui voulez vous connaitre les frères et soeurs ?")
            nom = input("==> ")
            id = getId(nom)
            if(id == -1):
                control = valideyninverted("Effectuer une nouvelle recherche ?")
            else:
                os.system("clear")
                print("--------------------------FRERE&SOEUR-----------------------")
                freresoeurls = desfreresetdessoeurs(id)
                if freresoeurls != []:
                    print("Les frères et soeurs de",three[id][0],"sont :")
                    print('')
                    displaybis(freresoeurls)
                    print("")
                    os.system("sleep 2")
                else:
                    print(three[id][0],"n'a pas d'ascendant")
                    print('')
                print("Pour revenir au menu pricipale taper [Q]")
                qloop = 0
                while(qloop != 1):
                    quit = input("==>")
                    if(quit == "Q") or (quit == "q"):
                        qloop = 1
            control = 1
    elif(choix == "7") or (choix == 7):
        while(control != 1):
            os.system("clear")
            print("----------------------Programme de généalogie-----------------------")
            print('')
            nbrpersls = []
            for i in range(0,len(three)):
                nbrpersls.append(i)
            print("Voici toute les personne de l'arbre par ordre de nom")
            print('')
            displaybis(sortbyname(nbrpersls))
            os.system("sleep 2")
            print('')
            print("Pour revenir au menu pricipale taper [Q]")
            qloop = 0
            while(qloop != 1):
                quit = input("==>")
                if(quit == "Q") or (quit == "q"):
                    qloop = 1
            control = 1
    elif(choix == "8") or (choix == 8):
        while(control != 1):
            os.system("clear")
            print("----------------------Programme de généalogie-----------------------")
            print('')
            nbrpersls = []
            for i in range(0,len(three)):
                nbrpersls.append(i)
            print("Voici toute les personne de l'arbre par ordre de date de naissance")
            print('')
            display(sortbydate(nbrpersls))
            os.system("sleep 2")
            print('')
            print("Pour revenir au menu pricipale taper [Q]")
            qloop = 0
            while(qloop != 1):
                quit = input("==>")
                if(quit == "Q") or (quit == "q"):
                    qloop = 1
            control = 1
    elif(choix == "Q") or (choix == "q") or (choix == "9") or (choix == 9):
        exit = 1
    return exit

while(exit != 1):
    exit = main()
