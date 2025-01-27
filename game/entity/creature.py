import random
from game.entity.entity import EntityAI
from interface.graphique import Image,charge_png_dans_dossier

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


class Forolo(Creature):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], stats: dict[str, int], info: dict[str, str | list[str]]) -> None:
        if not "age" in info:
            info["age"]="adulte"
        super().__init__(coordonnee, taille, stats, info)
        self.actualise_texture()
        

    def actualise_texture(self):
        if self.info == "adulte":
            self.texture = charge_png_dans_dossier("textures/entity/forolo/adulte")
        if self.info == "enfant":
            self.texture = charge_png_dans_dossier("textures/entity/forolo/enfant")
    


    @staticmethod
    def random_forolo_sauvage(coordonnee: tuple[int, int], taille: tuple[int, int]):
        """Crée un forolo aléatoire
        Args:
            coordonnee (tuple[int, int]): coordonnée du forolo
            taille (tuple[int, int]): taille du forolo
            age (str): age du forolo ("adulte" ou "enfant")
        """
        info = {
            "nom": "Forolo",
            "sexe": random.choice(("male", "femelle")),
        }
        #sexe
        rand = random.randint(1, 100)
        if rand <= 95:
            #"hetero"
            info["orientation_sexuel"] = ["male" if info["sexe"]=="femelle" else "femelle"]
        elif rand <= 98:
            #"bi"
            info["orientation_sexuel"]=["male","femelle"]
        else:
            #"gay"
            info["orientation_sexuel"]=[info["sexe"]]
        #age
        rand = random.randint(1, 100)
        if rand <= 90:
            info["age"] = "adulte"
        else:
            info["age"] = "enfant"

        #comportement
        rand = random.randint(1, 100)
        # ["passif","calme","calineur","peureux","timide","joueur","curieux","autiste"]
        if rand <=15:
            comportement = "passif"
        if rand <=31:
            comportement = "calme"
        if rand <=46:
            comportement = "calineur"
        if rand <=56:
            comportement = "peureux"
        if rand <=61:
            comportement = "timide"
        if rand <=86:
            comportement = "joueur"
        elif rand <=99:
            comportement = "curieux"
        else :
            comportement = "autiste"
        info["comportement"] = comportement
        stats={"vie_max": random.randint(90,110), "vitesse_min": 2, "vitesse_max":4,}
        Forolo(coordonnee, taille, stats, info)

    def compatibilite_amour(self,partenaire:"Forolo")->bool:
        return (self.info["sexe"] in partenaire.info["orientation_sexuel"] and
                partenaire.info["sexe"] in self.info["orientation_sexuel"])
    
    def compatibilite_reprod(self,partenaire:"Forolo")->bool:
        return (self.info["sexe"] != partenaire.info["sexe"] )
    
    def reproduction(self,partenaire:"Forolo"):
        if not self.compatibilite_reprod(partenaire): 
            raise ValueError("Les forolos ne sont pas compatibles pour la reproduction")
        
        info = {
            "nom": "Forolo",
            "sexe": random.choice(("male", "femelle")),
            "age": "enfant",
        }

        #orientation sexuel
        rand = random.randint(1, 100)
        if rand <= 95:
            #"hetero"
            info["orientation_sexuel"] = ["male" if info["sexe"]=="femelle" else "femelle"]
        elif rand <= 98:
            #"bi"
            info["orientation_sexuel"]=["male","femelle"]
        else:
            #"gay"
            info["orientation_sexuel"]=[info["sexe"]]
        
        #comportement
        rand = random.randint(1, 100)
        if rand <=15:
            comportement = "passif"
        if rand <=31:
            comportement = "calme"
        if rand <=46:
            comportement = "calineur"
        if rand <=56:
            comportement = "peureux"
        if rand <=61:
            comportement = "timide"
        if rand <=86:
            comportement = "joueur"
        elif rand <=99:
            comportement = "curieux"
        else :
            comportement = "autiste"
        info["comportement"] = comportement
        
        #stats
        stats={"vie_max": (random.randint(90,110)+self.stats["vie_max"]+partenaire.stats["vie_max"])//3+5, "vitesse_min": 2, "vitesse_max":4,}

        return Forolo(self.coordonnee, self.taille, stats, info)

 