import random
import pygame
from interface.graphique import screen
from game.map.biome.teste_biome import TesteBiome
def main():
    biome = TesteBiome(random.randint(0, 1000000))
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