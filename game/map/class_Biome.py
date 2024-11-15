import random 
import pygame
from game.map.composant import Composant,Sol
class Biome:
    def __init__(self,seed):
        random.seed(seed)
        taille=(10,10)
        self.fond= pygame.Surface(taille,pygame.SRCALPHA)
        self.fond.fill((0,0,0,0))
        self.composants=[]
        self.sol:list[Sol]=[]

    def genere_comp(self):
        pass
    def ajout_sol_fond(self):
       """Ajoute le sol au fond"""
       for sol in self.sol:
            sol.afficher(surface=self.fond)
