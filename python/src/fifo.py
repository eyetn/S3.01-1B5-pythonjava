
class Ordonnanceur:
    def __init__(self, processus, ressources, energie):
        self.processus = processus
        self.ressources = ressources
        self.energie = energie
        self.allocations = []
    def ordonnancer(self):
        raise NotImplementedError

class FIFO(Ordonnanceur):
    def __init__(self, processus, ressources, energie):
        super().__init__(processus, ressources, energie)
        self.FileAtt = []
        self.etat = {}
        for cpu in self.ressources["processeur"]:
            self.etat[cpu] = None
        self.ram = 0

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
        while fini == False:

            # libere les CPU quand le processus est fini
            for cpu in self.etat:
                if self.etat[cpu] is not None:
                    p = self.etat[cpu][0]
                    debut = self.etat[cpu][1]
                    fin = self.etat[cpu][2]
                    if fin == t:
                        self.allocations.append((p["id_processus"], debut, fin, cpu))
                        self.ram = self.ram - int(p["ram_necessaire"])
                        self.etat[cpu] = None
            # ajoute les arrivées dans la file
            for p in self.processus:
                if int(p["date_soumission"]) == t:
                    self.FileAtt.append(p)
            # verifie si t existe
            if t in dispo:
                maxi = dispo[t] // self.ressources["energieParProc"]
            else:
                maxi = 0
            # compte des qu'un CPU est occupé
            for cpu in self.etat:
                occupes = 0
                for c in self.etat:
                    if self.etat[c] is not None:
                        occupes = occupes + 1
                # vérifie qu'on peut commencer
                if self.etat[cpu] is None and occupes < maxi:
                    #cherche le proccessus qui est le premier et dont la RAM est inférieur ou égale à la RAM disponible
                    for p in self.FileAtt:
                        if int(p["ram_necessaire"]) <= self.ressources["ramTotale"] - self.ram:
                            self.FileAtt.remove(p)
                            self.etat[cpu] = (p, t, t + int(p["duree_execution"]))
                            self.ram = self.ram + int(p["ram_necessaire"])
                            break

            # teste si on a fini
            cpu_occupe = False
            for cpu in self.etat:
                if self.etat[cpu] is not None:
                    cpu_occupe = True

            if t > derniere and len(self.FileAtt) == 0 and cpu_occupe == False:
                fini = True
            if t > 1000:  # sécurité contre boucle infinie
                fini = True

            t = t + 1

        return self.allocations

if __name__ == "__main__":
    processus = [
        {"id_processus": "P1", "date_soumission": "0", "duree_execution": "5", "ram_necessaire": "512", "priorite": "10", "date_butoir": "20"},
        {"id_processus": "P2", "date_soumission": "1", "duree_execution": "3", "ram_necessaire": "256", "priorite": "5", "date_butoir": "15"},
        {"id_processus": "P3", "date_soumission": "2", "duree_execution": "6", "ram_necessaire": "1024", "priorite": "7", "date_butoir": "30"},
    ]
    ressources = {"nbProcesseurs": 2, "ramTotale": 1024, "energieParProc": 40, "processeur": ["CPU1", "CPU2"]}
    vals = [0,0,0,0,0,0,15,45,85,120,150,175,190,190,170,140,105,65,30,10,0,0,0,0]
    energie = [{"instant": str(i), "energie_disponible": str(v)} for i, v in enumerate(vals)]

    f = FIFO(processus, ressources, energie)
    for alloc in f.ordonnancer():
        print(alloc)