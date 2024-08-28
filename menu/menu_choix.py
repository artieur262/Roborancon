"""Module qui gère les choix dans un menu

class:
    - MenuChoix
"""

import pygame

from interface.actualisation_pygame import actualise_event, change_fullscreen
from interface.graphique import (
    ObjetGraphique,
    Image,
    screen,
    genere_texture,
    place_texte_in_texture,
    decoupe_texte,
)
from interface.bouton import BoutonText
from interface.class_clavier import Clavier, Souris
from textures import assembleur

# pylint: disable=no-member


class MenuChoix:
    """Classe qui gère les choix"""

    def __init__(
        self,
        fond: pygame.Surface | str | Image,
        texte: str,
        boutons: list[str],
    ):

        self.__fond = ObjetGraphique((0, 0), [fond], (1, 1))
        self.__fond.set_size(self.__fond.image_actuel().get_size())
        police_texte = pygame.font.Font(None, 45)
        police_bouton = pygame.font.Font(None, 25)
        taille_bouton = max([police_bouton.size(bouton)[0] for bouton in boutons]) + 20
        if taille_bouton < 100:
            taille_bouton = 100
        ecart_entre_bouton = 30
        taille_zone_texte = (
            (taille_bouton + ecart_entre_bouton) * len(boutons) - ecart_entre_bouton,
            len(
                decoupe_texte(
                    texte,
                    (taille_bouton + ecart_entre_bouton) * len(boutons)
                    - ecart_entre_bouton,
                    police_texte,
                )
            )
            * 50,
        )
        self.__zone_texte = ObjetGraphique(
            (0, 0), [genere_texture(taille_zone_texte, (0, 0, 0, 0))], taille_zone_texte
        )
        self.__zone_texte.texture[0].texture = place_texte_in_texture(
            self.__zone_texte.texture[0].texture, texte, police_texte, (0, 0, 0)
        )
        self.boutons = [
            BoutonText(
                (0, 0),
                [assembleur.bouton2(taille_bouton, i) for i in (1, 2)],
                (taille_bouton, 50),
                bouton,
                (0, 0, 0),
                police_bouton,
                data=bouton,
            )
            for bouton in boutons
        ]

    def afficher(self):
        """affiche l'objet"""
        self.__fond.afficher()
        self.__zone_texte.afficher()
        for bouton in self.boutons:
            bouton.afficher()

    def actualise_dimension(self):
        """actualise les dimensions des objets"""
        self.__fond.set_pos(
            (
                screen.get_width() // 2 - self.__fond.get_size()[0] // 2,
                screen.get_height() // 2 - self.__fond.get_size()[1] + 70,
            )
        )
        self.__zone_texte.set_pos(
            (
                screen.get_width() // 2 - self.__zone_texte.get_size()[0] // 2,
                screen.get_height() // 2 - self.__zone_texte.get_size()[1],
            )
        )

        for i, bouton in enumerate(self.boutons):
            bouton.set_pos(
                (
                    screen.get_width() // 2
                    - (len(self.boutons) * (bouton.get_size()[0] + 30) - 30) // 2
                    + i * (bouton.get_size()[0] + 30),
                    screen.get_height() // 2 + 10,
                )
            )

    def hover(self, souris: Souris):
        """gere le survol des boutons"""
        for bouton in self.boutons:
            if bouton.point_dans_objet(souris.get_pos()):
                bouton.animation = 1
            else:
                bouton.animation = 0

    def click(self, souris: Souris):
        """gere le click sur les boutons"""
        if souris.get_pression(1) == "vien_presser":
            for bouton in self.boutons:
                if bouton.point_dans_objet(souris.get_pos()):
                    return bouton.get_data()
        return None

    def actualise(self, souris: Souris):
        """actualise l'objet"""
        self.actualise_dimension()
        self.hover(souris)
        return self.click(souris)

    def play(self, souris: Souris):
        """affiche l'objet et le fait interagir avec l'utilisateur"""
        return self.actualise(souris)

    @staticmethod
    def main(
        clavier: Clavier,
        souris: Souris,
        fond_autre: pygame.Surface | str | Image,
        fond_menu: pygame.Surface | str | Image,
        texte: str,
        boutons: list[str],
    ):
        """cree un choix et le fait apparaitre jusqu'a ce qu'il disparaisse"""
        choix = MenuChoix(fond_menu, texte, boutons)
        choix.actualise_dimension()
        fond = ObjetGraphique((0, 0), [fond_autre], (1, 1))
        fond.set_size(fond.image_actuel().get_size())
        fond.set_pos(
            (
                screen.get_width() // 2 - fond.get_size()[0] // 2,
                screen.get_height() // 2 - fond.get_size()[1] // 2,
            )
        )
        fond.set_size(fond.image_actuel().get_size())
        clock = pygame.time.Clock()
        encour = True
        while encour:
            event = actualise_event(clavier, souris)
            if clavier.get_pression(pygame.K_F11) == "vien_presser":
                change_fullscreen()
                event.add("redimentione")
            if "redimentione" in event:
                choix.actualise_dimension()
                fond.set_pos(
                    (
                        screen.get_width() // 2 - fond.get_size()[0] // 2,
                        screen.get_height() // 2 - fond.get_size()[1] // 2,
                    )
                )
            fond.afficher()
            choix.afficher()

            temp = choix.play(souris)
            if temp is not None:
                encour = False
            pygame.display.update()
            clock.tick(60)
        return temp
