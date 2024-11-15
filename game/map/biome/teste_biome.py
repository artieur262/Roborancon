import random
import pygame
from game.map.module import Module, SousModule
from game.map.composant import Composant,Sol
from game.map.class_Biome import Biome
from interface.graphique import LienSpritesheet, Image

class TesteBiome(Biome):
    def __init__(self, seed):
        random.seed(seed)
        self.taille_grille = (20, 20)
        self.echelle = (32,32)
        self.taille = (self.taille_grille[0]*self.echelle[0], self.taille_grille[1]*self.echelle[1])
        self.fond = pygame.Surface(self.taille, pygame.SRCALPHA)
        self.fond.fill((0, 0, 0, 0))
        self.composants:list[Composant] = []
        self.sol = []
        self.image = LienSpritesheet("textures/herbe.png",(32,32)).decoupe()
        self.grille_fond = [["vide" for _ in range(self.taille_grille[0])] for _ in range(self.taille_grille[1])]
        self.grille_comp = [["vide" for _ in range(self.taille_grille[0])] for _ in range(self.taille_grille[1])]

    def get_fond(self)->pygame.Surface:
        """Retourne le fond du biome"""
        return self.fond

    def get_comp(self)->list:
        """Retourne les composants du biome"""
        return self.composants

    def genere_grille(self):
        """Génère la grille du biome"""
        
        pos_herbe_cyan = []
        #ajout de l'herbe_cyan
        for _ in range(random.randint(1, 5)):
            y = random.randint(0, self.taille_grille[0]-1)
            x = random.randint(0, self.taille_grille[1]-1)
            self.grille_fond[x][y] = "herbe_cyan"
            pos_herbe_cyan.append((y, x))
        
        
        
        # propagation de l'herbe_cyan
        for _ in range(random.randint(1,10)):
            for pos in pos_herbe_cyan:
                if random.random() < 0.5:
                    y = pos[0] + random.randint(-1, 1)
                    x = pos[1] + random.randint(-1, 1)
                    if 0 <= y < self.taille_grille[0] and 0 <= x < self.taille_grille[1] and (y!=0 or x!=0):
                        self.grille_fond[x][y] = "herbe_cyan"
                        pos_herbe_cyan.append((y, x))
        
        # self.grille_fond[4][5] = "herbe_cyan"
        # self.grille_fond[5][4] = "herbe_cyan"
        # self.grille_fond[6][5] = "herbe_cyan"

        #place l'herbe_bleu la ou il n'y a pas de l'herbe_cyan
        for x in range(self.taille_grille[0]):
            for y in range(self.taille_grille[1]):
                if self.grille_fond[x][y] == "vide":
                    self.grille_fond[x][y] = "herbe_bleu"

        # ajout de l'herbe_cyan si au moin 3 autre herbe_cyan la touche 
        for x in range(self.taille_grille[0]):
            for y in range(self.taille_grille[1]):
                if "herbe_bleu"==self.grille_fond[x][y]:
                    autours = self.get_autour((x,y))
                    if (sum(("herbe_cyan"==autours[1], "herbe_cyan"==autours[3], "herbe_cyan"==autours[4],"herbe_cyan"==autours[6]))>=3):
                        self.grille_fond[x][y] = "herbe_cyan"
        
    def genere_comp(self):
        """Génère les composants du biome"""
        for x in range(self.taille_grille[0]):
            for y in range(self.taille_grille[1]):
                if self.grille_fond[x][y] == "herbe_cyan":
                    self.sol.append(self.genère_herbe((x,y),self.echelle))
                if self.grille_fond[x][y] == "herbe_bleu":
                    self.sol.append(self.genère_herbe((x,y),self.echelle))
                    
        for sol in self.sol:
            sol.afficher(surface=self.fond)
    
    def get_autour(self,pos:tuple[int,int])->list[str]:
        """Retourne les éléments autour de la position"""
        autour = []
        for x in range(-1,2):
            for y in range(-1,2):
                if 0 <= pos[0]+x < self.taille_grille[0] and 0 <= pos[1]+y < self.taille_grille[1] and (x!=0 or y!=0):
                    autour.append(self.grille_fond[pos[0]+x][pos[1]+y])
                elif x!=0 or y!=0:
                    autour.append("border")
        return autour
    def genère_herbe(self,pos:tuple[int,int],taille:tuple[int,int])->Sol:
        """Génère de l'herbe selon l'herbe autour dans la grille"""
        autour = self.get_autour(pos)
        debug = True
        if debug:
            if self.grille_fond[pos[0]][pos[1]] == "herbe_cyan":
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[7])
            if self.grille_fond[pos[0]][pos[1]] == "herbe_bleu":
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[10])
        if self.grille_fond[pos[0]][pos[1]] == "herbe_cyan":
            if "herbe_bleu"== autour[1] or "herbe_bleu"== autour[3] or "herbe_bleu"== autour[4] or "herbe_bleu"== autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([22,23])])
            if "herbe_bleu"== autour[0] or "herbe_bleu"== autour[2] or "herbe_bleu"== autour[5] or "herbe_bleu"== autour[7]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([7,23])])
            return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[7])
        elif self.grille_fond[pos[0]][pos[1]] == "herbe_bleu":
            #coin inverse
            if "herbe_cyan"==autour[1] and "herbe_cyan"==autour[3]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[3])
            if "herbe_cyan"==autour[1] and "herbe_cyan"==autour[4]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[15])
            if "herbe_cyan"==autour[4] and "herbe_cyan"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[17])
            if "herbe_cyan"==autour[3] and "herbe_cyan"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[5])
            
            #coté
            if "herbe_cyan"== autour[1]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([8,9])])
            if "herbe_cyan"== autour[3]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([13,4])])
            if "herbe_cyan"== autour[4]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([1,16])])
            if "herbe_cyan"== autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([6,11])])
            
            #double coin
            if "herbe_cyan"==autour[0] and "herbe_cyan"==autour[7]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[19])
            if "herbe_cyan"==autour[2] and "herbe_cyan"==autour[5]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[18])

            #Coin 
            if "herbe_cyan"==autour[0]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[14])
            if "herbe_cyan"==autour[2]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[2])
            if "herbe_cyan"==autour[5]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[12])
            if "herbe_cyan"==autour[7]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[0])
            
            rand=random.randint(0,100)
            if rand<75 :
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[10])
            if rand<98:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[20])
            return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[21])
        if self.grille_fond[pos[0]][pos[1]] == "bug":
            return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[24])

            
class Maison(Module):
    def genere_comp(self)->Composant:
        """Génère les composants du module"""
        taille = (10,5)
        




