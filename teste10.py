import random
import pygame
from interface.graphique import screen
from game.map.biome.teste_biome import TesteBiome
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
        pygame.display.flip()
        screen.blit(biome.get_fond(), (0, 0))

if __name__ == "__main__":
    main()