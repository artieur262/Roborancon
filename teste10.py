import os
import random
import pygame
from interface.graphique import screen
from game.map.biome.teste_biome import TesteBiome

def save_image(surface:pygame.Surface, path:str):
    """Sauvegarde une surface dans un fichier"""
    if not os.path.exists(path+".png"):
        pygame.image.save(surface, path+".png")
        return
    i=0
    while (os.path.exists(path+" "+str(i)+".png")):
        i+=1
    pygame.image.save(surface, path+" "+str(i)+".png")
    return

def main():
    seed=random.randint(0,100000)
    # seed=95282
    # seed=83035
    # seed=52715 #bug rare
    print("seed: " +str(seed))
    biome = TesteBiome(seed)
    biome.genere_grille()
    biome.genere_comp()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    save_image(biome.get_fond(), "screenshots/testbiome")
                    print("image sauvegardée")
                if event.key == pygame.K_r:
                    seed=random.randint(0,100000)
                    print("seed: " +str(seed))
                    biome = TesteBiome(seed)
                    biome.genere_grille()
                    biome.genere_comp()
        pygame.display.flip()
        screen.blit(biome.get_fond(), (0, 0))

if __name__ == "__main__":
    main()