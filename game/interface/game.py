import pygame

from game.entity.playeur import Playeur  # [import-error]
from game.entity.entity import Entity
from game.interface.contruction import MenuConstruction
from game.map.composant import Mur, Porte
from interface.class_clavier import Clavier, Souris
from interface.graphique import screen,Zone



MUR= Mur((0,0),(64,10),("textures/teste/test_mur/mur1.png",(0,54)))
FABRICATEUR = Mur((0,0),(64,10),"textures/teste/construction/fabricateur.png")

class Game:
    CADRIAGE=16
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
        self.fourniture = []
        self.mode="libre"
        self.tick=0
        self.construction=MenuConstruction()

    def actualise(self):
        self.tick+=1
        self.deplacement()
        self.interaction()
    def deplacement(self):
        if self.mode =="libre":
            self.deplacement_playeur()
            self.playeur.actualise_animation(self.tick)

    def deplacement_playeur(self):
        obstacle = self.mur+self.fourniture+[porte for porte in self.porte if porte.etat=="fermer"]
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
        pos_s=self.souris.get_pos()
        pos_p=self.playeur.get_pos()
        size_p=self.playeur.get_size()
        if self.mode=="libre":
            if self.clavier.get_pression(self.controls["interagir"]) =="vien_presser":
                # axe=None
                # if self.playeur.sens in ("haut","bas"):
                #     axe=0
                # elif self.playeur.sens in ("gauche","droite"):
                #     axe=1
                pos_z=None
                size_z=None
                longueur=65
                match self.playeur.sens:
                    case "haut":
                        pos_z=(pos_p[0],pos_p[1]-size_p[1])
                        size_z=(size_p[0],longueur)
                    case "bas":
                        pos_z=(pos_p[0],pos_p[1])
                        size_z=(size_p[0],longueur)
                    case "gauche":
                        pos_z=(pos_p[0]-size_p[0],pos_p[1])
                        size_z=(longueur,size_p[1])
                    case "droite":
                        pos_z=(pos_p[0],pos_p[1])
                        size_z=(longueur,size_p[1])
                        
                for porte in self.porte:
                    if porte.collision(pos_z,size_z):
                        if not self.playeur.collision(porte.get_pos(),porte.get_size()):
                            if porte.etat=="fermer":
                                porte.ouvrir()
                            else:
                                porte.fermer()
            if self.clavier.get_pression(self.controls["construction"]) =="vien_presser":
                self.mode="construction"
                self.construction.redimentione()

        elif self.mode=="construction":
            comp=self.construction.gestion_touche(self.controls,self.clavier)
            if comp is not None:
                # pos=corrige_grille(pos_s[0],self.CADRIAGE),corrige_grille(pos_s[1],self.CADRIAGE)
                # comp.set_pos(pos)
                self.fourniture.append(comp)
            if self.clavier.get_pression(self.controls["construction"]) =="vien_presser":
                self.mode="libre"
            

                
                    
                        
                # zone_dection
    def afficher(self):
        screen.fill((0, 0, 0))
        list_affiche=[mur for mur in self.mur if mur.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[entity for entity in self.entity if entity.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[projectille for projectille in self.projectille if projectille.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[porte for porte in self.porte if porte.imgage_dans_surface((0,0),screen.get_size())]
        list_affiche+=[fourniture for fourniture in self.fourniture if fourniture.imgage_dans_surface((0,0),screen.get_size())]
        if self.playeur.imgage_dans_surface((0,0),screen.get_size()):
            list_affiche.append(self.playeur)
        for affiche in quick_sort_y(list_affiche):
            affiche.afficher()
            
        if self.mode=="construction":
            futurcomp=self.construction.get_futurcomp()
            futurcomp.set_pos((
                corrige_grille(self.souris.get_pos()[0],self.CADRIAGE),
                corrige_grille(self.souris.get_pos()[1],self.CADRIAGE)
            ))
            futurcomp.afficher()
            self.construction.afficher()
        # pygame.display.flip()

    def redimentione(self):
        if self.mode=="construction":
            self.construction.redimentione()
    



def tri_decroisant_y(liste:list[Zone]):
    for i in range(len(liste)):
        for j in range(i+1,len(liste)):
            if liste[i].get_pos()[1]+liste[i].get_size()[1]>liste[j].get_pos()[1]+liste[j].get_size()[1]:
                liste[i],liste[j]=liste[j],liste[i]
    return liste

def quick_sort_y(liste:list[Zone]):
    if len(liste)<=1:
        return liste
    pivot=liste[0]
    list_inf=[]
    list_sup=[]
    for i in range(1,len(liste)):
        if liste[i].get_pos()[1]+liste[i].get_size()[1]<pivot.get_pos()[1]+pivot.get_size()[1]:
            list_inf.append(liste[i])
        else:
            list_sup.append(liste[i])
    return quick_sort_y(list_inf)+[pivot]+quick_sort_y(list_sup)

def corrige_grille(pos:int,taille:int)->int:
    sup = taille if pos%taille>taille//2 else 0
    return pos-pos%taille+sup
    