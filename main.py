# import pygame

import teste

# from interface.graphique import gener_texture
from interface.start_menu import StartMenu
from interface.class_clavier import Clavier, Souris


def main():
    """fonction principale"""
    langue = "fr"
    clavier = Clavier()
    souris = Souris()
    # clock = pygame.time.Clock()
    encours = True
    action = "menu_start"
    while encours:
        if action == "menu_start":
            temp = StartMenu.main(clavier, souris, langue)
            if temp == "quitter":
                encours = False
            if temp == "jouer":
                action = "jeu"
        if action == "jeu":
            teste.main()
            action = "menu_start"


if __name__ == "__main__":
    main()
