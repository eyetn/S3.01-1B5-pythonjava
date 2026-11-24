from fonction_communes import *


def ordonnancer(processus, ressources, energie):
    dispo = energie_par_instant(energie)
    derniere = derniere_soumission(processus)
    etat = creer_etat(ressources)
    file_att = []
    allocations = []
    ram = 0
    t = 0

    while True:
        ram = liberer(etat, processus, ram, allocations, t)
        ajouter_arrivees(processus, file_att, t)

        file_att.sort(key=lambda i: int(processus["date_butoir"][i]))
        maxi = cpu_alimentables(dispo, t, ressources)

        for cpu in etat:
            if etat[cpu] is None and nb_occupes(etat) < maxi:
                choisi = None

                for i in file_att:
                    if ram_ok(i, processus, ram, ressources):
                        choisi = i
                        break

                if choisi is not None:
                    ram = demarrer(
                        etat, file_att, processus, cpu, choisi, t, ram
                    )

        if t > derniere and len(file_att) == 0 and nb_occupes(etat) == 0:
            break

        if t > 1000:
            break

        t += 1

    return allocations

