from python.src.config_extrude import *

# un dictionnaire {cpu: None} (None = libre)
def creer_etat(ressources):
    etat = {}
    for cpu in ressources["processeur"]:
        etat[cpu] = None
    return etat

# énergie disponible à chaque instant : {instant: énergie}
def energie_par_instant(energie):
    dispo = {}
    for k in range(len(energie["instant"])):
        instant = int(energie["instant"][k])
        dispo[instant] = int(energie["energie_disponible"][k])
    return dispo

# plus grande date de soumission
def derniere_soumission(processus):
    derniere = 0
    for i in range(len(processus["id_processus"])):
        if int(processus["date_soumission"][i]) > derniere:
            derniere = int(processus["date_soumission"][i])
    return derniere

# nombre de CPU occupés
def nb_occupes(etat):
    n = 0
    for cpu in etat:
        if etat[cpu] is not None:
            n = n + 1
    return n

# nombre de CPU que l'énergie permet d'alimenter à l'instant t
def cpu_alimentables(dispo, t, ressources):
    if t in dispo:
        return dispo[t] // ressources["energieParProc"]
    return 0

# permet de savoir si le processus i passe en ram
def ram_ok(i, processus, ram, ressources):
    return int(processus["ram_necessaire"][i]) <= ressources["ramTotale"] - ram

# libère les CPU dont le processus se termine à t et renvoie la nouvelle RAM
def liberer(etat, processus, ram, allocations, t):
    for cpu in etat:
        if etat[cpu] is not None:
            i = etat[cpu][0]
            debut = etat[cpu][1]
            fin = etat[cpu][2]
            if fin == t:
                allocations.append((processus["id_processus"][i], debut, fin, cpu))
                ram = ram - int(processus["ram_necessaire"][i])
                etat[cpu] = None
    return ram

# ajoute dans la file les numéros des processus soumis à t
def ajouter_arrivees(processus, file_att, t):
    for i in range(len(processus["id_processus"])):
        if int(processus["date_soumission"][i]) == t:
            file_att.append(i)

# lance le processus numéro i sur le cpu, renvoie la nouvelle RAM
def demarrer(etat, file_att, processus, cpu, i, t, ram):
    file_att.remove(i)
    etat[cpu] = (i, t, t + int(processus["duree_execution"][i]))
    ram = ram + int(processus["ram_necessaire"][i])
    return ram
