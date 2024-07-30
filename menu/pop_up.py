"""ce module contien les class pour les pop up"""

import time

import pygame

from interface.actualisation_pygame import actualise_event
from interface.graphique import Image, screen
from interface.class_clavier import Clavier, Souris

# pylint: disable=no-member


class PopUp:
    def __init__(
        self,
        coordonnee: tuple[int, int],
        texture: Image | pygame.Surface | str,
        temp_vie: float,
    ):
        if not isinstance(texture, Image):
            texture = Image(texture)
        self.__texture = texture
        self.coordonnee = coordonnee
        self.__taille = texture.get_size()
        self.__temp_vie = temp_vie
        self.naisance = time.time()
        self.en_vie = True

    def centrer(self):
        """centre le pop up"""
        self.coordonnee = (
            screen.get_width() // 2 - self.__taille[0] // 2,
            screen.get_height() // 2 - self.__taille[1] // 2,
        )

    def afficher(self):
        """affiche le pop up"""
        screen.blit(self.__texture.texture, self.coordonnee)

    def play(self):
        """affiche le pop up et le fait disparaitre après un certain temps"""
        self.afficher()
        if time.time() - self.naisance > self.__temp_vie:
            self.en_vie = False
        return self.en_vie

    @staticmethod
    def main(
        clavier: Clavier,
        souris: Souris,
        coordonnee: tuple[int, int],
        texture: Image | pygame.Surface | str,
        temp_vie: float,
    ):
        """cree un pop up et le fait apparaitre jusqu'a ce qu'il disparaisse"""
        popup = PopUp(coordonnee, texture, temp_vie)

        clock = pygame.time.Clock()
        while popup.en_vie:
            popup.play()
            event = actualise_event(clavier, souris)
            if (
                "quitter" in event
                or clavier.get_pression(pygame.K_ESCAPE) == "vien_presser"
                or "redimentione" in event
                or clavier.get_pression(pygame.K_F11) == "vien_presser"
                or souris.get_pression(1) == "vien_presser"
            ):
                popup.en_vie = False

            pygame.display.update()
            clock.tick(60)
