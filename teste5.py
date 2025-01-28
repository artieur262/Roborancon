import time
import pygame
from interface.graphique import screen,genere_texture,place_texte_in_texture
from interface import convert_text
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
    aide=False
    aide_text=genere_texture((400,250),(0,0,0,0))
    aide_text=place_texte_in_texture(aide_text,"- z et s pour monter et descendre\n\n"+
                                     "- espace pour marcher\n\n"+
                                     "- shift pour courir\n\n"+
                                     "- r pour reset la position\n\n"+
                                     "- haute et bas pour changer la vitesse_min\n\n"+
                                     "- droite et gauche pour changer la vitesse_max\n\n",
                                     pygame.font.Font(None, 36),(0,0,0),"haut_droit")
    list_text = [genere_texture((250,25),(0,0,0,0)) for _ in range(6)]
    playeur.set_pos((200, 110))
    encour=True
    while encour:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    encour = False
                if event.key == pygame.K_SPACE:
                    action = "marche" if action == "rien" else "rien"
                    if action == "rien":
                        playeur.arrete()
                if event.key == pygame.K_h:
                    aide = not aide
                if event.key == pygame.K_r:
                    playeur.set_pos((200, 110))
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
            playeur.marche(sens,[],tick)
        if action == "courir":
            playeur.action = "courir"
            playeur.courir(sens,[],tick)
        if playeur.get_pos()[1] > screen.get_height():
            playeur.set_pos((200, -playeur.get_size()[1]))
        if playeur.get_pos()[1] < -playeur.get_size()[1]:
            playeur.set_pos((200, screen.get_height()))
        playeur.afficher()
        list_text[0]=place_texte_in_texture(list_text[0],"action : "+action,pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[1]=place_texte_in_texture(list_text[1],"sens : "+sens,pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[2]=place_texte_in_texture(list_text[2],"vitesse_min : "+str(playeur.stats["vitesse_min"]),pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[3]=place_texte_in_texture(list_text[3],"vitesse_max : "+str(playeur.stats["vitesse_max"]),pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[4]=place_texte_in_texture(list_text[4],"tick : "+str(tick),pygame.font.Font(None, 36),(0,0,0),"haut_gauche")
        list_text[5]=place_texte_in_texture(list_text[5],"h pour de l'aide",pygame.font.Font(None, 36),(0,0,0),"haut_gauche")   
                                      
        for i,text in enumerate(list_text):
            screen.blit(text,(0,25*i))
        if aide:
            screen.blit(aide_text,(screen.get_width()-410,0))
        pygame.display.flip()
        clok.tick(60)
        tick += 1
if __name__ == "__main__":
    main()
