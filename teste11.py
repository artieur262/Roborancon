import pygame
from interface.graphique import screen,LienSpritesheet,Image
from game.entity.playeur import Playeur
from autre import save

LIEN_JOUER = "teste/playeur.json"
TESTE_PLAYEUR = "textures/teste/test_playeur/imgset"
BRAS_G = "textures/entity/playeur/bras g/bras g"
def main():
    decalage = (21, 37)

    playeur=Playeur.genere_self(save.load_json(LIEN_JOUER))
    playeur.set_pos(decalage)
    image:list[Image] = LienSpritesheet(BRAS_G,None).decoupe()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # for i in range(len(image)):
        #     image[i].afficher(((i%3)*64+decalage[0], i//3*64+decalage[1]),screen)
        playeur.afficher(surface=screen)
        playeur.membre_equipe["bras_gauche"].get_texture(0).afficher(decalage,screen)

        pygame.display.flip()
        screen.fill((255, 255, 255))

if __name__ == "__main__":
    main()