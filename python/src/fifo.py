from fonction_communes import *

def ordonnancer(processus, ressources, energie):
    dispo = energie_par_instant(energie)
    derniere = derniere_soumission(processus)
    etat = creer_etat(ressources)
    file_att = []
    allocations = []
    ram = 0
    t = 0
    fini = False
    while fini == False:
        ram = liberer(etat, processus, ram, allocations, t)
        ajouter_arrivees(processus, file_att, t)
        maxi = cpu_alimentables(dispo, t, ressources)
        for cpu in etat:
            if etat[cpu] is None and nb_occupes(etat) < maxi:
                # le premier de la file dont la RAM passe
                choisi = None
                for i in file_att:
                    if ram_ok(i, processus, ram, ressources):
                        choisi = i
                        break
                if choisi is not None:
                    ram = demarrer(etat, file_att, processus, cpu, choisi, t, ram)

        if t > derniere and len(file_att) == 0 and nb_occupes(etat) == 0:
            fini = True
        if t > 1000:    # sécurité contre la boucle infinie
            fini = True
        t = t + 1
    return allocations