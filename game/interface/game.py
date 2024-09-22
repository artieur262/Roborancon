import pygame

from game.entity.playeur import Playeur  # [import-error]
from game.entity.entity import Entity
from game.map import Mur, Porte
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
        self.mur:Mur = []
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
        if self.clavier.get_pression(self.controls["interagir"]) =="vien_presser":
            if self.playeur.sens=="bas":
                pos_p=self.playeur.get_pos()
                size_p=self.playeur.get_size()
                zone_dection=Zone([pos_p[0],pos_p[1]+size_p[1]],(50,100))
            elif self.playeur.sens=="haut":
                pos_p=self.playeur.get_pos()
                zone_dection=Zone((pos_p[0],pos_p[1]-100),(50,100)) 
           
            for porte in self.porte:
                if porte.collision(zone_dection.get_pos(),zone_dection.get_size()):
                    porte.ouvrir_fermer()
                    
            # zone_dection
    def afficher(self):
        screen.fill((0, 0, 0))
        self.playeur.afficher()
        for entity in self.entity:
            entity.afficher()
        for projectille in self.projectille:
            projectille.afficher()
        for mur in self.mur:
            mur.afficher()
        for porte in self.porte:
            porte.afficher()
            
        pygame.display.flip()
    
