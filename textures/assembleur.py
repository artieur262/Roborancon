"""Module qui contient les fonctions pour assembler les textures des blocs"""

import pygame

# pylint: disable=no-member


def gener_texture(taille: tuple[int, int], color: tuple) -> pygame.Surface:
    """génere une texture rectangulaire

    Args:
        taile (tuple[int]): (x,y) est la taille de la texture
        color (tuple[int]): (Red,Green,Blue,trasparence "optionel") est la couleur de l'image

    Returns:
        Surface: est l'image généré
    """

    if len(color) == 3:  # permet de pas forcer de metre des couleurs
        # print(taille)
        image = pygame.Surface(taille)
        image.fill(color)
    elif len(color) == 4:
        image = pygame.Surface(taille, pygame.SRCALPHA)
        image.fill(color)
    return image


def arc_ciel(taille: list[int], decalage: int = 0):
    """génere une texture arc en ciel
    créer à cause de lgwythyr
    je n'avais pas le choix
    (viens d'un autre projet)

    agrs:
        taille (list[int]) : est la taille de l'image
        decalage (int) : est le décalage de l'arc en ciel
    """
    couleur = [
        (255, 0, 0),
        (255, 125, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (125, 0, 255),
    ]
    min_taille = 0
    if taille[0] < taille[1]:
        min_taille = taille[0]
    else:
        min_taille = taille[1]
        texture = gener_texture(taille, couleur[0 + decalage])
    for i in range(1, min_taille // 10):
        texture.blit(
            gener_texture(
                [taille[0] - 10 * i, taille[1] - i * 10],
                couleur[(i + decalage) % len(couleur)],
            ),
            (i * 5, i * 5),
        )
    return texture


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
    coin1 = pygame.image.load("textures/bouton/bouton1/coin1.1.png")

    surface.blit(coin1, (0, 0))
    surface.blit(
        pygame.transform.rotate(coin1, 180),
        (taille_surface[0] - 30, taille_surface[1] - 30),
    )

    coin2 = pygame.image.load("textures/bouton/bouton1/coin1.2.png")
    surface.blit(coin2, (taille_surface[0] - 30, 0))
    surface.blit(pygame.transform.rotate(coin2, 180), (0, taille_surface[1] - 30))

    # place le dessus et le dessous
    dessus = pygame.image.load("textures/bouton/bouton1/dessus1.png")

    for i in range(taille[0]):
        surface.blit(dessus, (30 + i * 50, 0))
        surface.blit(
            pygame.transform.rotate(dessus, 180), (30 + i * 50, taille_surface[1] - 30)
        )
    # place les cotes
    cote = pygame.image.load("textures/bouton/bouton1/cote1.png")
    for i in range(taille[1]):
        surface.blit(cote, (0, 30 + i * 50))
        surface.blit(
            pygame.transform.rotate(cote, 180), (taille_surface[0] - 30, 30 + i * 50)
        )
    # place le centre
    centre = pygame.image.load("textures/bouton/bouton1/centre1.png")
    for i in range(taille[0]):
        for j in range(taille[1]):
            surface.blit(centre, (30 + i * 50, 30 + j * 50))

    return surface


def bouton2(longueur: int, variante: int = 1):
    """crée un bouton avec des motif en fonction de la longueur
    args:
        longueur (int) : est la longueur du bouton
        variante (int) : est la variante du bouton variant de 1 à 3

    """
    longueur = longueur - 100
    if longueur < 0:
        longueur = 0
    texture = gener_texture((longueur + 100, 50), (0, 0, 0, 0))
    texture.blit(
        pygame.image.load(f"textures/bouton/bouton2/bord2.1_V{variante}.png"), (0, 0)
    )
    for i in range(longueur // 50 + (0 if longueur % 50 == 0 else 1)):
        texture.blit(
            pygame.image.load(f"textures/bouton/bouton2/milieu2_V{variante}.png"),
            (50 + i * 50, 0),
        )

    texture.blit(
        pygame.image.load(f"textures/bouton/bouton2/bord2.2_V{variante}.png"),
        (50 + longueur, 0),
    )
    return texture


def cadre(
    taille: tuple[int, int], couleur_1: list[int], couleur_2: list[int], marge: int
):
    """génere un cadre avec une couleur de fond et une couleur de bordure"""
    texture = gener_texture(taille, couleur_1)
    texture.blit(
        gener_texture((taille[0] - marge * 2, taille[1] - marge * 2), couleur_2),
        (marge, marge),
    )
    return texture
