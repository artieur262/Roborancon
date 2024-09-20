import pygame
from interface.graphique import screen
from interface.actualisation_pygame import actualise_event
from game.entity.playeur import Playeur
from game.inventaire.item import Item, Membre, MembreSens, Corps
from game.map import Mur, Porte
from game.interface.game import Game
from autre import save

# pylint: disable=no-member

def main():
    porte=Porte((100,100),(100,100),["textures/porte/porte 1 pos1.png"
        ,"textures/porte/porte 1 pos2.png"])
    # list_porte=[Porte((100*i1,100*i2),(100,100),["textures/porte/porte 1 pos1.png"
    #     ,"textures/porte/porte 1 pos2.png"])for i1 in range(10) for i2 in range(10)]
    # list_mur=[Mur((100*i1,100*i2),(100,100),"textures/mur/mur1.png")for i1 in range(10) for i2 in range(10)]  
    mur=Mur((100,300),(100,100),"textures/mur/mur1.png")
    playeur =Playeur.genere_self(save.load_json("teste/playeur.json"))
    control = save.load_json("option/control.json")[0]
    game=Game(control, playeur, [])
    game.porte.append(porte)
    game.mur.append(mur)
    encour=True
    clook=pygame.time.Clock()
    while encour:
        event=actualise_event(game.clavier,game.souris)
        game.actualise()
        game.afficher()
        if "quitter" in event:
            encour=False
        clook.tick(60)
main()


