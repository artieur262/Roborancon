import os
import copy
import pygame
from interface.graphique import (
    ObjetGraphique,
    genere_texture,
    # charge_png_dans_dossier,
)


class Entity(ObjetGraphique):
    """Classe de base pour les entités

    args:
        coordonnee (tuple[int, int]): coordonnée de l'entité
        texture (str): chemin vers le dossier contenant les images
        taille (tuple[int, int]): taille de l'entité
        stats (dict[str, int]): stats de l'entité

    """

    def __init__(
        self,
        coordonnee: tuple[int, int],
        taille: tuple[int, int],
        stats: dict[str, int],
    ) -> None:
        if "vie_max" not in stats:
            print("vie_max n'est pas dans stats\ndefinition de vie_max à 100")
            stats["vie_max"] = 100
        super().__init__(coordonnee, [genere_texture((1, 1), (0, 0, 0))], taille)
        self.action = "rien"
        self.__stats_de_base = stats
        self.calcul_stats()
        self.vie = self.stats["vie_max"]
        self.effect = {}
        self.sens = "bas"
        

    def calcul_stats(self):
        """Calcul les stats du joueur"""
        self.stats = copy.deepcopy(self.__stats_de_base)

    def actualise_animation(self):
        """Actualise l'animation"""
        if self.action == "rien":
            self.set_animation(0)

    def actualise_effect(self):
        """Actualise les effets"""
        clee_suppr = []
        for clee, value in self.effect.items():
            value["duree"] -= 1
            if value["duree"] <= 0:
                clee_suppr.append(clee)

        for clee in clee_suppr:
            self.effect.pop(clee)

    def applique_effect(self):
        """Applique les effets"""
        for clee, value in self.effect.items():
            match clee:
                case "regeneration":
                    self.ajoute_vie(value["puissance"])

    def ajoute_vie(self, valu):
        """ajoute de la vie et adjuste la vie"""
        self.vie += valu
        self.corrige_vie()

    def corrige_vie(self):
        """évite de dépacer la valeur max"""
        if self.vie < 0:
            self.vie = 0
        if self.vie > self.stats["vie_max"]:
            self.vie = self.stats["vie_max"]

    def convert_to_dict(self):
        """converti en dict"""
        return {
            "type": "entity",
            "coordonnee": self.get_pos(),
            "taille": self.get_size(),
            "stats": self.stats,
            "vie": self.vie,
            "effect": self.effect,
        }
    
class EntityAI(Entity):
    """Classe de base pour les entités

    args:
        coordonnee (tuple[int, int]): coordonnée de l'entité
        texture (str): chemin vers le dossier contenant les images
        taille (tuple[int, int]): taille de l'entité
        stats (dict[str, int]): stats de l'entité

    """

    def __init__(
        self,
        coordonnee: tuple[int, int],
        taille: tuple[int, int],
        stats: dict[str, int],
    ) -> None:
        super().__init__(coordonnee, taille, stats)
        self.pensee = "rien"

    def pense(self):
        """Pense"""
        pass

    