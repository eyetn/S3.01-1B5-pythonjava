import csv
from calcul_metrique import *
import os

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

"""
Écrit les métriques globales d'un ordonnancement dans le fichier de métriques commun

Calcule les métriques du résultat de l'ordonnancement : temps d'attente moyen,
temps de réponse moyen, makespan, énergie consommée totale, énergie disponible
totale et taux d'utilisation (énergie consommée / énergie disponible). Elles sont
écrites dans le fichier indiqué par la clé fichier_metriques du config.txt, sous
forme d'une ligne : id, type d'ordonnanceur, puis les métriques.

L'id s'incrémente à chaque ligne ajoutée, en partant de 0. L'en-tête n'est écrit
que si le fichier est créé ou écrasé.

:param config_path : chemin d'accès vers le fichier config.txt
:param retour : liste de lignes [id, instant, processeur, ram] ; processeur vaut None
    pour une ligne de soumission
:param type : nom de l'ordonnanceur écrit dans la 2e colonne (ex : "Priorite", "FIFO")
:param ecrase : False (par défaut) ajoute la ligne à la fin du fichier ; True écrase
    le fichier avec l'en-tête et la nouvelle ligne seule
:raises FileNotFoundError: si le config.txt ou un des fichiers d'entrée n'existe pas
"""
def metriques_global(config_path: str, retour: list, type:str, ecrase=False ):
    # Métriques :
    temps_reponse_moyen = calcul_temps_reponse_moyen(retour)
    temps_attente_moyen = calcul_temps_attente_moyen(retour)
    makespan = calcul_makespan(retour)
    energie_consommee_totale = calcul_energie_consommee_totale(config_path,retour)
    energie_disponible_totale = calcul_energie_dispo_totale(config_path,retour)
    taux_utilisation = 0
    if(energie_disponible_totale!=0):
        taux_utilisation = round(energie_consommee_totale/energie_disponible_totale,3)

    # Sortie 
    config = config_txt(config_path)
    sortie = config["fichier_metriques"][0]

    entete = ["id", "type_ordonnanceur", "temps_attente_moyen", "temps_reponse_moyen",
              "makespan", "energie_consommee_totale", "energie_disponible_totale",
              "taux_utilisation"]

    # Prochain id : dernier id du fichier + 1 (0 si le fichier n'existe pas ou si on écrase)
    prochain_id = 0
    if not ecrase and os.path.exists(sortie):
        with open(sortie, newline="", encoding="utf-8") as f:
            ids = [int(l["id"]) for l in csv.DictReader(f)]
        if ids:
            prochain_id = max(ids) + 1

    ligne = [prochain_id, type, temps_attente_moyen,temps_reponse_moyen,
             makespan, energie_consommee_totale, energie_disponible_totale,
             taux_utilisation]

    nouveau = ecrase or not os.path.exists(sortie) 
    with open(sortie, "w" if ecrase else "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if nouveau:
            writer.writerow(entete)             # en-tête seulement pour un fichier neuf
        writer.writerow(ligne)