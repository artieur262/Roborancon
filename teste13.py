import pygame

from interface.graphique import screen, Image,LienSpritesheet
from game.entity.creature import Lezardus
LIEN_IMG = "textures/entity/passif/lezardus"
VITESSE=8
def main():
    pygame.init()
    lezardus = Lezardus.random_sauvage((150, 150), (32, 32))
    clock = pygame.time.Clock()
    image:list[Image] = LienSpritesheet(LIEN_IMG,None).decoupe()
    tick = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    lezardus.sens = "haut"
                    lezardus.actualise_animation()
                if event.key == pygame.K_s:
                    lezardus.sens = "bas"
                    lezardus.actualise_animation()
                if event.key == pygame.K_q:
                    lezardus.sens = "gauche"
                    lezardus.actualise_animation()
                if event.key == pygame.K_d:
                    lezardus.sens = "droite"
                    lezardus.actualise_animation()
                if event.key == pygame.K_SPACE:
                    lezardus.action = "rien"
                    lezardus.actualise_animation()
        if tick%VITESSE==0:
            lezardus.actualise_animation()
        screen.fill((125, 125, 125))
        lezardus.afficher((100,100),surface=screen)
        # lezardus.texture[0].afficher((200,100),surface=screen)
        # image[0].afficher((300,100),screen)
        pygame.display.flip()
        # screen.fill((255, 255, 255))
        clock.tick(60)
        tick += 1
    
if __name__ == "__main__":
    main()
