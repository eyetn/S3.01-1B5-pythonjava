import unittest
from priorite import *
from config_extrude import *



# class TestPriorite(unittest.TestCase):

#     def test_1_classique(self):
#         config = config_ordonnanceur("python/inputs/Test1/config.txt")
#         retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
#         attendu = [['P1', 0, 11, 'CPU1'], ['P2', 1, 10, 'CPU2'], ['P3', 2, 17, 'CPU1']]
#         self.assertEqual(retour,attendu)

#     def test_2_1proc(self):
#         config = config_ordonnanceur("python/inputs/Test2/config.txt")
#         retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
#         attendu = [['P1', 0, 9, 'CPU1']]
#         self.assertEqual(retour,attendu)

#     def test_3_0energie(self):
#         config = config_ordonnanceur("python/inputs/Test3/config.txt")
#         retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
#         attendu = []
#         self.assertEqual(retour,attendu)

#     def test_4_0ram(self):
#         config = config_ordonnanceur("python/inputs/Test4/config.txt")
#         retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
#         attendu = []
#         self.assertEqual(retour,attendu)

#     def test_5_instant_eleve(self):
#         config = config_ordonnanceur("python/inputs/Test5/config.txt")
#         retour = ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"])
#         attendu = [['P1', 0, 11, 'CPU1'],['P2', 1, 10, 'CPU2'],['P3', 2, 17, 'CPU1'],['P4', 2, 566, 'CPU1']]
#         self.assertEqual(retour,attendu)


# if __name__ == "__main__":
#     unittest.main()


config = config_ordonnanceur("python/inputs/Test1/config.txt")
print(ordonnanceur_priorite(config["energie"],config["fichier_processus"],config["fichier_ressources"]))
