import csv

"""
Écrit le fichier d'informations globales des processus

Une ligne par processus : identifiant, date de soumission, date de début
d'exécution (première date où le processus a obtenu un processeur), date de fin
d'exécution (instant suivant la dernière exécution) et RAM demandée et utilisée.

:param output_path : chemin du fichier csv à écrire
:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
"""
def global_info(output_path: str, retour: list):
    soumissions = {}   # id -> date de soumission
    executions = {}    # id -> liste des instants d'exécution
    rams = {}          # id -> RAM

    for id_proc, instant, cpu, ram in retour: # Récupère par Proc les instants où ils sont executer
        rams[id_proc] = ram
        if cpu is None: # Si le tableau a en cpu None ca veux dire que cest le moment de soumission
            soumissions[id_proc] = instant
            executions[id_proc] = []
        else: # Sinon on ajoute l'instant
            executions[id_proc].append(instant)

    lignes = []
    for id_proc, instants in executions.items():
        if not instants:
            continue
        lignes.append({
            "id_processus": id_proc,
            "date_soumission": soumissions[id_proc],
            "date_debut": instants[0],
            "date_fin": instants[-1] + 1,
            "ram": rams[id_proc],
        })

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id_processus", "date_soumission", "date_debut", "date_fin", "ram"])
        writer.writeheader()
        writer.writerows(lignes)


"""
Écrit le fichier d'informations détaillées des allocations processeurs

Une ligne par période d'exécution continue d'un processus sur un processeur :
identifiant du processus, date de début sur le processeur, date de fin
(instant suivant la dernière exécution) et identifiant du processeur.
Si un processus est interrompu (manque d'énergie) puis reprend, il a
plusieurs lignes.

:param output_path : chemin du fichier csv à écrire
:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission (ignorée ici)
"""
def detail_info(output_path: str, retour: list):
    periodes = []        # liste de dictionnaires, une par période

    for id_proc, instant, cpu, ram in retour:
        cpt = 0
        index = None
        if cpu is None:                  # ligne de soumission : pas une exécution
            continue
        for periode in periodes: # Parcours les pariodes a la recherche de la derniere pour chaque Proc
            if periode.get("id_processus") == id_proc:
                index = cpt
            cpt+=1

        if index is not None and periodes[index].get("date_fin")==instant: 
            periodes[index]["date_fin"] = instant+1
        else:
            p = {
                "id_processus": id_proc,
                "date_debut": instant,
                "date_fin": instant + 1,
                "id_processeur": cpu,
            }
            periodes.append(p)
       


    periodes.sort(key=lambda p: (p["date_debut"], p["id_processus"]))

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id_processus", "date_debut", "date_fin", "id_processeur"])
        writer.writeheader()
        writer.writerows(periodes)

def metriques_global(output_path: str, retour: list):

    soumission = {id:soum for id,soum,cpu,ram in retour if cpu is None}   # Contient chaque date de soumission
    fin = {} # Contient le dictionnaire id, instant+1 de la dernière execution
    debut = {} # Contient le dictionnaire id, instant+1 de la première execution
    makespan = None

    for id,fini,cpu,ram in reversed(retour): 
        if id not in fin.keys() and cpu != None: # Récupère le dernier tableau contenant l'id de chaque process et donc la dernière execution
            fin[id] = fini + 1 # + 1 car c'est l'interval et pas l'instant

    for id,deb,cpu,ram in retour: 
            if id not in debut.keys() and cpu != None: # Récupère le premier tableau contenant l'id de chaque process et donc la première execution
                debut[id] = deb + 1 # + 1 car c'est l'interval et pas l'instant
        
    temps_reponse_moyen = 0
    temps_attente_moyen = 0
    for k in soumission.keys(): 
        duree = 0
        for ligne in retour: #Calcul du temp de d'execution
            if ligne[0] == k and ligne[2] is not None:
                duree+=1      

        temps_attente_moyen += (fin[k]-soumission[k])-duree # somme de tout les temps d'attente
        temps_reponse_moyen += debut[k]-soumission[k] # somme de tout les temps de réponse

    temps_attente_moyen = temps_attente_moyen/len(soumission) # Division par le nombre de proc
    temps_reponse_moyen = temps_reponse_moyen/len(soumission) 
    makespan = max(fin.values())-min(debut.values())

    #energie_consommee_totale = (len(retour)-len(soumission.keys()))*energieParProc
    #

    print(makespan)
