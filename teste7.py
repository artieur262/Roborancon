import pygame
from interface.graphique import screen,genere_texture,place_texte_in_texture
from interface.actualisation_pygame import actualise_event

from game.entity.playeur import Playeur ,PlayeurTest
from game.interface.game import Game
from game.map.composant import Mur, Porte

# from game.inventaire.item import Item, Membre, MembreSens, Corps

from autre import save

# pylint: disable=no-member

def main(): # pylint: disable=missing-function-docstring
    test=True
    if test:
        porte=Porte((100,150),(30,10),[("textures/teste/test_porte/porte 1 pos1.png",(17,47))
            ,("textures/teste/test_porte/porte 1 pos2.png",(17,47))])
        playeur =PlayeurTest.genere_self(save.load_json("teste/playeur.json"))
        mur=[
            Mur((36,150),(64,10),("textures/teste/test_mur/mur1.png",(0,54))),
            Mur((130,150),(64,10),("textures/teste/test_mur/mur1.png",(0,54))),
            Mur((100,300),(64,10),("textures/teste/test_mur/mur1.png",(0,54)))
            ]
    else:
        porte=Porte((100,150),(30,10),[("textures/porte/porte 1 pos1.png",(17,47))
            ,("textures/porte/porte 1 pos2.png",(17,47))])
        playeur =Playeur.genere_self(save.load_json("teste/playeur.json"))
        mur=[
            Mur((36,150),(64,10),("textures/mur/mur1.png",(0,54))),
            Mur((130,150),(64,10),("textures/mur/mur1.png",(0,54))),
            Mur((100,300),(64,10),("textures/mur/mur1.png",(0,54)))
        ]
    # list_porte=[Porte((100*i1,100*i2),(100,100),["textures/porte/porte 1 pos1.png",
    #     "textures/porte/porte 1 pos2.png"])for i1 in range(10) for i2 in range(10)]
    # list_mur=[Mur((100*i1,100*i2),(100,100),"textures/mur/mur1.png")
    #           for i1 in range(10) for i2 in range(10)]
   
    
    control = save.load_json("option/control.json")[0]     
    game=Game(control, playeur, [])
    game.porte.append(porte)
    game.mur=mur
    encour=True
    clook=pygame.time.Clock()
    fps=genere_texture((100,50),(0,0,0,0))
    while encour:
        event=actualise_event(game.clavier,game.souris)
        game.actualise()
        game.afficher()
        if "quitter" in event:
            encour=False
        if "redimentione" in event:
            game.redimentione()
        fps.fill((0,0,0,0))
        place_texte_in_texture(fps,str(int(clook.get_fps())),pygame.font.Font(None,25),(255,255,255))
        screen.blit(fps,(0,0))
        pygame.display.update()
        clook.tick(60)
        
if __name__ == "__main__":
    main()


