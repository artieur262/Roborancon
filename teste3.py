import pygame
from interface.graphique import screen, genere_texture
from menu.menu_entretext import MenuEntreText
from interface.class_clavier import Clavier, Souris
from textures import assembleur

MenuEntreText.main(
    Souris(),
    Clavier(),
    screen,
    assembleur.cadre((410, 187), (100, 100, 100), (130, 130, 130), 5),
    400,
    "fr",
    "entrez le nom d'utilisateur",
    10,
    "",
    "blacklist",
)
