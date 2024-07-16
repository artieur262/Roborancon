import pygame

from interface.graphique import screen, place_texte_in_texture, gener_texture
from interface.actualisation_pygame import actualise_event, change_fullscreen
from interface.class_clavier import Clavier, Souris
from interface.scrolling_bar import ScrollBar

# pylint: disable=no-member

clavier = Clavier()
souris = Souris()
scrollbar = ScrollBar(
    (100, 100),
    (20, 200),
    gener_texture((1, 1), (125, 125, 125)),
    gener_texture((1, 1), (175, 175, 175)),
    50,
    "vertical",
)
indicateur = gener_texture((300, 50), (230, 230, 230))

while True:
    event_autre = actualise_event(clavier, souris)
    if "quitter" in event_autre:
        break
    if "redimentione" in event_autre:
        screen.fill((0, 0, 0))
        pygame.display.update()
    scrollbar.souris_scroll(souris.pos)
    screen.fill((0, 0, 0))
    scrollbar.afficher()
    indicateur.fill((230, 230, 230))
    indicateur.blit(
        place_texte_in_texture(
            indicateur,
            str(round(scrollbar.get_pourcentage(),3)),
            pygame.font.Font(None, 50),
            (0, 0, 0),
        ),
        (0, 0),
    )
    screen.blit(indicateur, (400, 100))
    pygame.display.update()
    pygame.time.Clock().tick(60)
