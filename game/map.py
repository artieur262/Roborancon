from interface.graphique import ObjetGraphique

class Mur(ObjetGraphique):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str]) -> None:
        super().__init__(coordonnee, [texture], taille)
        

class Porte(ObjetGraphique):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str|tuple[str,tuple[int,int]]]) -> None:
        super().__init__(coordonnee, texture, taille)
        self.etat = "ferme"

    def ouvrir(self):
        self.etat = "ouvert"
        self.animation = 1
    
    def ferme(self):
        self.etat = "ferme"
        self.animation = 0
    
    def ouvrir_fermer(self):
        if self.etat == "ferme":
            self.ouvrir()
        else:
            self.ferme()
    