import unittest
from fifo import ordonnancer

# données de test (format colonnes, comme content_csv)
PROCESSUS = {
    "id_processus": ["P1", "P2", "P3"],
    "date_soumission": ["0", "1", "2"],
    "duree_execution": ["5", "3", "6"],
    "ram_necessaire": ["512", "256", "1024"],
    "priorite": ["10", "5", "7"],
    "date_butoir": ["20", "15", "30"],
}
RESSOURCES = {"ramTotale": 1024, "energieParProc": 40, "processeur": ["CPU1", "CPU2"]}
VALEURS = [0, 0, 0, 0, 0, 0, 15, 45, 85, 120, 150, 175, 190, 190, 170, 140, 105, 65, 30, 10, 0, 0, 0, 0]
ENERGIE = {
    "instant": [str(k) for k in range(24)],
    "energie_disponible": [str(v) for v in VALEURS],
}


# garde seulement les lignes où le processus tourne (cpu différent de None)
def en_cours(retour):
    lignes = []
    for ligne in retour:
        if ligne[2] is not None:
            lignes.append(ligne)
    return lignes


class TestFifo(unittest.TestCase):

    def test_1_classique(self):
        retour = en_cours(ordonnancer(PROCESSUS, RESSOURCES, ENERGIE))
        self.assertEqual(len(retour), 14)    # P1 : 5 instants, P2 : 3, P3 : 6
        self.assertEqual(retour[0], ("P1", 7, "CPU1", 512))
        self.assertEqual(retour[-1], ("P3", 17, "CPU1", 1024))

    def test_2_un_seul_cpu(self):
        procs = {
            "id_processus": ["P1"],
            "date_soumission": ["0"],
            "duree_execution": ["3"],
            "ram_necessaire": ["512"],
        }
        ressources = {"ramTotale": 1024, "energieParProc": 40, "processeur": ["CPU1"]}
        retour = en_cours(ordonnancer(procs, ressources, ENERGIE))
        attendu = [("P1", 7, "CPU1", 512), ("P1", 8, "CPU1", 512), ("P1", 9, "CPU1", 512)]
        self.assertEqual(retour, attendu)

    def test_3_zero_energie(self):
        energie = {"instant": [str(k) for k in range(24)], "energie_disponible": ["0"] * 24}
        retour = en_cours(ordonnancer(PROCESSUS, RESSOURCES, energie))
        self.assertEqual(retour, [])

    def test_4_ram_trop_grande(self):
        ressources = {"ramTotale": 100, "energieParProc": 40, "processeur": ["CPU1", "CPU2"]}
        retour = en_cours(ordonnancer(PROCESSUS, ressources, ENERGIE))
        self.assertEqual(retour, [])

    def test_5_ram_jamais_depassee(self):
        retour = en_cours(ordonnancer(PROCESSUS, RESSOURCES, ENERGIE))
        for instant in range(30):
            total = 0
            for ligne in retour:
                if ligne[1] == instant:
                    total = total + ligne[3]
            self.assertLessEqual(total, RESSOURCES["ramTotale"])

    def test_6_energie_jamais_depassee(self):
        retour = en_cours(ordonnancer(PROCESSUS, RESSOURCES, ENERGIE))
        for instant in range(24):
            nb = 0
            for ligne in retour:
                if ligne[1] == instant:
                    nb = nb + 1
            self.assertLessEqual(nb, VALEURS[instant] // 40)

    def test_7_ordre_fifo(self):
        # sans contrainte d'énergie ni de RAM, P1 démarre avant P2, P2 avant P3
        procs = {
            "id_processus": ["P1", "P2", "P3"],
            "date_soumission": ["0", "1", "2"],
            "duree_execution": ["5", "5", "5"],
            "ram_necessaire": ["10", "10", "10"],
        }
        ressources = {"ramTotale": 1000, "energieParProc": 10, "processeur": ["CPU1"]}
        energie = {"instant": [str(k) for k in range(50)], "energie_disponible": ["100"] * 50}
        retour = en_cours(ordonnancer(procs, ressources, energie))
        debuts = {}
        for ligne in retour:
            if ligne[0] not in debuts:
                debuts[ligne[0]] = ligne[1]
        self.assertEqual(debuts, {"P1": 0, "P2": 5, "P3": 10})


if __name__ == "__main__":
    unittest.main()