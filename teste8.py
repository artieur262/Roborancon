import pygame
from autre import save
from game.entity.playeur import Playeur

def main():
    playeur=Playeur.genere_self(save.load_json("teste/playeur.json"))

    for i,image in enumerate(playeur.texture):
        pygame.image.save(image.texture, f"textures/teste/playeur/img{i}.png")
    print("fini")
if __name__ == "__main__": 
    main()
      
