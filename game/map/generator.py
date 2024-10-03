from interface.graphique import Zone,ObjetGraphique,Image

class Module(Zone):
    def __init__(self, coordonnee: list, taille: list, composants: list[str],fond=str) -> None:
        super().__init__(coordonnee, taille)
        self.composants = composants
        self.fond = fond
    
    def get_composants(self) -> list[ObjetGraphique]:
        return self.composants
    
    def ajouter_composant(self, composant: ObjetGraphique) -> None:
        self.composants.append(composant)
    
    def get_fond(self) -> Image:
        return self.fond

 
    
