from random import randint

class Joueur :

    def __init__(self, nom):
        self.nom = nom # Nom du joueur
        self.vie = 4 # Vie actuelle du joueur
        self.vie_max = 4 # Vie maximale du joueur
        self.objet = [] # Liste des objets du joueur
        self.salle_parcours = 0 # Nombre de salles traversées

    # Fait perdre de la vie au joueur
    def perdre_vie(self, nb) : 
        self.vie -= nb
        print("Tu as perdu :", nb, "vie(s) !")
        print("Il te reste :", self.vie, "vie(s) !")

    # Ajoute un objet à l'inventaire du joueur
    def gagner_objet(self, objet): 
        self.objet.append(objet)
        print("Tu as gagner un objet :", objet)

    #Utilise un objet de l'inventaire du joueur
    def utiliser_objet(self, objet): 
        self.objet.remove(objet)
        print("Tu as utiliser un objet :", objet)

    #Vérifie si le joueur est vivant
    def est_vivant(self) : 
        vivant = True
        if self.vie <= 0 :
            vivant = False
        return vivant
            

class Monstre :

    def __init__(self, nom, degat): 
        self.nom = nom  # Nom du monstre
        self.degat = degat # Dégâts infligés par le monstre

    # Attaque le joueur si booleen est True (sinon n'attaque pas, si le joueur a un spray, voir ligne 149)
    def attaque(self, joueur, booleen): 
        if booleen == True :
            print("Le monstre :", self.nom, "attaque ! Et tu perd", self.degat, "vie !")
            joueur.perdre_vie(self.degat)
        else :
            print("Le monstre :", self.nom, "a essayé de t'attaquer !")

