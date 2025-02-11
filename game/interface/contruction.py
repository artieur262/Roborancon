import pygame

from interface.graphique import ObjetGraphique, Image,LienSpritesheet,place_texte_in_texture,genere_texture
from interface.class_clavier import Clavier
from game.map.composant import Composant, Mur, Porte,Sol


class FuturComp(ObjetGraphique):
    """
    varainte: tuple[str,tuple[int,int],tuple[int,int],(list[str|Image]|str),(list|None)]
              (class, decalage, taille, lien_textures, data_sup)
    
    """
    def __init__(self, coordonnee, texture, taille, variante:tuple[str,tuple[int,int],tuple[int,int],(list[str|Image]|str),(list|None)],apercu:Image|str):
        super().__init__(coordonnee, texture, taille)
        self.lien_textures = []
        self.variante = variante 
        decalage = self.variante[1]
        for img in self.texture:
            img.set_ancre((decalage[1][0]+img.get_ancre()[0],decalage[1][1]+img.get_ancre()[1]))  
        self.charger_apercu(apercu)
  
    def charger_apercu(self,apercu:Image|str):
        if isinstance(apercu,str):
            self.apercu = Image(apercu)
        elif isinstance(apercu,Image):
            self.apercu = apercu
    
    def actuel_comp(self)->Composant:
        """retourne le composant actuel"""
        return self.fabrique_comp(self.variante)
    
    def fabrique_comp(self,info)->Composant:
        """fabrique un composant à partir d'info"""
        if info[0] == "mur":
            return Mur((self.get_pos()[0]+info[1][0],self.get_pos()[1]+info[1][1]),info[2], info[3])
        elif info[0] == "porte":
            return Porte((self.get_pos()[0]+info[1][0],self.get_pos()[1]+info[1][1]),info[2], info[3])
        elif info[0] =="sol":
            return Sol((self.get_pos()[0]+info[1][0],self.get_pos()[1]+info[1][1]),info[2],info[3])
        elif info[0] == "composant":
            return Composant((self.get_pos()[0]+info[1][0],self.get_pos()[1]+info[1][1]),info[2], info[3])
    
    def get_apercu(self)->Image:
        return self.apercu
    
    def get_next_apercu(self,sens=1)->Image:
        return self.apercu

    def actalise_animation(self):
        """actualise l'animation"""
        self.animation = 0

    def next_variante(self,sens=1):
        """passe à la variante suivante"""
        pass
    
    def plusieur_variante(self):
        """retourne si il y a plusieurs variante"""
        return False

class ListFuturComp(FuturComp):
    """
    varainte: list[tuple[str,tuple[int,int],tuple[int,int],(list[str|Image]|str),(list|None)]]
              list[(class, decalage, taille, lien_textures, data_sup)]
    
    """
    def __init__(self, coordonnee, texture, taille, variante:list[tuple[str,tuple[int,int],tuple[int,int],(list[str|Image]|str),(list|None)]],apercu:list[str|Image]|str,variante_actuel=0,):
        super().__init__(coordonnee, texture, taille, variante[variante_actuel])
        self.variante_actuel = variante_actuel
        self.list_variante = variante
        #peut être optimisé 
        #car on fait une fois une boucle pour rien dans super().__init__
        for i,img in enumerate(self.texture):
            decalage = self.list_variante[i][1]
            img.set_ancre((decalage[0]+img.get_ancre()[0],decalage[1]+img.get_ancre()[1]))
        self.apercu:list[Image] = Image.genere_list_Image(apercu)
    
    def charger_apercu(self, apercu:list[str|Image]|str):
        self.apercu = Image.genere_list_Image(apercu)

    def set_variante(self,variante:int):
        self.variante_actuel = variante
        self.variante = self.list_variante[variante]
        self.actualise_animation()

    def actuel_comp(self)->Composant:
        return self.fabrique_comp(self.list_variante[self.variante_actuel])

    def next_variante(self,sens=1):
        self.variante_actuel=(self.variante_actuel+sens)%len(self.list_variante)
        self.variante = self.list_variante[self.variante_actuel]
        self.actualise_animation()
    
    def get_apercu(self)->Image:
        return self.apercu[self.variante_actuel]

    def get_next_apercu(self,sens=1)->Image:
        return self.apercu[(self.variante_actuel+sens)%len(self.list_variante)]

    def actualise_animation(self):
        self.animation = self.variante_actuel
    
    def plusieur_variante(self):
        return True

