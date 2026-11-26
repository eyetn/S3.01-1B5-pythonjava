
import os
import sys

from config_extrude import *
from EDF import ordonnancer as ordonnancer_edf
from fifo import ordonnancer as ordonnancer_fifo
from priorite import ordonnanceur_priorite
from roundrobin import RoundRobin
from script_ecriture import detail_info, global_info, metriques_global

Dossier_src = os.path.dirname(os.path.abspath(__file__))
Racine = os.path.dirname(os.path.dirname(Dossier_src))
sys.path.insert(0, Dossier_src)


def chemin(p, sortie=False):
    c = p if os.path.isabs(p) else os.path.join(Racine, p)
    if sortie:
        os.makedirs(os.path.dirname(c), exist_ok=True)
    elif not os.path.isfile(c):
        raise FileNotFoundError(f"Fichier introuvable : {c}")
    return c


def formater(proc, allocs, intervalles=False):
    ram = dict(zip(proc["id_processus"], map(int, proc["ram_necessaire"])))
    executions = []

    if intervalles:
        for pid, debut, fin, cpu in allocs:
            executions.extend(
                (pid, instant, cpu, ram[pid])
                for instant in range(int(debut), int(fin))
            )
    else:
        executions = [
            (pid, int(instant), cpu, int(ram_proc))
            for pid, instant, cpu, ram_proc in allocs
            if cpu is not None
        ]

    processus_alloues = {pid for pid, _, _, _ in executions}
    soumissions = [
        (pid, int(date), None, ram[pid])
        for pid, date in zip(proc["id_processus"], proc["date_soumission"])
        if pid in processus_alloues
    ]

    return soumissions + executions


def main(config_path="python/ressources/config.txt"):
    config_path = chemin(config_path)
    cfg = config_ordonnanceur(config_path)

    res_path, proc_path, en_path = (
        chemin(cfg[k]) for k in ("fichier_ressources", "fichier_processus", "energie")
    )

    ressources = ressources_json(res_path)
    processus = content_csv(proc_path)
    energies = content_csv(en_path)

    energie = [
        {"instant": int(i), "energie_disponible": int(e)}
        for i, e in zip(energies["instant"], energies["energie_disponible"])
    ]

    liste = [dict(zip(processus, vals)) for vals in zip(*processus.values())]

    premier = True

    for algo in ",".join(cfg["algorithmes"]).replace(" ", "").upper().split(","):
        
        if algo == "FIFO":
            s = config_sortieFIFO(config_path)
            allocations = ordonnancer_fifo(processus, ressources, energies)
            nom = "FIFO"

        elif algo == "RR":
            s = config_sortieRR(config_path)
            q = int(config_quantum(config_path)["quantum"])
            allocations = RoundRobin(liste, ressources, energie, q).ordonnancer()
            nom = "RoundRobin"

        elif algo in ("EDF", "EFF"):
            s = config_sortieEDF(config_path)
            allocations = ordonnancer_edf(processus, ressources, energies)
            nom = "EDF"

        elif algo == "PRIORITE":
            s = config_sortiePriorite(config_path)
            allocations = ordonnanceur_priorite(en_path, proc_path, res_path)
            nom = "Priorite"

        else:
            continue

        s = {k: chemin(v, sortie=True) for k, v in s.items()}

        r = formater(
            processus,
            allocations,
            intervalles=nom == "RoundRobin",
        )

        global_info(s[f"fichier_global_{nom}"], r)
        detail_info(s[f"fichier_allocations_{nom}"], r)
        metriques_global(config_path, r, nom,premier)
        premier = False

if __name__ == "__main__":
        inputs = os.path.join(Racine, "python", "inputs")
        for dossier in sorted(os.listdir(inputs)):
            cfg = os.path.join(inputs, dossier, "config.txt")
            if os.path.isfile(cfg):
                print(dossier)
                main(cfg)
