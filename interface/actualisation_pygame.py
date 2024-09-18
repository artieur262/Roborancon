"""module pour actualiser les événement de pygame

il y a 3 fonctions:
    - actualise_event : actualise les événement et retourne 
                        les événement autre que les touches et les cliques
    - get_fullscreen : retourne si on est en plein écran
    - change_fullscreen : change le mode plein écran"""

# pylint: disable=no-member
import pygame

from interface.graphique import screen
from interface.class_clavier import Clavier, Souris


def actualise_event(clavier: Clavier, souris: Souris) -> set:
    """actualise les événement et retourne les événement autre que les touches et les cliques
    
    return set["quitter","redimentione"]
    """
    event_autre = set()
    souris.actualise_all_clique()
    clavier.update_all_key()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            event_autre.add("quitter")
        elif event.type in (
            pygame.VIDEORESIZE,
            pygame.WINDOWSIZECHANGED,
        ):
            event_autre.add("redimentione")

        elif event.type == pygame.KEYDOWN:
            clavier.set_pression(event.key, "vien_presser")

        elif event.type == pygame.KEYUP:
            clavier.set_pression(event.key, "vien_lacher")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            souris.set_pression(event.button, "vien_presser")

        elif event.type == pygame.MOUSEBUTTONUP:
            souris.set_pression(event.button, "vien_lacher")
        # if event.type not in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
        #     print(event)

    souris.update_pos()
    return event_autre


def get_fullscreen():
    """retourne si on est en plein écran"""
    return screen.get_flags() & pygame.FULLSCREEN


def change_fullscreen():
    """change le mode plein écran"""
    global screen  # pylint: disable=global-statement

    if get_fullscreen():
        screen.fill((0, 0, 0))
        pygame.display.update()
        # premet d'eviter un bug graphique avec le plein écran
        # le bug est un clignotement noir de l'écran quand on change de mode
        # si l'écran est noir donc on ne le voit pas
        # oui je corrige un bug graphique à la schlague
        # car en plus le bug vien de pygame et pas de moi
        screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)

    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