class TileFuturComp(FuturComp):
    """
    varainte: 
        list[tuple[str,tuple[int,int],tuple[int,int],(list|None)]]
        list[(class, decalage, taille, data_sup)]
    """
    def __init__(self, coordonnee, texture, taille, variante:tuple[str,tuple[int,int],tuple[int,int],(list|None)], title:list[str|Image]|str,apercu:list[str|Image]|str,variante_actuel:int =0):
        super().__init__(coordonnee, texture, taille, variante,apercu)
        self.variante_actuel = variante_actuel
        self.title:list[Image] = Image.genere_list_Image(title)
        self.apercu:list[Image] = Image.genere_list_Image(apercu)

    def set_variante(self,variante:int):
        self.variante_actuel = variante
        self.variante = self.list_variante[variante]
        self.actualise_animation()
    
    def charger_apercu(self, apercu:list[str|Image]|str):
        self.apercu = Image.genere_list_Image(apercu)
        
    
    def actuel_comp(self)->Composant:
        variante = self.variante
        info= (variante[0],variante[1],variante[2],self.title[self.variante_actuel],variante[3])
        if info[0] in ("porte","composant"):
            raise ValueError("le type de composant n'est pas compatible avec les tiles")
        return self.fabrique_comp(info)

    def next_variante(self,sens=1):
        print(self.variante_actuel)
        self.variante_actuel=(self.variante_actuel+sens)%len(self.title)
        self.actualise_animation()
    
    def actualise_animation(self):
        self.animation = self.variante_actuel
    
    def plusieur_variante(self):
        return True
    
    def get_apercu(self)->Image:
        return self.apercu[self.variante_actuel]

    def get_next_apercu(self,sens=1)->Image:
        return self.apercu[(self.variante_actuel+sens)%len(self.title)]
    




class MenuConstruction:
    
    TEXTURE_FOND=(125,125,125,125)
    def __init__(self):
        self.comp:list[list[FuturComp]]= [
            [TileFuturComp((0,0),"textures/map/construction/bariere_plan",(32,32),[
                ("mur",(0,0),(18,32),None),
                ("mur",(0,13),(32,19),None),
                ("mur",(14,13),(18,19),None),
                ("mur",(0,13),(18,19),None),
                ("mur",(14,0),(32,32),None),
                ("mur",(0,0),(32,32),None),
                ("mur",(14,0),(4,32),None),
                ("mur",(0,0),(4,19),None),
                ("mur",(0,13),(4,19),None),
                ("mur",(13,12),(6,4),None),
                ("mur",(14,0),(18,4),None),
                ("mur",(0,0),(32,18),None),
                ("mur",(0,0),(18,18),None),
                ("mur",(14,13),(18,4),None),
                ("mur",(0,13),(32,4),None),
                ("mur",(0,13),(18,4),None),
            ],"textures/map/construction/bariere","textures/map/construction/bariere")],
        ]
        self.ordre=["mur", "sol", "fourniture","cloture"]
        self.categorie=0
        self.index=0
        self.fond = Image(genere_texture((200,800),self.TEXTURE_FOND))
        self.assemblage()

    def get_categorie(self):
        return self.ordre[self.categorie]
    
    def next_categorie(self,sens=1):
        self.categorie=(self.categorie+sens)%len(self.comp)
        self.index=0
        self.assemblage()

    def next_index(self,sens=1):
        self.index=(self.index+sens)%len(self.comp[self.categorie])
        if sens!=0:
            self.assemblage()
    
    def get_comp(self)->Composant:
        return self.comp[self.categorie][self.index].actuel_comp()
    
    def next_variante(self,sens=1):
        actuel = self.comp[self.categorie][self.index]
        if actuel.plusieur_variante():
            actuel.next_variante(sens)
        if sens!=0:
            self.assemblage()

    def get_apercu(self):
        return self.comp[self.categorie][self.index].get_apercu()
    
    def get_next_apercu(self,sens=1):
        return self.comp[self.categorie][self.index].get_next_apercu(sens)

    def get_next_block_apercu(self,sens=1):
        return self.comp[self.categorie][(self.index+sens)%len(self.comp[self.categorie])].get_apercu()
    
    def gestion_touche(self,controle:dict,clavier:Clavier)->Composant|None:
        if clavier.get_pression(controle["haut"])=="vien_presser":
            self.next_index(-1)
        elif clavier.get_pression(controle["bas"])=="vien_presser":
            self.next_index(1)
        elif clavier.get_pression(controle["gauche"])=="vien_presser":
            self.next_categorie(-1)
        elif clavier.get_pression(controle["droite"])=="vien_presser":
            self.next_categorie(1)
        elif clavier.get_pression(controle["next_var"])=="vien_presser":
            self.next_variante(1)
        elif clavier.get_pression(controle["prev_var"])=="vien_presser":
            self.next_variante(-1)
        elif clavier.get_pression(controle["interagir"])=="vien_presser":
            return self.get_comp()

    def assemblage(self):
        self.fond.colorier(self.TEXTURE_FOND)
        police=pygame.font.Font(None, 30)
        self.fond.ajoute_image(Image(place_texte_in_texture(
            genere_texture((200,100),(0,0,0,0)),
            self.get_categorie(),
            police,
            (255,255,255,255)
            )),(0,0))
        self.fond.ajoute_image(self.get_next_apercu(),(50,375))
        self.fond.ajoute_image(self.get_next_apercu(-1),(100,375))
        self.fond.ajoute_image(self.get_apercu(),(75,375))
        self.fond.ajoute_image(self.get_next_block_apercu(-2),(75,275))
        self.fond.ajoute_image(self.get_next_block_apercu(-1),(75,300))
        self.fond.ajoute_image(self.get_next_block_apercu(2),(75,475))
        self.fond.ajoute_image(self.get_next_block_apercu(),(75,450))
    
    def afficher(self,position=None,surface=None):
        if position is None:
            position=(0,0)
        self.fond.afficher(position,surface)


        

    
