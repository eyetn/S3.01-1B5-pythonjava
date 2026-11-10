
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
