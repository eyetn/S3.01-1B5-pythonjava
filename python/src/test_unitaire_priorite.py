import unittest
from priorite import *
from config_extrude import *



class TestPriorite(unittest.TestCase):

    def test_1_classique(self):
        config = config_ordonnanceur("python/inputs/Test1/config.txt")
        retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
        attendu = [['P1', 0, None ,512], ['P1', 7, 'CPU1', 512], ['P3', 17,'CPU1',1024]]
        comparaison = [retour[0],retour[3],retour[-1]]
        self.assertEqual(comparaison,attendu)

    def test_2_1proc(self):
        config = config_ordonnanceur("python/inputs/Test2/config.txt")
        retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
        attendu = [['P1', 0, None,512],['P1',7,'CPU1',512],['P1',8,'CPU1',512],['P1',9,'CPU1',512]]
        self.assertEqual(retour,attendu)

    def test_3_0energie(self):
        config = config_ordonnanceur("python/inputs/Test3/config.txt")
        retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
        attendu = []
        self.assertEqual(retour,attendu)

    def test_4_0ram(self):
        config = config_ordonnanceur("python/inputs/Test4/config.txt")
        retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
        attendu = []
        self.assertEqual(retour,attendu)

    def test_5_instant_eleve(self):
        config = config_ordonnanceur("python/inputs/Test5/config.txt")
        retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
        attendu = ['P4', 566, 'CPU1',1024]
        self.assertEqual(retour[-1],attendu)


if __name__ == "__main__":
    unittest.main()


