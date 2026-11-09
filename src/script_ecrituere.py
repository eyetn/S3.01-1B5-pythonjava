from config_extrude import *
import csv

"""
identifiant du processus, la date de soumission du processus, la date
de début d’exécution (première date à laquelle le processus a obtenu le
processeur), la date de fin d’exécution du processus, la RAM demandée et utilisée
par le processus
"""

def global_info_FIFO(config_path="ressources/config.txt"):
    sorties = config_sortieFIFO(config_path)

    # Récupération des infos par l'exécution du programme de l'ordonnanceur
    # exemple rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    with open("fichiers_sortie/" + sorties["fichier_global_FIFO"], "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id","name"]) #Idem a changer
        writer.writeheader()
        writer.writerows(rows)
    

