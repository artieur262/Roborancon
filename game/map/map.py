from interface.graphique import ObjetGraphique


class Composant(ObjetGraphique):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str|tuple[str,tuple[int,int]]]) -> None:
        super().__init__(coordonnee, texture, taille)
        self.lien_textures = texture
    
    def convet_to_dict(self) -> dict:
        return {"type":"composant","coordonnee": self.get_pos(), "taille": self.get_size(), "texture": self.lien_textures}

    @staticmethod
    def genere_self(dico: dict) -> "Composant":
        return Composant(dico["coordonnee"], dico["taille"], dico["texture"])

class Mur(Composant):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: str) -> None:
        super().__init__(coordonnee, taille,[texture])
    
    def convet_to_dict(self) -> dict:
        return {"type":"mur","coordonnee": self.get_pos(), "taille": self.get_size(), "texture": self.lien_textures}
        

class Porte(Composant):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str|tuple[str,tuple[int,int]]]) -> None:
        super().__init__(coordonnee, taille,texture)
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
    