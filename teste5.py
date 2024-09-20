import time
import pygame
from interface.graphique import screen,genere_texture,place_texte_in_texture
from game.entity.playeur import Playeur
from game.inventaire.item import Item, Membre, MembreSens, Corps
from autre import save

# pylint: disable=no-member

def main():
    playeur=Playeur.genere_self(save.load_json("teste/playeur.json"))

    playeur.action = "marche_bas"
    clok = pygame.time.Clock()
    tick = 0
    action="rien"
    sens="bas"
    list_text = [genere_texture((250,25),(0,0,0,0)) for _ in range(4)]
    playeur.set_pos((100, 10))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    action = "marche" if action == "rien" else "rien"
                    if action == "rien":
                        playeur.arrete()
                if event.key == pygame.K_r:
                    playeur.set_pos((100, 10))
                if event.key == pygame.K_UP:
                    playeur.stats["vitesse_min"] += 1
                if event.key == pygame.K_DOWN:
                    playeur.stats["vitesse_min"] -= 1
                if event.key == pygame.K_RIGHT:
                    playeur.stats["vitesse_max"] += 1
                if event.key == pygame.K_LEFT:
                    playeur.stats["vitesse_max"] -= 1
                if event.key == pygame.K_LSHIFT:
                    action = "marche" if action == "courir" else "courir"
                if event.key == pygame.K_s:
                    if sens == "bas":
                        sens = "haut"
                    else:
                        sens = "bas"
        
        screen.fill((200, 200, 200))
        for text in list_text:
            text.fill((0, 0, 0, 0))
        # if tick % 7 == 0:
        #     playeur.actualise_animation(tick)
        #     if playeur.action == "marche_bas":
        #         playeur.add_pos((0, vitesse))
        #     if playeur.action == "marche_haut":
        #         playeur.add_pos((0, -vitesse))
        playeur.actualise_animation(tick)
        if action == "marche":
            playeur.action = "marche"
            playeur.marche(sens,tick)
        if action == "courir":
            playeur.action = "courir"
            playeur.courir(sens,tick)
        
        playeur.afficher((-100, -100))
        list_text[0]=place_texte_in_texture(list_text[0],"action : "+action,pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[1]=place_texte_in_texture(list_text[1],"sens : "+sens,pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[2]=place_texte_in_texture(list_text[2],"vitesse_min : "+str(playeur.stats["vitesse_min"]),pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[3]=place_texte_in_texture(list_text[3],"vitesse_max : "+str(playeur.stats["vitesse_max"]),pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        for i,text in enumerate(list_text):
            screen.blit(text,(0,25*i))
        pygame.display.flip()
        clok.tick(60)
        tick += 1
main()