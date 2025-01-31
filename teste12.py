
from interface.graphique import LienSpritesheet,Image
from textures.tileset_assemble import * 

def img_vers_surface(liste:list[Image]) -> list[pygame.Surface]:
    return [img.texture for img in liste]


def main():
    taille=None
    decalage=None
    grille_pos=None
    data_add={}
    surface=[]
    surface_str=[]
    img_graf=[]
    ancre=None
    data_taille=True 
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    nom="textures/entity/passif/lezardus"
    taille=(32,32)
    img_graf+=LienSpritesheet("textures/entity/passif/lezardus",None).decoupe()
    img_graf+=LienSpritesheet("textures/entity/passif/lezardus g",None).decoupe()
    img_graf+=LienSpritesheet("textures/entity/passif/lezardus h",None).decoupe()
    img_graf+=LienSpritesheet("textures/entity/passif/lezardus d",None).decoupe()

    grille_pos=[(0,0),(1,0),(2,0),(3,0),
                (0,1),(1,1),(2,1),(3,1),
                (0,2),(1,2),(2,2),(3,2),
                (0,3),(1,3),(2,3),(3,3)
                ]
    
    surface+=img_vers_surface(img_graf)
    surface+=image_loader(surface_str)
    data_add=assemble_data(data_add,grille_pos,taille if data_taille else None ,ancre)
    assembleur=AssembleurTileSet(surface,grille_pos,taille,decalage,)
    tile_set=assembleur.get_fond()
    # tile_set.convert_alpha()
    pygame.display.init()
    pygame.image.save(tile_set, nom + ".png")
    save_json(nom+".json",data_add)

    pygame.quit()

if __name__ == "__main__":
    main()


