import csv
import json

#-------------------------------------------------------------------------------------------------------------
# Extrude de config.txt
#-------------------------------------------------------------------------------------------------------------
DEFAULT_CONFIG_PATH = "python/ressources/config.txt"

"""
Lit la configuration générale de l'ordonnanceur.

Clés lues dans le fichier : fichier_processus, fichier_ressources,
algorithmes.

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire de la configuration ; la valeur de "algorithmes" est une liste de chaînes
:raises FileNotFoundError: si le fichier n'existe pas
"""
def config_ordonnanceur(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row and row[0][0].strip() !="#":
                match row[0].strip():
                    case "fichier_processus":
                        config["fichier_processus"] = row[1].strip()
                    case "fichier_ressources":
                        config["fichier_ressources"] = row[1].strip()
                    case "algorithmes":
                        config["algorithmes"] = [e for e in row[1].strip().split()]
    return config

"""
Lit la configuration des fichiers de sortie pour FIFO.

Clés lues dans le fichier : fichier_global_FIFO,
fichier_allocations_FIFO.

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire des chemins des fichiers de sortie FIFO
:raises FileNotFoundError: si le fichier n'existe pas
"""

def config_sortieFIFO(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row and row[0][0].strip() !="#":
                match row[0].strip():
                    case "fichier_global_FIFO":
                        config["fichier_global_FIFO"] = row[1].strip()
                    case "fichier_allocations_FIFO":
                        config["fichier_allocations_FIFO"] = row[1].strip()
    return config

"""Lit la configuration des fichiers de sortie pour Round Robin.

Clés lues dans le fichier : fichier_global_RoundRobin,
fichier_allocations_RoundRobin.

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire des chemins des fichiers de sortie Round Robin
:raises FileNotFoundError: si le fichier n'existe pas
"""
def config_sortieRR(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row and row[0][0].strip() !="#":
                match row[0].strip():
                    case "fichier_global_RoundRobin":
                        config["fichier_global_RoundRobin"] = row[1].strip()
                    case "fichier_allocations_RoundRobin":
                        config["fichier_allocations_RoundRobin"] = row[1].strip()
    return config

"""
Lit la configuration des fichiers de sortie pour EDF.

Clés lues dans le fichier : fichier_global_EDF,
fichier_allocations_EDF.

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire des chemins des fichiers de sortie EDF
:raises FileNotFoundError: si le fichier n'existe pas
"""
def config_sortieEDF(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row and row[0][0].strip() !="#":
                match row[0].strip():
                    case "fichier_global_EDF":
                        config["fichier_global_EDF"] = row[1].strip()
                    case "fichier_allocations_EDF":
                        config["fichier_allocations_EDF"] = row[1].strip()
    return config


"""
Lit la configuration du fichier de métriques commun.

Clé lue dans le fichier : fichier_metriques.

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire contenant le chemin du fichier de métriques
:raises FileNotFoundError: si le fichier n'existe pas
"""
def config_metrique_commun(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row and row[0].startswith("#"):
                match row[0].strip():
                    case "fichier_metriques":
                        config["fichier_metriques"] = row[1].strip()
    return config


"""
Lit le quantum de l'ordonnanceur.

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire des paramètres ; la valeur est une liste si elle
    contient plusieurs mots, une chaîne sinon
:raises FileNotFoundError: si le fichier n'existe pas
"""
def config_quantum(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row:
                match row[0].strip():
                    case "quantum":
                        config["quantum"] = row[1].strip()
    return config



"""
Lit le fichier en entrer au global

Fais l'association cle = valeur

:param config_path: chemin d'accès vers le fichier config.txt
:return: dictionnaire des paramètres ; la valeur est une liste si elle
    contient plusieurs mots, une chaîne sinon
:raises FileNotFoundError: si le fichier n'existe pas
"""
def config_txt(config_path=DEFAULT_CONFIG_PATH) -> dict:
    config = {}
    with open(config_path, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='=', quotechar='\n')
        for row in spamreader:
            if row:
                if row[1].split():
                    config[row[0].strip()] = [e for e in row[1].strip().split()]
                else:
                    config[row[0].strip()] = row[1].strip()
    return config


#-------------------------------------------------------------------------------------------------------------
# Extrude de .json
#-------------------------------------------------------------------------------------------------------------

"""
Lit le fichier .json en entrer 

Fais l'association cle = valeur

:param ressources_pathh: chemin d'accès vers le fichier .json
:return: dictionnaire des données 
:raises FileNotFoundError: si le fichier n'existe pas
"""
def ressources_json(ressources_path: str) -> dict:
    with open(ressources_path, 'r') as file:
        ressources = json.load(file)
    return ressources


#-------------------------------------------------------------------------------------------------------------
# Extrude de .csv
#-------------------------------------------------------------------------------------------------------------

"""
Fonction utilitaire pour content_csv

Récupère les labels du fichiers csv

:param ressources_path: chemin d'accès vers le fichier .csv
:return: list de lables
:raises FileNotFoundError: si le fichier n'existe pas
"""
def label_csv(ressources_path: str) -> list:
    with open(ressources_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        labels = next(reader)
        return labels
    
"""
Lit le fichier .csv en entrer

Fais l'association cle(labels) = [valeur]

:param ressources_path: chemin d'accès vers le fichier .csv
:return: dict des données du csv
:raises FileNotFoundError: si le fichier n'existe pas
"""
def content_csv(ressources_path: str) -> dict:
    labels = label_csv(ressources_path)
    content = {k: [] for k in labels}
    with open(ressources_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for ligne in reader:
            for label, valeur in zip(labels, ligne):
                content[label].append(valeur)
    return content


print(config_quantum())