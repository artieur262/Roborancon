import pygame

from interface.graphique import screen, place_texte_in_texture, genere_texture
from interface.actualisation_pygame import actualise_event, change_fullscreen
from interface.class_clavier import Clavier, Souris
from interface.scrolling_bar import ScrollBar


# pylint: disable=no-member
def main():
    """fonction principale"""
    clavier = Clavier()
    souris = Souris()
    scrollbar1 = ScrollBar(
        (100, 100),
        (20, 200),
        genere_texture((1, 1), (125, 125, 125)),
        genere_texture((1, 1), (175, 175, 175)),
        50,
        "vertical",
    )
    scrollbar2 = ScrollBar(
        (200, 100),
        (200, 20),
        genere_texture((1, 1), (125, 125, 125)),
        genere_texture((1, 1), (175, 175, 175)),
        50,
        "horizontal",
    )
    indicateur1 = genere_texture((300, 50), (230, 230, 230))
    indicateur2 = genere_texture((300, 50), (230, 230, 230))

    while True:
        event_autre = actualise_event(clavier, souris)
        if (
            "quitter" in event_autre
            or clavier.get_pression(pygame.K_ESCAPE) == "vien_presser"
        ):
            break
        if clavier.get_pression(pygame.K_F11) == "vien_presser":
            change_fullscreen()
            event_autre.add("redimentione")
        if "redimentione" in event_autre:
            screen.fill((0, 0, 0))
            pygame.display.update()
        if souris.get_pression(1) == "vien_presser":
            if scrollbar1.point_dans_objet(souris.pos):
                scrollbar1.activer()
            if scrollbar2.point_dans_objet(souris.pos):
                scrollbar2.activer()
        if souris.get_pression(1) == "vien_lacher":
            scrollbar1.desactiver()
            scrollbar2.desactiver()

        scrollbar1.souris_scroll(souris.pos)
        scrollbar2.souris_scroll(souris.pos)
        screen.fill((0, 0, 0))
        scrollbar1.afficher()
        scrollbar2.afficher()
        indicateur1.fill((230, 230, 230))
        indicateur1.blit(
            place_texte_in_texture(
                indicateur1,
                str(round(scrollbar1.get_pourcentage(), 3)),
                pygame.font.Font(None, 50),
                (0, 0, 0),
            ),
            (0, 0),
        )
        indicateur2.fill((230, 230, 230))
        indicateur2.blit(
            place_texte_in_texture(
                indicateur2,
                str(round(scrollbar2.get_pourcentage(), 3)),
                pygame.font.Font(None, 50),
                (0, 0, 0),
            ),
            (0, 0),
        )
        screen.blit(indicateur1, (100, 400))
        screen.blit(indicateur2, (600, 100))
        pygame.display.update()
        pygame.time.Clock().tick(60)
