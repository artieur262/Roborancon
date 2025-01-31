
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
    nom="textures/map/decor/arbres_bleu"
    taille=(32,32)
    temp=LienSpritesheet("textures/autre",None).decoupe()
    img_graf+=[temp[44],temp[45],temp[48],temp[49]]

    grille_pos=[(0,0),(1,0),(0,1),(1,1)]
    
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


