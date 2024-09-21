import pygame
from interface.graphique import screen
from textures import assembleur

# pylint: disable=no-member

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(assembleur.bouton2(2), (100, 100))
    pygame.display.update()
