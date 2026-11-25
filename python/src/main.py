import os
import sys

from config_extrude import *
from EDF import ordonnancer as ordonnancer_edf
from fifo import ordonnancer as ordonnancer_fifo
from priorite import ordonnanceur_priorite
from roundrobin import RoundRobin
from script_ecriture import detail_info, global_info

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


def formater(proc, allocs):
    ram = dict(zip(proc["id_processus"], map(int, proc["ram_necessaire"])))
    res = [(i, int(d), None, ram[i])
           for i, d in zip(proc["id_processus"], proc["date_soumission"])]
    for pid, debut, fin, cpu in allocs:
        res += [(pid, t, cpu, ram[pid]) for t in range(int(debut), int(fin))]
    return res


def main(config_path="python/ressources/config.txt"):
    config_path = chemin(config_path)
    cfg = config_ordonnanceur(config_path)
    res_path, proc_path, en_path = (chemin(cfg[k], sortie=True  ) for k in
                                    ("fichier_ressources", "fichier_processus", "energie"))
    ressources = ressources_json(res_path)
    processus = content_csv(proc_path)
    energies = content_csv(en_path)
    energie = [{"instant": int(i), "energie_disponible": int(e)}
               for i, e in zip(energies["instant"], energies["energie_disponible"])]
    liste = [dict(zip(processus, vals)) for vals in zip(*processus.values())]

    

    for algo in ",".join(cfg["algorithmes"]).replace(" ", "").upper().split(","):
        if algo == "FIFO":
            s = {k: chemin(v,sortie=True) for k, v in config_sortieFIFO(config_path).items()}
            r = formater(processus, ordonnancer_fifo(processus, ressources, energies))
            nom = "FIFO"
        elif algo == "RR":
            s = {k: chemin(v,sortie=True) for k, v in config_sortieRR(config_path).items()}
            q = int(config_quantum(config_path)["quantum"])
            r = formater(processus, RoundRobin(liste, ressources, energie, q).ordonnancer())
            nom = "RoundRobin"
        elif algo in ("EDF", "EFF"):
            s = {k: chemin(v,sortie=True) for k, v in config_sortieEDF(config_path).items()}
            r = formater(processus, ordonnancer_edf(processus, ressources, energies))
            nom = "EDF"
        elif algo == "PRIORITE":
            s = {k: chemin(v,sortie=True) for k, v in config_sortiePriorite(config_path).items()}
            r = ordonnanceur_priorite(en_path, proc_path, res_path)
            nom = "Priorite"
        else:
            continue
        global_info(s[f"fichier_global_{nom}"], r)
        detail_info(s[f"fichier_allocations_{nom}"], r)


if __name__ == "__main__":
      if len(sys.argv) > 1:
        # un seul test : python main.py python/inputs/Test2/config.txt
        main(sys.argv[1])
      else:
        # sans argument : tous les tests de python/inputs/
        inputs = os.path.join(Racine, "python", "inputs")
        for dossier in sorted(os.listdir(inputs)):
            cfg = os.path.join(inputs, dossier, "config.txt")
            if os.path.isfile(cfg):
                print(f"{dossier}")
                main(cfg)