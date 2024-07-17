import pygame

import teste
from interface.graphique import gener_texture
from interface.start_menu import StartMenu
from interface.class_clavier import Clavier, Souris


def main():
    """fonction principale"""
    langue = "fr"
    taille_bouton = (200, 50)
    texture_bouton = [gener_texture(taille_bouton, (175, 175, 175)) for _ in range(2)]
    texture_bouton[0].blit(
        gener_texture((taille_bouton[0] - 10, taille_bouton[1] - 10), (150, 150, 150)),
        (5, 5),
    )
    texture_bouton[1].blit(
        gener_texture((taille_bouton[0] - 10, taille_bouton[1] - 10), (100, 100, 100)),
        (5, 5),
    )
    fond = gener_texture((150, 150), (200, 200, 200))
    fond = r".git\IMG_4840.jpg"
    start_menu = StartMenu(fond, texture_bouton, taille_bouton, langue)
    clavier = Clavier()
    souris = Souris()

    encours = True
    start_menu.reset()

    clock = pygame.time.Clock()
    while encours:

        temp = start_menu.play(clavier, souris)
        if "jouer" == temp or start_menu.button_langue[langue][0] == temp:
            teste.main()
        if "quitter" == temp or start_menu.button_langue[langue][2] == temp:
            encours = False
        clock.tick(90)


if __name__ == "__main__":
    main()
