from interface.graphique import ObjetGraphique,Image


class Composant(ObjetGraphique):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str|tuple[str,tuple[int,int]]]) -> None:
        super().__init__(coordonnee, texture, taille)
        self.lien_textures = []
        for tex in texture:
            if isinstance(tex, str):
                self.lien_textures.append(tex)
            elif isinstance(tex, tuple):
                self.lien_textures.append(tex)
            else:
                self.lien_textures.append(None)

    
    def convet_to_dict(self) -> dict:
        return {"type":"composant","coordonnee": self.get_pos(), "taille": self.get_size(), "texture": self.lien_textures}

    @staticmethod
    def genere_self(dico: dict) -> "Composant":
        return Composant(dico["coordonnee"], dico["taille"], dico["texture"])

class Mur(Composant):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: str|Image) -> None:
        super().__init__(coordonnee, taille,[texture])
        if isinstance(texture,Image):
            self.lien_textures=None
    
    def convet_to_dict(self) -> dict:
        sorti=super().convet_to_dict()
        sorti["type"]="mur"
        return sorti

    @staticmethod
    def genere_self(dico: dict) -> "Mur":
        return Mur(dico["coordonnee"], dico["taille"], dico["texture"][0])      
    
    def sont_fusionable(self, mur: "Mur") -> bool:
        self_pos = self.get_pos()
        self_size = self.get_size()
        mur_pos = mur.get_pos()
        mur_size = mur.get_size()
        if ((self_pos[0]==mur_pos[0]+mur_size[0] or self_pos[0]+self_size[0]==mur_pos[0])
            and self_pos[1]==mur_pos[1] and self_size[1]==mur_size[1]):
            return True
        if ((self_pos[1]==mur_pos[1]+mur_size[1] or self_pos[1]+self_size[1]==mur_pos[1])
            and self_pos[0]==mur_pos[0] and self_size[0]==mur_size[0]):
            return True
        return False
    
    def fusionne(self, mur: "Mur") -> "Mur":
        if not self.sont_fusionable(mur):
            raise ""
        self_pos = self.get_pos()
        self_size = self.get_size()
        mur_pos = mur.get_pos()
        mur_size = mur.get_size()
        if self_pos[0]==mur_pos[0]+mur_size[0]:

            mur.image_actuel().afficher()
            Mur(mur_pos,(self_size[0]+mur_size[0],self_size[1]))

    
    def copy(self):
        """retourne une copie du mur
        fait une copie pronfonde de l'objet sauf pour l'image
        """
        return Mur([self.get_pos()[0], self.get_pos()[1]],
                    (self.get_size()[0],self.get_size()[1]),
                    self.image_actuel())

class Porte(Composant):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: list[str|tuple[str,tuple[int,int]]]) -> None:
        super().__init__(coordonnee, taille,texture)
        self.etat = "fermer"

    def get_ouverture(self):
        return self.etat
    def set_ouverture(self,etat:str):
        self.etat=etat
    def ouvrir(self):
        self.etat = "ouvert"
        self.animation = 1
    
    def fermer(self):
        self.etat = "fermer"
        self.animation = 0
    
    def ouvrir_fermer(self):
        if self.etat == "fermer":
            self.ouvrir()
        else:
            self.fermer()

    def convet_to_dict(self) -> dict:
        sorti=super().convet_to_dict()
        sorti["type"]="porte"
        sorti["etat"]=self.etat
        return sorti

    @staticmethod
    def genere_self(dico: dict) -> "Porte":
        porte= Porte(dico["coordonnee"], dico["taille"], dico["texture"])
        porte.set_ouverture(dico["etat"])
        return porte
    
class Sol(Composant):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], texture: str) -> None:
        super().__init__(coordonnee, taille,[texture])
    
    def convet_to_dict(self) -> dict:
        sorti=super().convet_to_dict()
        sorti["type"]="sol"
        return sorti

    @staticmethod
    def genere_self(dico: dict) -> "Sol":
        return Sol(dico["coordonnee"], dico["taille"], dico["texture"][0])

