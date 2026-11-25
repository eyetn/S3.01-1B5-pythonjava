import unittest

from EDF import ordonnancer


def processus(entries):
    return {
        "id_processus": [entry[0] for entry in entries],
        "date_soumission": [str(entry[1]) for entry in entries],
        "duree_execution": [str(entry[2]) for entry in entries],
        "ram_necessaire": [str(entry[3]) for entry in entries],
        "date_butoir": [str(entry[4]) for entry in entries],
    }


def ressources(nb_cpu=1, ram_totale=100, energie_par_proc=10):
    return {
        "processeur": ["CPU%d" % i for i in range(1, nb_cpu + 1)],
        "ramTotale": ram_totale,
        "energieParProc": energie_par_proc,
    }


def energie(valeur=100, jusqu_a=100):
    return {
        "instant": [str(t) for t in range(jusqu_a)],
        "energie_disponible": [str(valeur) for _ in range(jusqu_a)],
    }


class TestEDF(unittest.TestCase):

    def test_aucun_processus(self):
        allocations = ordonnancer(
            processus([]), ressources(), energie()
        )
        self.assertEqual(allocations, [])

    def test_processus_avec_echeance_plus_proche_passe_en_premier(self):
        procs = processus([
            ("P1", 0, 3, 10, 20),
            ("P2", 0, 2, 10, 10),
        ])

        allocations = ordonnancer(procs, ressources(), energie())

        self.assertEqual(allocations, [
            ("P2", 0, "CPU1", 10),
            ("P2", 1, "CPU1", 10),
            ("P1", 2, "CPU1", 10),
            ("P1", 3, "CPU1", 10),
            ("P1", 4, "CPU1", 10),
        ])

    def test_toutes_les_dates_de_soumission_sont_respectees(self):
        procs = processus([
            ("P1", 0, 3, 10, 30),
            ("P2", 5, 2, 10, 10),
        ])

        allocations = ordonnancer(procs, ressources(), energie())

        soumission = {"P1": 0, "P2": 5}
        for processus_id, instant, cpu, _ in allocations:
            self.assertIsNotNone(cpu)
            self.assertGreaterEqual(instant, soumission[processus_id])

    def test_energie_insuffisante(self):
        procs = processus([("P1", 0, 2, 10, 10)])

        allocations = ordonnancer(
            procs,
            ressources(energie_par_proc=50),
            energie(valeur=10),
        )

        self.assertEqual(allocations, [])

    def test_ram_insuffisante_ne_bloque_pas_les_autres_processus(self):
        procs = processus([
            ("P1", 0, 2, 50, 10),
            ("P2", 0, 2, 10, 20),
        ])

        allocations = ordonnancer(
            procs,
            ressources(ram_totale=20),
            energie(),
        )

        self.assertEqual(allocations, [
            ("P2", 0, "CPU1", 10),
            ("P2", 1, "CPU1", 10),
        ])

    def test_echeances_a_l_arrivee(self):
        procs = processus([
            ("P1", 0, 2, 10, 20),
            ("P2", 1, 2, 10, 5),
        ])

        allocations = ordonnancer(
            procs,
            ressources(nb_cpu=1),
            energie(),
        )

        self.assertEqual(allocations, [
            ("P1", 0, "CPU1", 10),
            ("P1", 1, "CPU1", 10),
            ("P2", 2, "CPU1", 10),
            ("P2", 3, "CPU1", 10),
        ])


if __name__ == "__main__":
    unittest.main()
