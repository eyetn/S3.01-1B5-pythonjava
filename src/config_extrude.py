import csv

"""
# Configuration de l'ordonnanceur
fichier_processus
fichier_ressources
algorithmes

@param config_path: str chemin d'accès vers le fichier config.txt
@return config: dict qui contient la configuration de l'ordonnanceur

"""
def config_ordonnanceur(config_path: str) -> dict:
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
                    case _:
                        print(row)
    return config
