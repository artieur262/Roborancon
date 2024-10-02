import pygame

from autre import id_gestion
from game.entity.entity import Entity
from game.inventaire.item import Item, Membre, Corps,genere_item
from game.inventaire.inventaire import Inventaire
from interface.graphique import Zone, Image, genere_texture,charge_png_dans_dossier


class Playeur(Entity):
    def __init__(
        self,
        coordonnee: tuple[int, int],
        taille: tuple[int, int],
        stats: dict[str, int],
    ) -> None:
        if "vitesse_min" not in stats:
            print("vitesse_min n'est pas dans les stats")
            stats["vitesse_min"] = 7
        if "vitesse_max" not in stats:
            print("vitesse_max n'est pas dans les stats")
            stats["vitesse_max"] = 5
        self.membre_equipe: dict[str, Membre | None] = {"corps": None}
        super().__init__(coordonnee, taille, stats)
        self.inventaire = Inventaire(10)

    def actualise_animation(self,tick:int):
        if self.action == "rien" and tick%5== 0:
            if self.animation in (6, 3):
                self.set_animation(0)
            elif 1 <= self.animation < 6:
                self.set_animation(self.animation + 1)
        elif ((self.action == "marche" and tick % 7 == 0) or
               (self.action == "courir" and tick % 4 == 0)):
            if self.sens == "bas":
                if self.animation < 1 or self.animation >= 6:
                    self.set_animation(1)
                else:
                    self.set_animation(self.animation + 1)
            elif self.sens == "haut":
                if self.animation <=1  or self.animation > 6:
                    self.set_animation(6)
                else:
                    self.set_animation(self.animation -1)
       
    def equipe_membre(self, indice_iventaire, emplacement: str):
        """Équipe un item"""
        item = self.inventaire.get_item(indice_iventaire)
        if emplacement not in self.membre_equipe:
            return False
        if self.membre_equipe[emplacement] is not None:
            self.inventaire.supprime(indice_iventaire)
            self.inventaire.ajoute_item(item)
        else:
            self.membre_equipe[emplacement] = item
        return True

    def calcul_stats(self):
        """Actualise les stats du joueur"""
        super().calcul_stats()
        for membre in self.membre_equipe.values():
            if membre is not None:
                if membre.etat == "normal":
                    for clee, value in membre.stats.items():
                        if clee in self.stats:
                            if isinstance(value, (int, float)):
                                self.stats[clee] += value
                            else:
                                print(f"la valeur de {clee} n'est pas un nombre")
                        else:
                            print(f"la clée {clee} n'est pas dans les stats")

    def actualise_texture(self):
        """Actualise la texture du playeur"""
        nombre_texture = 7
        corps = self.membre_equipe["corps"]
        taille = (64, 64)
        if not isinstance(corps, Corps):
            for i in range(nombre_texture):
                self.texture.append(Image(genere_texture(taille, (0, 0, 0, 0))))
            return
        self.texture = []
        for i in range(nombre_texture):
            image = Image(genere_texture(taille, (0, 0, 0, 0)))

            for clee in corps.ordre_affichage:
                membre = self.membre_equipe[clee]
                position = corps.membre_emplacement[clee]
                image.ajoute_image(membre.get_texture(i), position)
            image.ancre=(21,37)
            self.texture.append(image)
        
    def arrete(self):
        """Arrête le playeur"""
        self.action = "rien"
    
    def marche(self, direction: str, list_obstacle:list[Zone], tick:int):
        """Fait marcher le playeur"""
        taille_pas = self.stats["vitesse_min"]

        if tick % 7 == 0:   
            if direction == "bas":
                self.sens = "bas"
                self.action = "marche"
                self.deplacement(direction,taille_pas,list_obstacle)

            elif direction == "haut":
                self.sens = "haut"
                self.action = "marche"
                self.deplacement(direction,taille_pas,list_obstacle)  
            elif direction == "gauche":
                self.sens = "gauche"
                self.action = "marche"
                self.deplacement(direction,taille_pas,list_obstacle)
            elif direction == "droite":
                self.sens = "droite"
                self.action = "marche"
                self.deplacement(direction,taille_pas,list_obstacle)      
    def courir(self, direction: str,list_obstacle:list[Zone],tick:int):
        """Fait courir le playeur"""
        taille_pas = self.stats["vitesse_max"]
        if tick % 4 == 0:
            if direction == "bas":
                self.sens = "bas"
                self.action = "courir"
                self.deplacement(direction,taille_pas,list_obstacle)   

            elif direction == "haut":
                self.sens = "haut"
                self.action = "courir"
                self.deplacement(direction,taille_pas,list_obstacle)
            elif direction == "gauche":
                self.sens = "gauche"
                self.action = "courir"
                self.deplacement(direction,taille_pas,list_obstacle)
            elif direction == "droite":
                self.sens = "droite"
                self.action = "courir"
                self.deplacement(direction,taille_pas,list_obstacle)
            else:
                print("direction non reconnue : ", direction)   
    
    def deplacement(self, direction: str,distance:int,obstacle:list[Zone]):
        """Déplace le playeur"""
        match direction:
            case "bas":
                deplacement=(0, distance)
            case "haut":
                deplacement=(0, -distance)
            case "gauche":
                deplacement=(-distance, 0)
            case "droite":
                deplacement=(distance, 0)
        
        self.add_pos(deplacement)
        colision = False
        for zone in obstacle:
            if self.collision(zone.get_pos(), zone.get_size()):
                match direction:
                    case "bas":
                        self.set_pos((self.get_pos()[0], zone.get_pos()[1] - self.get_size()[1]))
                    case "haut":
                        self.set_pos((self.get_pos()[0], zone.get_pos()[1] + zone.get_size()[1]))
                    case "gauche":
                        self.set_pos((zone.get_pos()[0] + zone.get_size()[0], self.get_pos()[1]))
                    case "droite":
                        self.set_pos((zone.get_pos()[0] - self.get_size()[0], self.get_pos()[1]))
        
        return not colision

                

    def convert_to_dict(self):
        sorti = super().convert_to_dict()
        sorti["type"] = "playeur"
        sorti["inventaire"] = self.inventaire.convert_to_dict()
        sorti["membre_equipe"] = {
            clee: value.convert_to_dict() if value is not None else None
            for clee, value in self.membre_equipe.items()
        }
        return sorti

    @staticmethod
    def genere_self(data: dict):
        playeur = Playeur(
            data["coordonnee"],
            data["taille"],
            data["stats"],
        )
        playeur.inventaire = Inventaire.genere_self(data["inventaire"])
        playeur.membre_equipe = {
            clee: genere_item(value) if value is not None else None
            for clee, value in data["membre_equipe"].items()
        }
        playeur.calcul_stats()
        playeur.actualise_texture()
        id_gestion.supprime_id(playeur.id)
        playeur.id=data["id"]
        id_gestion.ajoute_id(playeur.id)
        return playeur


