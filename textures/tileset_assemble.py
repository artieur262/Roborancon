import json
import pygame

class AssembleurTileSet:
    def __init__(self,img:list[pygame.Surface],matrice_pos:list[tuple[int,int]]=None, taille:tuple[int,int]=None, decalage:list[tuple[int,int]]=None):
        if matrice_pos is None:
            matrice_pos = [(i,0) for i in range(len(img))]
        if decalage is None:
            decalage = [(0,0) for _ in img]
        if taille is None:
            taille = (img[0].get_size()+decalage[0], img[1].get_size()+decalage[1])
        self.constructeur(img,matrice_pos,taille,decalage)
            
    def constructeur(self,img:list[pygame.Surface],matrice_pos:list[tuple[int,int]],taille:tuple[int,int],decalage:list[tuple[int,int]]):
        taille_fond=(max([pos[0] for pos in matrice_pos])+1)*taille[0], (max([pos[1] for pos in matrice_pos])+1)*taille[1]
        self.fond = pygame.Surface(taille_fond, pygame.SRCALPHA)
        self.fond.fill((0,0,0,0))
        for i in range(len(img)):
            self.fond.blit(img[i], (matrice_pos[i][0]*taille[0]+decalage[i][0], matrice_pos[i][1]*taille[1]+decalage[i][0]))
      
    


    def get_fond(self):
        return self.fond

def image_loader(liste: list[str])->list[pygame.Surface]:
    liste:list[pygame.Surface]= [pygame.image.load(i) for i in liste]
    # for img in liste:
    #     img.convert_alpha()
    return liste

def save_json(lien: str, contenu):
    """crée un json

    Args:
        lien (str): est parcour de ficher est le nom.extention du ficher
        contenu (_type_): est le contenu du fiche
    """
    with open(lien, "w", encoding="utf8") as file:
        json.dump(contenu, file, indent=1)
        # file.close()

def assemble_data(data_add:dict, grille_pos:list[tuple[int,int]],taille:tuple[int,int],ancre:list[tuple[int,int]]):
    if taille is not None:
        data_add["taille"]=taille
    if grille_pos is not None:
        data_add["grille_pos"]=[i for i in grille_pos]
    else:
        data_add["grille_pos"]=[(i,0) for i in range(len(ancre))]
    if ancre is not None:
        data_add["ancre"]=[i for i in ancre]
    return data_add
def main():
    taille=None
    decalage=None
    grille_pos=None
    data_add={}
    ancre=None
    data_taille=True 
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    nom="textures/teste/test_playeur/imgset"
    img=[
        "textures/teste/test_playeur/img0.png",
        "textures/teste/test_playeur/img01.png",
        "textures/teste/test_playeur/img02.png",
        "textures/teste/test_playeur/img06.png",
        "textures/teste/test_playeur/img07.png",
        "textures/teste/test_playeur/img08.png",
        "textures/teste/test_playeur/img03.png",
        "textures/teste/test_playeur/img04.png",
        "textures/teste/test_playeur/img05.png",
        "textures/teste/test_playeur/img09.png",
        "textures/teste/test_playeur/img10.png",
        "textures/teste/test_playeur/img11.png",
    ]
    taille=(64,64)
    
    grille_pos=[
        (0,0),(1,0),(2,0),
        (0,1),(1,1),(2,1),
        (0,2),(1,2),(2,2),
        (0,3),(1,3),(2,3),
    ]
    ancre=[
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37],
    [21,37]
]
    img=image_loader(img)
    data_add=assemble_data(data_add,grille_pos,taille if data_taille else None ,ancre)
    assembleur=AssembleurTileSet(img,grille_pos,taille,decalage,)
    tile_set=assembleur.get_fond()
    # tile_set.convert_alpha()
    pygame.display.init()
    pygame.image.save(tile_set, nom + ".png")
    if len(data_add)>1:
        save_json(nom+".json",data_add)

    pygame.quit()

if __name__ == "__main__":
    main()
    