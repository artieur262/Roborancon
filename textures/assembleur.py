"""Module qui contient les fonctions pour assembler les textures des blocs"""

import pygame

# pylint: disable=no-member


def bouton1(taille: list[int]):
    """crée un bouton avec des motif en fonction de la taille"""
    if taille[0] < 0:
        taille[0] = 0
    if taille[1] < 0:
        taille[1] = 0

    surface = pygame.Surface(
        (60 + taille[0] * 50, 60 + taille[1] * 50), pygame.SRCALPHA
    )

    taille_surface = surface.get_size()
    # place les coins
    coin = pygame.image.load("textures/bouton/coin1.png")

    for i in (
        ((0, 0), 0),
        ((taille_surface[0] - 30, 0), 270),
        ((0, taille_surface[1] - 30), 90),
        ((taille_surface[0] - 30, taille_surface[1] - 30), 180),
    ):
        surface.blit(pygame.transform.rotate(coin, i[1]), i[0])

    # place le dessus et le dessous
    dessus = pygame.image.load("textures/bouton/dessus1.png")

    for i in range(taille[0]):
        surface.blit(dessus, (30 + i * 50, 0))
        surface.blit(
            pygame.transform.rotate(dessus, 180), (30 + i * 50, taille_surface[1] - 30)
        )
    # place les cotes
    cote = pygame.image.load("textures/bouton/cote1.png")
    for i in range(taille[1]):
        surface.blit(cote, (0, 30 + i * 50))
        surface.blit(
            pygame.transform.rotate(cote, 180), (taille_surface[0] - 30, 30 + i * 50)
        )
    # place le centre
    centre = pygame.image.load("textures/bouton/centre1.png")
    for i in range(taille[0]):
        for j in range(taille[1]):
            surface.blit(centre, (30 + i * 50, 30 + j * 50))

    return surface
