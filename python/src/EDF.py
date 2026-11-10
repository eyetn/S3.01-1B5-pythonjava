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

class EDF(Ordonnanceur): 
    def __init__(self, processus, ressources, energie): 
        super().__init__(processus, ressources, energie) 
        self.FileAtt = [] 
        self.etat = {} 
        for cpu in self.ressources["processeur"]: 
            self.etat[cpu] = None 
        self.ram = 0 
        
    def ordonnancer(self): 
        # Énergie disponible à chaque instant
        dispo = {
            int(ligne["instant"]): int(ligne["energie_disponible"])
            for ligne in self.energie
        }
            
        # Date de soumission la plus grande
        derniere = 0 
        for p in self.processus: 
            derniere = max(derniere, int(p["date_soumission"])) 
            
        t = 0 
        fini = False 
        
        while fini == False: 
            # Libère les CPU quand le processus est fini
            for cpu in self.etat: 
                if self.etat[cpu] is not None: 
                    p = self.etat[cpu][0] 
                    debut = self.etat[cpu][1] 
                    fin = self.etat[cpu][2] 
                    if fin == t: 
                        self.allocations.append((p["id_processus"], debut, fin, cpu)) 
                        self.ram -= int(p["ram_necessaire"]) 
                        self.etat[cpu] = None 
                        
            # Ajoute les arrivées dans la file
            for p in self.processus: 
                if int(p["date_soumission"]) == t: 
                    self.FileAtt.append(p) 
                    
            # Tri la file d'attente par deadline croissante pour EDF
            self.FileAtt.sort(key=lambda x: int(x["deadline"])) 
            
            # Récupère l'énergie disponible à l'instant t (0 par défaut si non spécifié)
            energie_dispo_t = dispo.get(t, 0)
            
            for cpu in self.etat: 
                if self.etat[cpu] is None and self.FileAtt: 
                    processus_alloue = None 
                    
                    for p in self.FileAtt: 
                        ram_ok = self.ram + int(p["ram_necessaire"]) <= self.ressources["ram"]
                        energie_ok = int(p.get("energie_necessaire", 0)) <= energie_dispo_t
                        
                        if ram_ok and energie_ok: 
                            processus_alloue = p 
                            break 
                            
                    if processus_alloue: 
                        debut = t 
                        fin = t + int(processus_alloue["duree"]) 
                        self.etat[cpu] = (processus_alloue, debut, fin) 
                        self.ram += int(processus_alloue["ram_necessaire"]) 
                        # On consomme l energie pour cet instant t
                        energie_dispo_t -= int(processus_alloue.get("energie_necessaire", 0))
                        self.FileAtt.remove(processus_alloue) 
                        
            t += 1 
            cpus_libres = all(self.etat[cpu] is None for cpu in self.etat) 
            if t > derniere and not self.FileAtt and cpus_libres: 
                fini = True 
            elif t > 1000: 
                print("Probleme") 
                fini = True 
                
        return self.allocations
