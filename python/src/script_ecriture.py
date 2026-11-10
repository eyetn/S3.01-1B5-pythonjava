from python.src.config_extrude import *
import csv

DEFAULT_CONFIG_PATH = "python/ressources/config.txt"

"""
identifiant du processus, la date de soumission du processus, la date
de début d’exécution (première date à laquelle le processus a obtenu le
processeur), la date de fin d’exécution du processus, la RAM demandée et utilisée
par le processus
"""

def global_info_FIFO(config_path=DEFAULT_CONFIG_PATH):
    sorties = config_sortieFIFO(config_path)

    # Récupération des infos par l'exécution du programme de l'ordonnanceur
    # Exemple 
    rows = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob2"}]

    with open("fichiers_sortie/" + sorties["fichier_global_FIFO"], "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id","name"]) #Idem a changer
        writer.writeheader()
        writer.writerows(rows)
    

global_info_FIFO()
