import random
from game.entity.entity import EntityAI
from interface.graphique import Image,charge_png_dans_dossier,LienSpritesheet

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
        if "comportement" not in info:
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
        if self.info["age"] == "adulte":
            self.texture = LienSpritesheet("textures/entity/passif/forolo",None).decoupe()
        elif self.info["age"] == "enfant":
            self.texture = LienSpritesheet("textures/entity/passif/forolo",None).decoupe()
        else:
            raise ValueError("age inconnu")
    


    @staticmethod
    def random_sauvage(coordonnee: tuple[int, int], taille: tuple[int, int])->"Forolo":
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
        list_comp=["passif", "calme", "calineur", "peureux", "timide", "joueur", "curieux", "autiste"]
        proba_comp=[15, 16, 15, 10, 5, 25, 13, 1]
        somme = 0
        for i in range(1, len(proba_comp)):
            somme += proba_comp[i]
            if rand <= somme:
                comportement = list_comp[i]
        info["comportement"] = comportement
        stats={"vie_max": random.randint(90,110), "vitesse_min": 2, "vitesse_max":4,}
        return Forolo(coordonnee, taille, stats, info)

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

class Lezardus(Creature):
    def __init__(self, coordonnee: tuple[int, int], taille: tuple[int, int], stats: dict[str, int], info: dict[str, str | list[str]]) -> None:
        if not "age" in info:
            info["age"]="adulte"
        super().__init__(coordonnee, taille, stats, info)
        self.actualise_texture()
    
    def actualise_texture(self):
        if self.info["age"] == "adulte":
            self.texture = LienSpritesheet("textures/entity/passif/lezardus.png",(32,32)).decoupe()
        elif self.info["age"] == "enfant":
            self.texture = LienSpritesheet("textures/entity/passif/lezardus.png",(32,32)).decoupe()
        else:
            raise ValueError("age inconnu")

    
    def actualise_animation(self):
        """Actualise l'animation"""
        match self.action:
            case "rien":
                match self.sens:
                    case "bas":
                        if self.get_animation() not in (1, 2, 0):
                            self.set_animation(0)
                        else:
                            self.set_animation(self.get_animation()+1)
                    case "gauche":
                        if self.get_animation() not in (5, 6, 4):
                            self.set_animation(4)
                        else:
                            self.set_animation(self.get_animation()+1)
                    case "haut":
                        if self.get_animation() not in (9, 10, 8):
                            self.set_animation(8)
                        else:
                            self.set_animation(self.get_animation()+1)
                    case "droite":
                        if self.get_animation() not in (13, 14, 12):
                            self.set_animation(12)
                        else:
                            self.set_animation(self.get_animation()+1)
            

    @staticmethod
    def random_sauvage(coordonnee: tuple[int, int], taille: tuple[int, int])->"Lezardus":
        """Crée un Lezardus aléatoire
        Args:
            coordonnee (tuple[int, int]): coordonnée du Lezardus
            taille (tuple[int, int]): taille du Lezardus
            age (str): age du Lezardus ("adulte" ou "enfant")
        """
        info = {
            "nom": "Lezardus",
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
        list_comp=["curieux", "calme"  , "somnolent"  , "glouton",
                   "timide",  "peureux", "territorial", "autiste"]
        proba_comp=[20,20,17,15,
                    10,10, 7,1]
        rand = 100
        somme = 0
        for i in range(0, len(proba_comp)):
            somme += proba_comp[i]
            if rand <= somme:
                comportement = list_comp[i]
                break
        info["comportement"] = comportement
        stats={"vie_max": random.randint(90,110), "vitesse_min": 2, "vitesse_max":4,}
        return Lezardus(coordonnee, taille, stats, info)

    def compatibilite_amour(self,partenaire:"Forolo")->bool:
        return (self.info["sexe"] in partenaire.info["orientation_sexuel"] and
                partenaire.info["sexe"] in self.info["orientation_sexuel"])
    
    def compatibilite_reprod(self,partenaire:"Forolo")->bool:
        return (self.info["sexe"] != partenaire.info["sexe"] )
    