class PlayeurTest(Playeur):
    def actualise_texture(self):
        self.texture = charge_png_dans_dossier("textures/teste/test_playeur")
    
    def actualise_animation(self,tick:int):
        if self.action == "rien" and tick%5== 0:
            match self.sens:
                case "bas": 
                    self.set_animation(0)
        
                case "haut":
                    self.set_animation(3)
                case "droite":
                    self.set_animation(6)
                case "gauche":
                    self.set_animation(9)

        elif (self.action == "marche" and tick % 7 == 0):
            match self.sens:
                case "bas":
                    self.set_animation(1)
                case "haut":
                    self.set_animation(4)
                case "droite":
                    self.set_animation(7)
                case "gauche":
                    self.set_animation(10)

        elif (self.action == "courir" and tick % 4 == 0):
            match self.sens:
                case "bas":   
                    self.set_animation(2)
                case "haut":
                    self.set_animation(5)
                case "droite":
                    self.set_animation(8)
                case "gauche":
                    self.set_animation(11)    


    @staticmethod
    def genere_self(data: dict):
        playeur = PlayeurTest(
            data["coordonnee"],
            data["taille"],
            data["stats"],
        )
        playeur.inventaire = Inventaire.genere_self(data["inventaire"])
        playeur.membre_equipe = {
            clee: genere_item(value) if value is not None else None
            for clee, value in data["membre_equipe"].items()
        }
        playeur.calcul_stats()
        playeur.actualise_texture()
        id_gestion.supprime_id(playeur.id)
        playeur.id=data["id"]
        id_gestion.ajoute_id(playeur.id)
        return playeur