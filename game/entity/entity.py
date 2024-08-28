import copy
import pygame
from interface.graphique import ObjetGraphique


class Entity(ObjetGraphique):
    def __init__(
        self,
        coordonnee: tuple[int, int],
        texture: pygame.Surface | str,
        taille: tuple[int, int],
        stats: dict[str, int],
    ) -> None:
        if "vie_max" not in stats:
            print("vie_max n'est pas dans stats\ndefinition de vie_max à 100")
            stats["vie_max"] = 100
        super().__init__(coordonnee, texture, taille)
        self.action = "rien"
        self.__stats_de_base = stats
        self.calcul_stats()
        self.vie = self.stats["vie_max"]
        self.effect = {}

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
