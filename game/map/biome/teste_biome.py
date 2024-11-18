import random
import pygame
from game.map.module import Module, SousModule
from game.map.composant import Composant,Sol
from game.map.class_Biome import Biome
from interface.graphique import LienSpritesheet, Image

class TesteBiome(Biome):
    def __init__(self, seed):
        random.seed(seed)
        self.taille_grille = (30, 18)
        self.echelle = (32,32)
        self.taille = (self.taille_grille[0]*self.echelle[0], self.taille_grille[1]*self.echelle[1])
        self.fond = pygame.Surface(self.taille, pygame.SRCALPHA)
        self.fond.fill((0, 0, 0, 0))
        self.composants:list[Composant] = []
        self.sol = []
        self.image = LienSpritesheet("textures/herbe.png",(32,32)).decoupe()
        self.grille_fond = [["vide" for _ in range(self.taille_grille[1])] for _ in range(self.taille_grille[0])]
        self.grille_comp = [["vide" for _ in range(self.taille_grille[1])] for _ in range(self.taille_grille[0])]

    def get_fond(self)->pygame.Surface:
        """Retourne le fond du biome"""
        return self.fond

    def get_comp(self)->list:
        """Retourne les composants du biome"""
        return self.composants

    def genere_grille(self):
        """Génère la grille du biome"""
        
        pos_terre_bleu = []
        #ajout de la terre_bleu
        for _ in range(random.randint(1, 6)):
            x = random.randint(0, self.taille_grille[0]-1)
            y = random.randint(0, self.taille_grille[1]-1)
            self.grille_fond[x][y] = "terre_bleu"
            pos_terre_bleu.append((x, y))
       
        
        
        # propagation de l'terre_bleu
        for _ in range(random.randint(2,10)):
            for pos in pos_terre_bleu:
                if random.random() < 0.5:
                    y = random.randint(-1, 1)
                    x = random.randint(-1, 1)
                    if 0 <= pos[0]+x < self.taille_grille[0] and 0 <= pos[1]+y < self.taille_grille[1] and (x!=0 or y!=0):
                        self.grille_fond[pos[0]+x][pos[1]+y] = "terre_bleu"
                        pos_terre_bleu.append((pos[0]+x, pos[1]+y))
                    
        
      
        # self.grille_fond[4][5] = "terre_bleu"
        # self.grille_fond[5][4] = "terre_bleu"
        # self.grille_fond[6][5] = "terre_bleu"

        #place l'herbe_cyan la ou il n'y a pas de la terre_bleu
        for x in range(self.taille_grille[0]):
            for y in range(self.taille_grille[1]):
                if self.grille_fond[x][y] == "vide":
                    self.grille_fond[x][y] = "herbe_cyan"

        # ajout de la terre_bleu s'il y a 4 autre terre_bleu qui la touche 

        for x in range(self.taille_grille[0]):
            for y in range(self.taille_grille[1]):
                if "herbe_cyan"==self.grille_fond[x][y]:
                    autours = self.get_autour((x,y))
                    if (sum(("terre_bleu"==autours[1], "terre_bleu"==autours[3], "terre_bleu"==autours[4],"terre_bleu"==autours[6]))==4):
                        self.grille_fond[x][y] = "terre_bleu"

        
    def genere_comp(self):
        """Génère les composants du biome"""
        for x in range(self.taille_grille[0]):
            for y in range(self.taille_grille[1]):
                if self.grille_fond[x][y] == "terre_bleu":
                    self.sol.append(self.genère_herbe((x,y),self.echelle))
                if self.grille_fond[x][y] == "herbe_cyan":
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
        debug = False
        if debug:
            if self.grille_fond[pos[0]][pos[1]] == "terre_bleu":
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[7])
            if self.grille_fond[pos[0]][pos[1]] == "herbe_cyan":
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[10])
        if self.grille_fond[pos[0]][pos[1]] == "terre_bleu":
            if "herbe_cyan"== autour[1] or "herbe_cyan"== autour[3] or "herbe_cyan"== autour[4] or "herbe_cyan"== autour[6]:
                image=self.image[random.choice([22,23])]
                rand=random.choice([0, 90, 180, 270])
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,pygame.transform.rotate(image.texture,rand))
            
            if "herbe_cyan"== autour[0] or "herbe_cyan"== autour[2] or "herbe_cyan"== autour[5] or "herbe_cyan"== autour[7]:
                image=self.image[random.choice([7,23])] 
                rand=random.choice([0, 90, 180, 270])
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,pygame.transform.rotate(image.texture,rand))
            
            return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[7])
        
        elif self.grille_fond[pos[0]][pos[1]] == "herbe_cyan":

            #triple coin
            if "terre_bleu"==autour[1] and "terre_bleu"==autour[3] and "terre_bleu"==autour[4]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[29])
            if "terre_bleu"==autour[1] and "terre_bleu"==autour[3] and "terre_bleu"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[25])
            if "terre_bleu"==autour[1] and "terre_bleu"==autour[4] and "terre_bleu"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[33])
            if "terre_bleu"==autour[3] and "terre_bleu"==autour[4] and "terre_bleu"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[31])

            #coin inverse
            if "terre_bleu"==autour[1] and "terre_bleu"==autour[3]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[3])
            if "terre_bleu"==autour[1] and "terre_bleu"==autour[4]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[15])
            if "terre_bleu"==autour[4] and "terre_bleu"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[17])
            if "terre_bleu"==autour[3] and "terre_bleu"==autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[5])
            #coté
            if "terre_bleu"== autour[1]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([8,9])])
            if "terre_bleu"== autour[3]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([13,4])])
            if "terre_bleu"== autour[4]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([1,16])])
            if "terre_bleu"== autour[6]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[random.choice([6,11])])
            
            #double coin
            if "terre_bleu"==autour[0] and "terre_bleu"==autour[7]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[19])
            if "terre_bleu"==autour[2] and "terre_bleu"==autour[5]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[18])

            #Coin 
            if "terre_bleu"==autour[0]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[14])
            if "terre_bleu"==autour[2]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[2])
            if "terre_bleu"==autour[5]:
                return Sol((pos[0]*self.echelle[0],pos[1]*self.echelle[1]),taille,self.image[12])
            if "terre_bleu"==autour[7]:
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
        




