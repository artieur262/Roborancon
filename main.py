# import pygame

import teste1

# from interface.graphique import gener_texture
from interface.start_menu import StartMenu
from interface.menu_option import MenuOption
from interface.class_clavier import Clavier, Souris


def main():
    """fonction principale"""
    langue = "fr"
    clavier = Clavier()
    souris = Souris()
    # clock = pygame.time.Clock()
    encours = True
    action = "menu_start"
    contexte = set()
    while encours:
        if action == "menu_start":
            temp = StartMenu.main(clavier, souris, langue)
            if temp == "quitter":
                encours = False
            if temp == "option":
                action = "menu_option"
                contexte.add("menu_start")
            if temp == "jouer":
                action = "jeu"
        if action == "jeu":
            teste1.main()
            action = "menu_start"
        if action == "menu_option":
            temp = MenuOption.main(clavier, souris, langue)
            if temp == "quitter":
                if "menu_start" in contexte:
                    action = "menu_start"
                    contexte.remove("menu_start")


if __name__ == "__main__":
    main()
