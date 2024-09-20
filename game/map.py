from interface.graphique import ObjetGraphique

class Mur(ObjetGraphique):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str]) -> None:
        super().__init__(coordonnee, [texture], taille)
        self.lien_texture = texture
        

class Porte(ObjetGraphique):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str|tuple[str,tuple[int,int]]]) -> None:
        super().__init__(coordonnee, texture, taille)
        self.lien_texture = texture
        self.etat = "ferme"

    def ouvre(self):
        self.etat = "ouvert"
        self.animation = 1
    
    def ferme(self):
        self.etat = "ferme"
        self.animation = 0
    
    