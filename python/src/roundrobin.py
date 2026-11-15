from config_extrude import *

content_csv("python/ressources/energie.csv") 


class Ordonnanceur:
    def __init__(self, processus, ressources, energie):
        self.processus = processus
        self.ressources = ressources
        self.energie = energie
        self.allocations = []

    def ordonnancer(self):
        raise NotImplementedError


class RoundRobin(Ordonnanceur):
    def __init__(self, processus, ressources, energie, quantum=2):
        super().__init__(processus, ressources, energie)
        self.quantum = quantum      # durée maximale d'une tranche de temps
        self.FileAtt = []           # file d'attente circulaire
        self.etat = {}              # cpu -> (processus, debut, fin) ou None
        for cpu in self.ressources["processeur"]:
            self.etat[cpu] = None
        self.ram = 0
        self.reste = {}             # id_processus -> temps d'exécution restant
        for p in self.processus:
            self.reste[p["id_processus"]] = int(p["duree_execution"])

    def ordonnancer(self):
        # énergie disponible à chaque instant
        dispo = {}
        for ligne in self.energie:
            instant = int(ligne["instant"])
            dispo[instant] = int(ligne["energie_disponible"])

        # date de soumission la plus grande
        derniere = 0
        for p in self.processus:
            if int(p["date_soumission"]) > derniere:
                derniere = int(p["date_soumission"])

        t = 0
        fini = False
        while not fini:

            # 1) fin de tranche : on libère les CPU
            preemptes = []
            for cpu in self.etat:
                if self.etat[cpu] is not None:
                    p, debut, fin = self.etat[cpu]
                    if fin == t:
                        self.allocations.append((p["id_processus"], debut, fin, cpu))
                        self.ram -= int(p["ram_necessaire"])
                        self.etat[cpu] = None
                        self.reste[p["id_processus"]] -= (fin - debut)
                        # pas terminé -> il retourne en fin de file
                        if self.reste[p["id_processus"]] > 0:
                            preemptes.append(p)

            # 2) nouvelles arrivées (avant les processus préemptés)
            for p in self.processus:
                if int(p["date_soumission"]) == t:
                    self.FileAtt.append(p)

            # 3) les processus préemptés repassent en fin de file
            for p in preemptes:
                self.FileAtt.append(p)

            # 4) nombre max de processeurs utilisables avec l'énergie dispo
            if t in dispo:
                maxi = dispo[t] // self.ressources["energieParProc"]
            else:
                maxi = 0

            # 5) affectation des CPU libres
            for cpu in self.etat:
                occupes = 0
                for c in self.etat:
                    if self.etat[c] is not None:
                        occupes += 1
                if self.etat[cpu] is None and occupes < maxi:
                    # premier processus de la file dont la RAM tient
                    for p in self.FileAtt:
                        if int(p["ram_necessaire"]) <= self.ressources["ramTotale"] - self.ram:
                            self.FileAtt.remove(p)
                            duree = min(self.quantum, self.reste[p["id_processus"]])
                            self.etat[cpu] = (p, t, t + duree)
                            self.ram += int(p["ram_necessaire"])
                            break

            # 6) test de fin
            cpu_occupe = False
            for cpu in self.etat:
                if self.etat[cpu] is not None:
                    cpu_occupe = True

            if t > derniere and len(self.FileAtt) == 0 and not cpu_occupe:
                fini = True
            if t > 1000:  # sécurité contre boucle infinie
                fini = True

            t += 1

        return self.allocations