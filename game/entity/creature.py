from game.entity.entity import EntityAI

class Creature(EntityAI):
    def __init__(
        self,
        coordonnee: tuple[int, int],
        taille: tuple[int, int],
        stats: dict[str, int],
        info: dict[str, str|list[str]],
    ) -> None:
        super().__init__(coordonnee, taille, stats)
        if "nom" not in info:
            raise ValueError("Il manque le nom dans les info")
        if "compotement" not in info:
            raise ValueError("Il manque le comportement dans les info")
        if "sexe" not in info:
            raise ValueError("Il manque le sexe dans les info")
        if "orientation_sexuel" not in info:
            raise ValueError("Il manque l'orientation sexuel dans les info")
        
        self.info = info
        
    
    # def pense(self):




# info = {
#     "nom": "Bob",
#     "compotement": "autiste",
#     "sexe": "male",
#     "orientation_sexuel":["femelle"] 
# }