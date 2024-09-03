import pygame

from game.entity.entity import Entity
from game.inventaire.item import Item, Membre, Corps
from game.inventaire.inventaire import Inventaire
from interface.graphique import Image, genere_texture


class Playeur(Entity):
    def __init__(
        self,
        coordonnee: tuple[int, int],
        taille: tuple[int, int],
        stats: dict[str, int],
    ) -> None:
        self.membre_equipe: dict[str, Membre | None] = {"corps": None}
        super().__init__(coordonnee, taille, stats)
        self.inventaire = Inventaire(10)

    def actualise_animation(self):
        if self.action == "rien":
            if self.animation in (6, 3):
                self.set_animation(0)
            elif 1 <= self.animation < 6:
                self.set_animation(self.animation + 1)
        elif self.action == "marche":
            if self.animation < 1 or self.animation > 5:
                self.set_animation(1)
            else:
                self.set_animation(self.animation + 1)

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
            self.texture.append(image)
