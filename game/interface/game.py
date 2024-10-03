import pygame

from game.entity.playeur import Playeur  # [import-error]
from game.entity.entity import Entity
from game.map.map import Mur, Porte
from interface.class_clavier import Clavier, Souris
from interface.graphique import screen,Zone



class Game:
    def __init__(
        self,
        controls: dict[str, int],
        playeur: Playeur,
        entity: list[Entity],
    ):
        self.playeur = playeur
        self.clavier = Clavier()
        self.souris = Souris()
        self.controls = controls
        self.entity = entity
        self.projectille = []
        self.mur:list[Mur] = []
        self.porte:list[Porte] = []
        self.mode="libre"
        self.tick=0
    def actualise(self):
        self.tick+=1
        self.deplacement()
        self.interaction()
    def deplacement(self):
        if self.mode =="libre":
            self.deplacement_playeur()
            self.playeur.actualise_animation(self.tick)

    def deplacement_playeur(self):
        obstacle = self.mur+[porte for porte in self.porte if porte.etat=="ferme"]
        if self.clavier.get_pression(self.controls["courir"])in ("presser","vien_presser"):
            if self.clavier.get_pression(self.controls["haut"])in ("presser","vien_presser"):
                self.playeur.courir("haut",obstacle,self.tick)
            elif self.clavier.get_pression(self.controls["bas"])in ("presser","vien_presser"):
                self.playeur.courir("bas",obstacle,self.tick)
            elif self.clavier.get_pression(self.controls["gauche"])in ("presser","vien_presser"):
                self.playeur.courir("gauche",obstacle,self.tick)
            elif self.clavier.get_pression(self.controls["droite"])in ("presser","vien_presser"):
                self.playeur.courir("droite",obstacle,self.tick)
            else:
                self.playeur.arrete()
        else:
            if self.clavier.get_pression(self.controls["haut"])in ("presser","vien_presser"):
                self.playeur.marche("haut",obstacle,self.tick)
            elif self.clavier.get_pression(self.controls["bas"])in ("presser","vien_presser"):
                self.playeur.marche("bas",obstacle,self.tick)
            elif self.clavier.get_pression(self.controls["gauche"])in ("presser","vien_presser"):
                self.playeur.marche("gauche",obstacle,self.tick)
            elif self.clavier.get_pression(self.controls["droite"])in ("presser","vien_presser"):
                self.playeur.marche("droite",obstacle,self.tick)
            else:
                self.playeur.arrete()
    def interaction(self):
        pos_p=self.playeur.get_pos()
        size_p=self.playeur.get_size()
        if self.clavier.get_pression(self.controls["interagir"]) =="vien_presser":
            match self.playeur.sens:
                case "bas":
                    zone_dection=Zone([pos_p[0]-12,pos_p[1]+size_p[1]],(50,100))
                case "haut":
                    zone_dection=Zone((pos_p[0]-12,pos_p[1]-100),(50,100)) 
                case "gauche":
                    zone_dection=Zone((pos_p[0]-100,pos_p[1]-12),(100,50))
                case "droite":
                    zone_dection=Zone([pos_p[0]+size_p[0],pos_p[1]-12],(100,50))
                    
            for porte in self.porte:
                if not porte.collision(pos_p,size_p) and porte.collision(zone_dection.get_pos(),zone_dection.get_size()):
                    porte.ouvrir_fermer()
                    
            # zone_dection
    def afficher(self):
        screen.fill((0, 0, 0))
        list_affiche=[mur for mur in self.mur if mur.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[entity for entity in self.entity if entity.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[projectille for projectille in self.projectille if projectille.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[porte for porte in self.porte if porte.imgage_dans_surface((0,0),screen.get_size())]
        if self.playeur.imgage_dans_surface((0,0),screen.get_size()):
            list_affiche.append(self.playeur)

        for affiche in quick_sort_y(list_affiche):
            affiche.afficher()
            
        # pygame.display.flip()
    

def tri_decroisant_y(list:list[Zone]):
    for i in range(len(list)):
        for j in range(i+1,len(list)):
            if list[i].get_pos()[1]+list[i].get_size()[1]>list[j].get_pos()[1]+list[j].get_size()[1]:
                list[i],list[j]=list[j],list[i]
    return list

def quick_sort_y(list:list[Zone]):
    if len(list)<=1:
        return list
    pivot=list[0]
    list_inf=[]
    list_sup=[]
    for i in range(1,len(list)):
        if list[i].get_pos()[1]+list[i].get_size()[1]<pivot.get_pos()[1]+pivot.get_size()[1]:
            list_inf.append(list[i])
        else:
            list_sup.append(list[i])
    return quick_sort_y(list_inf)+[pivot]+quick_sort_y(list_sup)