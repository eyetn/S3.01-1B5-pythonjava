import unittest

from roundrobin import *


# ---------- outils pour construire les données de test ----------

def proc(id_, date, duree, ram=1):
    return {
        "id_processus": id_,
        "date_soumission": date,
        "duree_execution": duree,
        "ram_necessaire": ram,
    }


def ressources(nb_cpu=1, energie_par_proc=10, ram_totale=100):
    return {
        "processeur": ["CPU%d" % (i + 1) for i in range(nb_cpu)],
        "energieParProc": energie_par_proc,
        "ramTotale": ram_totale,
    }


def energie(valeur=1000, jusqu_a=1100):
    return [{"instant": t, "energie_disponible": valeur} for t in range(jusqu_a)]


def lancer(processus, res, ener, quantum=2):
    return RoundRobin(processus, res, ener, quantum).ordonnancer()


def sans_cpu(allocations):
    """[(id, debut, fin), ...] pour comparer sans se soucier du nom du CPU."""
    return [(a[0], a[1], a[2]) for a in allocations]


def temps_total(allocations, id_):
    return sum(fin - debut for (i, debut, fin, _) in allocations if i == id_)


def se_chevauchent(a, b):
    return a[1] < b[2] and b[1] < a[2]


# ---------- tests ----------

class TestRoundRobin(unittest.TestCase):

    def test_aucun_processus(self):
        self.assertEqual(lancer([], ressources(), energie()), [])

    def test_processus_plus_court_que_le_quantum(self):
        alloc = lancer([proc("P1", 0, 1)], ressources(), energie(), quantum=3)
        self.assertEqual(sans_cpu(alloc), [("P1", 0, 1)])

    def test_processus_decoupe_en_tranches(self):
        alloc = lancer([proc("P1", 0, 5)], ressources(), energie(), quantum=2)
        self.assertEqual(sans_cpu(alloc),
                         [("P1", 0, 2), ("P1", 2, 4), ("P1", 4, 5)])

    def test_alternance_entre_deux_processus(self):
        procs = [proc("P1", 0, 3), proc("P2", 0, 3)]
        alloc = lancer(procs, ressources(), energie(), quantum=2)
        self.assertEqual(sans_cpu(alloc),
                         [("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 5), ("P2", 5, 6)])

    def test_quantum_grand_se_comporte_comme_fifo(self):
        procs = [proc("P1", 0, 3), proc("P2", 0, 2)]
        alloc = lancer(procs, ressources(), energie(), quantum=100)
        self.assertEqual(sans_cpu(alloc), [("P1", 0, 3), ("P2", 3, 5)])

    def test_quantum_de_un(self):
        procs = [proc("P1", 0, 2), proc("P2", 0, 2)]
        alloc = lancer(procs, ressources(), energie(), quantum=1)
        self.assertEqual(sans_cpu(alloc),
                         [("P1", 0, 1), ("P2", 1, 2), ("P1", 2, 3), ("P2", 3, 4)])

    def test_temps_total_execute_egal_duree(self):
        procs = [proc("P1", 0, 7), proc("P2", 1, 4), proc("P3", 2, 5)]
        alloc = lancer(procs, ressources(nb_cpu=2), energie(), quantum=3)
        for p in procs:
            self.assertEqual(temps_total(alloc, p["id_processus"]),
                             p["duree_execution"])

    def test_aucun_demarrage_avant_la_soumission(self):
        procs = [proc("P1", 0, 3), proc("P2", 5, 2), proc("P3", 8, 4)]
        alloc = lancer(procs, ressources(nb_cpu=2), energie(), quantum=2)
        soumission = {p["id_processus"]: p["date_soumission"] for p in procs}
        for (i, debut, fin, _) in alloc:
            self.assertGreaterEqual(debut, soumission[i])

    def test_arrivee_avant_la_fin_de_tranche_passe_devant_le_preempte(self):
        # P2 arrive à t=1, P1 est préempté à t=2 -> P2 doit passer avant P1
        procs = [proc("P1", 0, 4), proc("P2", 1, 2)]
        alloc = lancer(procs, ressources(), energie(), quantum=2)
        self.assertEqual(sans_cpu(alloc),
                         [("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 6)])

    def test_arrivee_pile_a_la_fin_de_tranche_passe_devant_le_preempte(self):
        # P2 arrive exactement à t=2, au moment où P1 est préempté
        procs = [proc("P1", 0, 4), proc("P2", 2, 2)]
        alloc = lancer(procs, ressources(), energie(), quantum=2)
        self.assertEqual(sans_cpu(alloc),
                         [("P1", 0, 2), ("P2", 2, 4), ("P1", 4, 6)])

    def test_cpu_inactif_puis_demarrage_a_l_arrivee(self):
        alloc = lancer([proc("P1", 3, 2)], ressources(), energie(), quantum=2)
        self.assertEqual(sans_cpu(alloc), [("P1", 3, 5)])

    def test_deux_cpu_en_parallele(self):
        procs = [proc("P1", 0, 2), proc("P2", 0, 2)]
        alloc = lancer(procs, ressources(nb_cpu=2, energie_par_proc=50),
                       energie(valeur=100), quantum=2)
        self.assertEqual(sorted(sans_cpu(alloc)), [("P1", 0, 2), ("P2", 0, 2)])
        self.assertEqual(len(set(a[3] for a in alloc)), 2)  # 2 CPU différents

    def test_limite_d_energie_empeche_le_parallelisme(self):
        # énergie pour un seul processeur à la fois, même avec 2 CPU
        procs = [proc("P1", 0, 4), proc("P2", 0, 4)]
        alloc = lancer(procs, ressources(nb_cpu=2, energie_par_proc=50),
                       energie(valeur=50), quantum=2)
        for i in range(len(alloc)):
            for j in range(i + 1, len(alloc)):
                self.assertFalse(se_chevauchent(alloc[i], alloc[j]))
        self.assertEqual(temps_total(alloc, "P1"), 4)
        self.assertEqual(temps_total(alloc, "P2"), 4)

    def test_energie_insuffisante_rien_ne_demarre(self):
        # 10 d'énergie dispo pour 50 par processeur -> aucun CPU utilisable
        alloc = lancer([proc("P1", 0, 2)],
                       ressources(energie_par_proc=50), energie(valeur=10))
        self.assertEqual(alloc, [])

    def test_ram_empeche_l_execution_simultanee(self):
        procs = [proc("P1", 0, 4, ram=6), proc("P2", 0, 4, ram=6)]
        alloc = lancer(procs, ressources(nb_cpu=2, ram_totale=10),
                       energie(), quantum=2)
        for i in range(len(alloc)):
            for j in range(i + 1, len(alloc)):
                self.assertFalse(se_chevauchent(alloc[i], alloc[j]))
        self.assertEqual(temps_total(alloc, "P1"), 4)
        self.assertEqual(temps_total(alloc, "P2"), 4)

    def test_ram_suffisante_permet_l_execution_simultanee(self):
        procs = [proc("P1", 0, 2, ram=6), proc("P2", 0, 2, ram=4)]
        alloc = lancer(procs, ressources(nb_cpu=2, ram_totale=10),
                       energie(), quantum=2)
        self.assertEqual(sorted(sans_cpu(alloc)), [("P1", 0, 2), ("P2", 0, 2)])

    def test_processus_trop_gourmand_en_ram_ne_bloque_pas_les_autres(self):
        procs = [proc("P1", 0, 2, ram=50), proc("P2", 0, 2, ram=1)]
        alloc = lancer(procs, ressources(ram_totale=10), energie(), quantum=2)
        self.assertEqual(sans_cpu(alloc), [("P2", 0, 2)])

    def test_un_cpu_ne_fait_jamais_deux_choses_a_la_fois(self):
        procs = [proc("P%d" % i, i, 3 + i) for i in range(5)]
        alloc = lancer(procs, ressources(nb_cpu=2), energie(), quantum=2)
        for cpu in ("CPU1", "CPU2"):
            sur_cpu = [a for a in alloc if a[3] == cpu]
            for i in range(len(sur_cpu)):
                for j in range(i + 1, len(sur_cpu)):
                    self.assertFalse(se_chevauchent(sur_cpu[i], sur_cpu[j]))

    def test_aucune_tranche_ne_depasse_le_quantum(self):
        procs = [proc("P1", 0, 9), proc("P2", 0, 6)]
        alloc = lancer(procs, ressources(), energie(), quantum=3)
        for (_, debut, fin, _) in alloc:
            self.assertLessEqual(fin - debut, 3)

    def test_quantum_par_defaut(self):
        ordo = RoundRobin([proc("P1", 0, 5)], ressources(), energie())
        self.assertEqual(ordo.quantum, 2)


if __name__ == "__main__":
    unittest.main()