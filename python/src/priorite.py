from config_extrude import *

"""
@author POTTIN Tom 1B5
"""

#-------------------------------------------------------------------------------------------------------------
# Fonction utilise pour l'ordonnanceur
#-------------------------------------------------------------------------------------------------------------
"""
Tri le dictionnaire de processus
tri a bulle avec la priorite des processus

:param processus : dictionnaire contenant les processus
:return: dictionnaire des données trier
"""
def sort_processus(processus: dict) -> dict:
    items = list(processus.items())
    n = len(items)
    for i in range(n - 1):
        echange = False
        for j in range(n - 1 - i):
            # items[j] = (id, [date, duree, ram, priorite, butoir]) : plus grande priorité d'abord
            if items[j][1][3] < items[j + 1][1][3]:
                items[j], items[j + 1] = items[j + 1], items[j]
                echange = True
        if not echange:
            break
    return dict(items)



"""
Soumet le processus dans la file d'ordonnancement
Compare si a un instant un processus devrait être dans la file si oui on regarde si il est
déjà soumis ou fini sinon on l'ajoute a la file

:param instant : instant de l'execution
:param processus_ex : dictionnaire contenant les processus dans la file
:param processus_fini : dictionnaire contenant les processus terminer
:param processus : dictionnaire contenant les processus
:param retour : tableau de retour
"""
def soumission(instant:int, processus_ex:dict, processus_fini:dict,processus:dict,retour:list):
    for i in processus.keys():
        if instant >= processus[i][0]:
            if i not in processus_ex.keys() and i not in processus_fini.keys():
                processus_ex[i] = processus[i].copy()
                retour.append([i,instant,None,processus_ex[i][2]])





"""
Vérifie avant la simulation si l'ordonnancement est impossible

Détecte les cas où aucun processus ne pourra jamais s'exécuter ou terminer :
- un processus demande plus de RAM que la RAM totale
- aucun processeur n'est disponible
- l'énergie disponible n'est jamais suffisante pour alimenter un processeur

:param energies : dictionnaire de l'énergie disponible par instant (contenu de energie.csv)
:param processus : dictionnaire contenant les processus {id: [soumission, durée, ram, priorité, butoir]}
:param ram_totale : RAM totale disponible
:param energieParProc : énergie consommée par un processeur sur un pas de temps
:param processeurs : liste des identifiants des processeurs
:return: True si l'ordonnancement est impossible, False s'il peut être tenté
"""
def faisabilite(energies,processus,ram_totale,energieParProc,processeurs):
    # Vérification de faisabilité avant de lancer la simulation
    energies_dispo = [int(e) for e in energies["energie_disponible"]]
    energie_necessaire = 0

    for id_proc, (date, duree, ram, priorite, butoir) in processus.items():
        if ram > ram_totale: # ne tiendra jamais en RAM
            return True

    if len(processeurs) == 0: # aucun processeur
        return True
    if max(energies_dispo) < energieParProc: # jamais assez d'énergie pour 1 CPU
        return True

    return False



#-------------------------------------------------------------------------------------------------------------
# Fonction qui execute l'ordonnanceur
#-------------------------------------------------------------------------------------------------------------

"""
Simule un ordonnanceur à priorité, sous contraintes
d'énergie, de nombre de processeurs et de RAM.

Données lues :
- python/ressources/energie.csv : énergie disponible à chaque instant
- python/ressources/processus.csv : id, date de soumission, durée,
    RAM nécessaire, priorité, date butoir
- python/ressources/ressources.json : processeurs, RAM totale,
    énergie consommée par processeur

Déroulement à chaque instant :
1. soumission des nouveaux processus dans la file
2. tri de la file par priorité
3. calcul du nombre de processeurs utilisables
    (énergie disponible // énergie par processeur)
4. exécution, dans l'ordre de priorité, des processus qui tiennent en RAM,
    jusqu'à épuisement des processeurs utilisables
5. un processus dont la durée restante tombe à 0 passe dans les terminés

La simulation s'arrête quand tous les processus sont terminés.

:return: liste de lignes [id, instant, processeur]
"""
def ordonnanceur_priorite(energies_path:str,processus_path:str,ressources_path:str):
    # Extraction des données
    energies = content_csv(energies_path) 
    raw_processus = content_csv(processus_path)
    ressources = ressources_json(ressources_path)


    # Déclaration de variables utile
    processeurs = ressources["processeur"]
    ram_totale = ressources["ramTotale"]
    energieParProc = ressources["energieParProc"]

    processus = {}

    for i in range(len(raw_processus["id_processus"])):
        processus[raw_processus["id_processus"][i]] = [int(raw_processus["date_soumission"][i]),int(raw_processus["duree_execution"][i]),int(raw_processus["ram_necessaire"][i]),int(raw_processus["priorite"][i]),int(raw_processus["date_butoir"][i])]



    terminer = False
    retour = []

    instant = 0
    journer = 0
    processus_fini = {}
    processus_ex = {}
    en_cours = {} 

    terminer = faisabilite(energies,processus,ram_totale,energieParProc,processeurs)


    #Boucle d'execution
    while terminer == False:
        soumission(instant+journer,processus_ex,processus_fini,processus,retour)
        processus_ex = sort_processus(processus_ex)

        energie_dispo = int(energies["energie_disponible"][instant])

        #Vérification du nombre de processeurs possible a faire fonctionner
        nb_possible = energie_dispo // energieParProc
        realiter = min(nb_possible, len(processeurs), len(processus_ex))

        #Execution
        ram_dispo = ram_totale - sum(processus_ex[i][2] for i in en_cours) # Somme de la ram utilisé actuelment 
        cpu_libres = [c for c in processeurs if c not in en_cours.values()] # Récupère les CPUs non utilisé
        actifs = 0

        ids = list(en_cours)

        # Boucle qui fais l'execution des processus déjà en file
        for id_proc in ids:
            if actifs >= nb_possible:      # plus assez d'énergie 
                break
            processus_ex[id_proc][1] -= 1
            retour.append([id_proc, instant + journer, en_cours[id_proc],processus_ex[id_proc][2]])
            actifs += 1
            if processus_ex[id_proc][1] == 0:
                processus_fini[id_proc] = processus_ex.pop(id_proc)
                del en_cours[id_proc]       # CPU et RAM libérés pour l'instant suivant


        idp = list(processus_ex)
        # Boucle qui regarde qui il est possible d'executer et l'execute tout en l'ajoutant dans la file
        for id_proc in idp :
            if actifs >= nb_possible or not cpu_libres: # Pas possible d'executer plus de processus avec les ressources actuel
                break
            if id_proc in en_cours: # Déjà en cours donc rien a faire execution déjà effectuer
                continue
            ram_proc = processus_ex[id_proc][2] 
            if ram_proc <= ram_dispo:       # Si il y a assez de ram pour ce processus alors on le rajoute dans la file et on l'execute
                ram_dispo -= ram_proc # Aloue la RAM
                en_cours[id_proc] = cpu_libres.pop(0) # Aloue le CPU
                processus_ex[id_proc][1] -= 1 # Execution
                retour.append([id_proc, instant + journer, en_cours[id_proc],processus_ex[id_proc][2]]) # Ajout dans l'historique
                actifs += 1
                if processus_ex[id_proc][1] == 0:
                    processus_fini[id_proc] = processus_ex.pop(id_proc)
                    del en_cours[id_proc]

        instant += 1
        if(instant == 24):
            instant = 0
            journer += 24

        terminer = len(processus_fini) == len(processus)

    return retour
    




