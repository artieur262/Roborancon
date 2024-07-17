"""Module qui gère le menu de démarrage"""

import pygame

# import copy

from interface.actualisation_pygame import actualise_event, change_fullscreen
from interface.graphique import (
    # ObjetGraphique,
    Image,
    screen,
    place_texte_in_texture,
    vider_affichage,
)
from interface.bouton import Bouton

# pylint: disable=no-member


class StartMenu:
    r"""Classe qui gère le menu de démarrage

    agrs :
        - fond : Image | pygame.Surface | str : texture de fond
        - tecture_bouton : list[Image | pygame.Surface | str] : texture des boutons
                           /!\ il faut au moins 2 texture
        - taille_bouton : tuple[int, int] : taille des boutons
        - langue : str : langue du menu
    """

    def __init__(
        self,
        fond: Image | pygame.Surface | str,
        tecture_bouton: list[Image | pygame.Surface | str],
        taille_bouton: tuple[int, int],
        langue: str,
    ) -> None:
        if not isinstance(fond, Image):
            fond = Image(fond)
        fond: Image
        self.fond_original = fond.texture
        self.fond = fond

        nom_bouton = self.button_langue[langue]
        self.taille_bouton = taille_bouton
        self.bouton = [
            Bouton(
                (0, 0),
                tecture_bouton,  # copy.deepcopy(tecture_bouton),
                taille_bouton,
                data,
            )
            for data in nom_bouton
        ]
        for bouton in self.bouton:
            bouton.redimentione_all_image(bouton.get_taille())
            for image in bouton.texture:
                place_texte_in_texture(
                    image.texture, bouton.data, pygame.font.Font(None, 50), (0, 0, 0)
                )

    button_langue = {
        "fr": ["Démarrer", "Options", "Quitter"],
        "en": ["Start", "Options", "Quit"],
    }

    def positionne_bouton(self):
        """positionne les boutons au centre de l'écran"""
        ecart = 10
        debut = (
            screen.get_height() // 2
            - (
                self.taille_bouton[1] * len(self.bouton)
                + ecart * (len(self.bouton) - 1)
            )
            // 2
        )
        for i, bouton in enumerate(self.bouton):
            bouton.set_coordonnee(
                (
                    screen.get_width() // 2 - self.taille_bouton[0] // 2,
                    debut + (self.taille_bouton[1] + ecart) * i,
                )
            )

    def actualise_dimention(self):
        """actualise la dimention
        ajuste la taille de l'image de fond pour qu'elle soit toujours visible
        et positionne les boutons au centre de l'écran
        """
        ration_fond = self.fond.get_size()[0] / self.fond.get_size()[1]
        ration_screen = screen.get_width() / screen.get_height()
        self.fond.texture = self.fond_original

        if ration_fond < ration_screen:
            self.fond.redimentione(
                (screen.get_width(), screen.get_width() // ration_fond)
            )
            self.fond.ancre = (
                0,
                -screen.get_height() // 2 + self.fond.get_size()[1] // 2,
            )
        else:
            self.fond.redimentione(
                (screen.get_height() * ration_fond, screen.get_height())
            )
            self.fond.ancre = (
                -screen.get_width() // 2 + self.fond.get_size()[0] // 2,
                0,
            )
        self.positionne_bouton()

    def actualise(self, souris):
        """actualise le menu de démarrage"""
        self.actualise_over(souris)
        return self.actualise_click(souris)

    def actualise_over(self, souris):
        """actualise les boutons"""
        for bouton in self.bouton:
            if bouton.point_dans_objet(souris.pos):
                bouton.animation = 1
            else:
                bouton.animation = 0

    def actualise_click(self, souris):
        """actualise les boutons"""
        if souris.get_pression(1) == "vien_presser":
            for bouton in self.bouton:
                if bouton.point_dans_objet(souris.pos):
                    return bouton.data
        return None

    def afficher(self):
        """affiche le menu de démarrage"""
        self.fond.afficher((0, 0))
        for bouton in self.bouton:
            bouton.afficher()

    def reset(self):
        """reset le menu de démarrage"""
        for bouton in self.bouton:
            bouton.animation = 0
        self.actualise_dimention()

    def play(self, clavier, souris) -> str:
        """joue le menu de démarrage"""
        event = actualise_event(clavier, souris)
        temp = self.actualise(souris)
        if clavier.get_pression(pygame.K_F11) == "vien_presser":
            change_fullscreen()
            event.add("redimentione")
        if "quitter" in event:
            return "quitter"
        if "redimentione" in event:
            self.actualise_dimention()

        vider_affichage((200, 200, 200))
        self.afficher()
        pygame.display.update()
        return temp