class Salle :

    def __init__(self, num):
        self.num = num # Numéro de la salle
    
    def generer_porte(self, joueur):

        porte = ["p_simp", "p_clous", "p_maud", "p_cadenas", "p_piques", "p_gold"] # Types de portes
        compt_p = [] # Compteur pour chaque type de porte

        # Permet de créer une liste des portes en fonction des probabilités
        def comptage(compt):
            c=0 
            salle_finale =[] 
            for i in range(len(compt)) :
                for k in range(compt[i]) :
                    salle_finale.append(porte[c])
                c+=1
            return salle_finale
        
        # Tire 3 portes en fonction des probabilités
        def tirage_p(salle_finale) :

            salle = [] # Liste des portes sélectionnées
            porte_mini = ["p_simp", "p_clous", "p_maud"] # Portes minimales (sans cadenas, piques ou or)
        
            for i in range(2): # Tirage de 2 portes aléatoires et ajout d'une porte minimale
                p = randint(0, len(salle_finale)-1)
                salle.append(salle_finale[p])
            p_mini = randint(0, len(porte_mini)-1)
            salle.append(porte_mini[p_mini])
            return salle

        # Probabilités pour chaque type de porte
        if joueur.salle_parcours <= 20 :  
            Prob_simp = 4
            Prob_clous = 3
            Prob_maud = 1
            Prob_cadenas = 2
            Prob_piques = 0
            Prob_gold = 0
            

        elif joueur.salle_parcours <= 50 : 
            Prob_simp = 4
            Prob_clous = 5
            Prob_maud = 3
            Prob_cadenas = 4
            Prob_piques = 3
            Prob_gold = 1
            
        
        elif joueur.salle_parcours <= 80 :
            Prob_simp = 3
            Prob_clous = 5
            Prob_maud = 4
            Prob_cadenas = 4
            Prob_piques = 3
            Prob_gold = 1
            
        else :
            Prob_simp = 2
            Prob_clous = 4
            Prob_maud = 5
            Prob_cadenas = 4
            Prob_piques = 3
            Prob_gold = 2

        compt_p += (Prob_simp, Prob_clous, Prob_maud, Prob_cadenas, Prob_piques, Prob_gold) # Ajout des probabilités au compteur
        return tirage_p(comptage(compt_p))
    
    # Gère le contenu derrière la porte choisie par le joueur
    def contenu(self, porte, joueur): 

        fantome = Monstre("fantome", 1)
        dragon = Monstre("dragon", 2)
        nounours = Monstre("nounours", 3)
        comp_c = [] # Compteur pour le type de contenu
        comp_o = [] # Compteur pour les objets
        comp_m = [] # Compteur pour les monstres
        chose = ["monstre", "objet", "rien"]
        monstre = ["fantome", "dragon", "nounours"]
        objet = ["clé", "spray", "coeur", "clé dorée", "coeur + 1"]

        # Compte les probabilités pour chaque type de contenu
        def comptage_c(compt, tab): 
            c=0
            contenu = []
            for i in range(len(compt)) :
                for k in range(compt[i]) :
                    contenu.append(tab[c])
                c+=1
            return contenu
        
        # Tire un contenu aléatoire en fonction des probabilités
        def tirage_c(contenu) : 
            r = contenu[randint(0, len(contenu)-1)]
            return r
        
        # Gère les effets en fonction du résultat du tirage
        def effet(resultat) :    
            if resultat == "monstre" :
                mon = tirage_c(comptage_c(comp_m, monstre))

                # Active le spray et gère les effets en fonction du résultat
                if mon == "fantome" :
                    if "spray" not in joueur.objet :
                        fantome.attaque(joueur, True)
                    else :
                        fantome.attaque(joueur, False)
                        joueur.utiliser_objet("spray")
                        
                elif mon == "dragon" :
                    if "spray" not in joueur.objet :
                        dragon.attaque(joueur, True)
                    else :
                        dragon.attaque(joueur, False)
                        joueur.utiliser_objet("spray")

                elif mon == "nounours" :
                    if "spray" not in joueur.objet :
                        nounours.attaque(joueur, True)
                    else :
                        nounours.attaque(joueur, False)
                        joueur.utiliser_objet("spray")


            elif resultat == "objet":
                obj = tirage_c(comptage_c(comp_o, objet))
                if obj == "clé" :
                    joueur.gagner_objet("clé")
                elif obj == "spray" :
                    joueur.gagner_objet("spray")
                elif obj == "coeur" :
                    print("Tu as reçu un coeur et tu reprends toute ta vie !")
                    joueur.vie = joueur.vie_max
                elif obj == "clé dorée" :
                    joueur.gagner_objet("clé dorée")
                elif obj == "coeur + 1" :
                    print("Tu as reçu un coeur et tu reprends toute ta vie et un coeur en plus !")
                    joueur.vie = (joueur.vie_max)+1 

            elif resultat == "rien":
                print("Il n'y a rien derrière la porte !")

        # Probabilités pour chaque type d'objet
        Prob_clé= 4
        Prob_spray= 4
        Prob_coeur= 4
        Prob_clé_dorée= 1
        Prob_coeur_1= 0
        comp_o += [Prob_clé, Prob_spray, Prob_coeur, Prob_clé_dorée, Prob_coeur_1]
        
        
        # Probabilités pour chaque type de monstre
        if joueur.salle_parcours <= 49 : 
            Prob_fant = 1
            Prob_drag = 0
            Prob_nounou = 0
            
        elif joueur.salle_parcours <= 89 : 
            Prob_fant = 3
            Prob_drag = 1
            Prob_nounou = 0
        else : 
            Prob_fant = 4
            Prob_drag = 2
            Prob_nounou = 1
        comp_m += [Prob_fant, Prob_drag, Prob_nounou]


        # Contenu en fonction de la porte choisie
        if porte == "p_simp":
            Prob_mon = 3
            Prob_obj = 1
            Prob_rien = 4
            comp_c = [Prob_mon, Prob_obj, Prob_rien]
            resultat = tirage_c(comptage_c(comp_c, chose)) 
            effet(resultat)  

        elif porte == "p_clous":
            Prob_mon = 5
            Prob_obj = 3
            Prob_rien = 3
            comp_c = [Prob_mon, Prob_obj, Prob_rien]
            resultat = tirage_c(comptage_c(comp_c, chose))
            effet(resultat)

        elif porte == "p_maud":
            Prob_mon = 7
            Prob_obj = 5
            Prob_rien = 0
            comp_c = [Prob_mon, Prob_obj, Prob_rien]
            resultat = tirage_c(comptage_c(comp_c, chose))  
            effet(resultat)

        elif porte == "p_cadenas":
            Prob_mon = 2
            Prob_obj = 4
            Prob_rien = 0
            comp_c = [Prob_mon, Prob_obj, Prob_rien]
            resultat = tirage_c(comptage_c(comp_c, chose))  
            if "clé" in joueur.objet : # Vérifie si le joueur a une clé pour ouvrir la porte
                joueur.utiliser_objet("clé")
                effet(resultat)
            elif "clé dorée" in joueur.objet :
                joueur.utiliser_objet("clé dorée")
                effet(resultat)
                
        elif porte == "p_piques":
            Prob_mon = 3
            Prob_obj = 7
            Prob_rien = 0
            comp_c = [Prob_mon, Prob_obj, Prob_rien]
            resultat = tirage_c(comptage_c(comp_c, chose))  
            joueur.perdre_vie(1) # Le joueur perd 1 vie en entrant
            effet(resultat)

        elif porte == "p_gold":
            if "clé dorée" in joueur.objet :
                joueur.utiliser_objet("clé dorée")
                print("Tu as reçu un coeur et tu reprends toute ta vie et un coeur en plus !")
                joueur.vie = (joueur.vie_max)+1 

    # Gère l'exploration de la salle par le joueur
    def explorer(self, joueur): 
        
        print("\nSalle", self.num +1) # Affiche le numéro de la salle (numéro de salle commence à 1)
        portes = self.generer_porte(joueur) # Génère les portes disponibles

        for i in range(len(portes)):
            print(str(i+1) + " Porte : ", portes[i]) # Affiche les portes disponibles


        while True:
            try:
                choix = int(input("Choisis une porte (1–3) : ")) - 1

                # Vérifie si le choix est valide
                if choix < 0 or choix > 2:
                    print("Choix invalide.")
                    continue  # retourner au début du while

                porte = portes[choix]

                # Vérifie les conditions d'accès
                if porte == "p_cadenas" :  
                    if "clé" not in joueur.objet :
                        if "clé dorée" not in joueur.objet :
                            print("Tu n'as pas de clé !")
                            continue

                if porte == "p_gold" and "clé dorée" not in joueur.objet:
                    print("Tu n'as pas de clé dorée !")
                    continue

                # Si tout est ok, on sort de la boucle
                break

            #Si l'entrée n'est pas un chiffre
            except ValueError:
                print("Entrée invalide, entrez un chiffre.")
                   
            

        self.contenu(porte, joueur)
    

class Jeu :
    def __init__(self):
        nom = input("Nom du joueur : ") # Demande le nom du joueur
        self.joueur = Joueur(nom) # Crée une instance de Joueur

    def jouer(self):
        print("\nBienvenue dans Hauntlet !\n")

        # Boucle principale du jeu
        while self.joueur.est_vivant() and self.joueur.salle_parcours < 100: 
            salle = Salle(self.joueur.salle_parcours) 
            salle.explorer(self.joueur) 
            self.joueur.salle_parcours += 1
            print("Progression :", self.joueur.salle_parcours, "salle(s) traversée(s)")

        # Fin du jeu
        if self.joueur.salle_parcours < 100 :
            print("\nGAME OVER !")
            print("Tu es arrivé jusqu'à la salle :", self.joueur.salle_parcours)

        else :
            print("\nYOU WIN !")
            print("Tu es arrivé jusqu'à la salle :", self.joueur.salle_parcours)

Jeu().jouer()