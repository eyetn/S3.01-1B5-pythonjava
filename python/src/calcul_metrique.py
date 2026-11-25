from config_extrude import *

"""
Calcule le temps de réponse moyen de l'ordonnancement

Pour chaque processus, le temps de réponse est l'écart entre sa première exécution
(comptée en fin d'intervalle, instant + 1) et sa date de soumission. La valeur
retournée est la moyenne sur tous les processus soumis.

:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
:return: temps de réponse moyen (0 si aucun processus n'a été soumis)
"""
def calcul_temps_reponse_moyen(retour: list):
    temps_reponse_moyen = 0

    soumission = {id:soum for id,soum,cpu,ram in retour if cpu is None}   # Contient chaque date de soumission
    debut = {} # Contient le dictionnaire id, instant+1 de la première execution

    for id,deb,cpu,ram in retour: 
            if id not in debut.keys() and cpu != None: # Récupère le premier tableau contenant l'id de chaque process et donc la première execution
                debut[id] = deb
        
    for k in soumission.keys(): 
        duree = 0
        for ligne in retour: #Calcul du temp de d'execution
            if ligne[0] == k and ligne[2] is not None:
                duree+=1      

        temps_reponse_moyen += debut[k]-soumission[k] # somme de tout les temps de réponse

    if len(soumission) != 0:
        temps_reponse_moyen = temps_reponse_moyen/len(soumission) # Division par le nombre de proc

    return temps_reponse_moyen


"""
Calcule le temps d'attente moyen de l'ordonnancement

Pour chaque processus, le temps d'attente est (date de fin - date de soumission)
moins sa durée d'exécution, c'est-à-dire le temps passé en file sans s'exécuter.
La date de fin est l'instant suivant la dernière exécution. La valeur retournée
est la moyenne sur tous les processus soumis.

:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
:return: temps d'attente moyen (0 si aucun processus n'a été soumis)
"""
def calcul_temps_attente_moyen(retour: list):
    temps_attente_moyen = 0

    soumission = {id:soum for id,soum,cpu,ram in retour if cpu is None}   # Contient chaque date de soumission
    fin = {} # Contient le dictionnaire id, instant+1 de la dernière execution

    for id,fini,cpu,ram in reversed(retour): 
        if id not in fin.keys() and cpu != None: # Récupère le dernier tableau contenant l'id de chaque process et donc la dernière execution
            fin[id] = fini + 1 # + 1 car c'est l'interval et pas l'instant
        
    for k in soumission.keys(): 
        duree = 0
        for ligne in retour: #Calcul du temp de d'execution
            if ligne[0] == k and ligne[2] is not None:
                duree+=1      

        temps_attente_moyen += (fin[k]-soumission[k])-duree # somme de tout les temps d'attente
    if len(soumission) != 0:
        temps_attente_moyen = temps_attente_moyen/len(soumission) # Division par le nombre de proc

    return temps_attente_moyen

"""
Calcule le makespan de l'ordonnancement

Le makespan est l'écart entre la plus grande date de fin (instant suivant la
dernière exécution) et la plus petite date de début (première exécution, comptée
en fin d'intervalle, instant + 1) parmi tous les processus.

:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
:return: makespan (0 si aucun processus ne s'est exécuté)
"""
def calcul_makespan(retour: list):
    makespan = 0
    fin = {} # Contient le dictionnaire id, instant+1 de la dernière execution
    debut = {} # Contient le dictionnaire id, instant+1 de la première execution

    for id,fini,cpu,ram in reversed(retour): 
        if id not in fin.keys() and cpu != None: # Récupère le dernier tableau contenant l'id de chaque process et donc la dernière execution
            fin[id] = fini + 1 # + 1 car c'est l'interval et pas l'instant

    for id,deb,cpu,ram in retour: 
            if id not in debut.keys() and cpu != None: # Récupère le premier tableau contenant l'id de chaque process et donc la première execution
                debut[id] = deb
    if len(fin.values())>0 and len(debut.values())>0:
        makespan = max(fin.values())-min(debut.values())
    return makespan

"""
Calcule l'énergie consommée totale

Chaque ligne d'exécution de retour correspond à un processeur actif pendant un
instant. L'énergie consommée est donc le nombre de lignes d'exécution (lignes de
soumission exclues) multiplié par l'énergie consommée par un processeur, lue dans
le fichier de ressources indiqué par le config.txt.

:param config_path : chemin d'accès vers le fichier config.txt
:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
:return: énergie consommée totale
:raises FileNotFoundError: si le config.txt ou le fichier de ressources n'existe pas
"""
def calcul_energie_consommee_totale(config_path:str,retour:list):
    energie_consommee_totale = 0
    config = config_txt(config_path)
    energieParProc = ressources_json(config["fichier_ressources"][0])["energieParProc"]
    soumission = {id:soum for id,soum,cpu,ram in retour if cpu is None}   # Contient chaque date de soumission

    energie_consommee_totale = (len(retour)-len(soumission.keys()))*energieParProc
    return energie_consommee_totale

"""
Calcule l'énergie disponible totale sur la durée de simulation

Additionne l'énergie disponible de chaque instant, depuis la première date de
soumission jusqu'à la fin du dernier processus. Le profil d'énergie du fichier
energie.csv est relu depuis le début chaque fois que sa fin est atteinte.

:param config_path : chemin d'accès vers le fichier config.txt
:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
:return: énergie disponible totale (0 si aucune simulation n'a eu lieu)
:raises FileNotFoundError: si le config.txt ou le fichier d'énergie n'existe pas
"""
def calcul_energie_dispo_totale(config_path:str,retour:list):
    config = config_txt(config_path)
    energies = content_csv(config["energie"][0])
    energie_disponible_totale = 0

    soumission = {id:soum for id,soum,cpu,ram in retour if cpu is None}   # Contient chaque date de soumission
    fin = {} # Contient le dictionnaire id, instant+1 de la dernière execution

    for id,fini,cpu,ram in reversed(retour): 
        if id not in fin.keys() and cpu != None: # Récupère le dernier tableau contenant l'id de chaque process et donc la dernière execution
            fin[id] = fini + 1 # + 1 car c'est l'interval et pas l'instant
    
    if(len(soumission)>0 and len(fin.values())>0): # Regarde si il y a eu simulation
        continuer = True 
        instant = min(soumission.values()) # Défini le début de l'interval de la simulation
        cpt = instant
        while continuer:
            energie_disponible_totale+=int(energies["energie_disponible"][instant])
            if cpt == max(fin.values())-1: # Fin de l'interval
                continuer = False
            instant+=1
            if instant == 24:
                instant = 0
            cpt += 1
    return energie_disponible_totale