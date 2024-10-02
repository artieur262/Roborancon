import pygame
from textures import assembleur
from interface.graphique import screen
img1=assembleur.cadre((200,200),(0,0,0),(255,255,255),5)
rect = pygame.Rect(0, 0, 100, 100)
img1:pygame.Surface
img2=img1.subsurface(rect)
screen.fill((125,125,125))
screen.blit(img1,(10,10))
screen.blit(img2,(10,220))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    pygame.display.flip()