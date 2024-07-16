"""cette parti est la pour gérer l'interface graphique du jeu

il y a 2 class:
    - Image : class pour gérer les images
    - ObjetGraphique : class pour gérer les objet graphique

il y a 6 fonctions:
    - gener_texture : permet de générer une texture rectangulaire
    - gener_texture_arc_ciel : permet de générer une texture arc en ciel
    - decoupe_texte : permet de découper un texte en plusieur ligne
    - place_texte_in_texture : permet de mettre du texte sur une image
    - vider_affichage : permet de vider l'affichage
    - quitter : permet de quitter
    
et 1 variable:
    - screen : est la fenêtre du jeu
"""

# pylint: disable=no-member

import pygame


class Image:
    """class pour gérer les images
    avec des fonctions pour les afficher et les redimentionner

    agrs:
        texture (str or pygame.Surface) : est l'image
        ancre (tuple[int, int]) : est l'ancre de l'image
    """

    def __init__(self, texture: str | pygame.Surface, ancre: tuple[int, int] = None):
        if ancre is None:
            ancre = (0, 0)
        if isinstance(texture, str):
            texture = pygame.image.load(texture)
            texture.convert()
        self.ancre: tuple[int, int] = ancre
        self.texture: pygame.surface = texture
        self.__dimention: tuple[int, int] = self.texture.get_size()

    def get_texture(self) -> pygame.surface:
        """retourne la texture de l'objet"""
        return self.texture

    def get_dimention(self):
        """retourne la dimention de l'objet"""
        return self.__dimention

    def get_ancre(self):
        """retourne l'ancre de l'objet"""
        return self.ancre

    def redimentione(self, taille: tuple[int, int]):
        """redimentionne l'image"""
        self.texture = pygame.transform.scale(self.texture, taille)
        self.__dimention = self.texture.get_size()

    def if_in_zone(self, pos_self: tuple, pos_zone: tuple, size_zone: tuple) -> bool:
        """permet de savoir si l'objet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)

        Returns:
            bool: si l'objet
        """
        size_self = self.get_dimention()
        coin_1_self = [pos_self[0] - self.ancre[0], pos_self[1] - self.ancre[1]]
        coin_2_self = [
            pos_self[0] + size_self[0] - self.ancre[0],
            pos_self[1] + size_self[1] - self.ancre[1],
        ]

        coin_1_zone = pos_zone
        coin_2_zone = [pos_zone[0] + size_zone[0], pos_zone[1] + size_zone[1]]

        return (
            coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
            or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
        ) and (
            coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
            or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
        )

    def affiche(self, surface: pygame.Surface, position):
        """affiche l'image sur la fenêtre"""
        if self.if_in_zone(position, (0, 0), surface.get_size):
            emplacement = (position[0] - self.ancre[0], position[1] - self.ancre[1])
            surface.blit(self.texture, emplacement)


class ObjetGraphique:
    """objet graphique qui a le but d'etre affiché

    Args:
        coordonnee (list): est les coordonées de l'objet
        texture (list[str, Image, pygame.Surface]): est la texture de l'objet
        taille (list): est la taille de l'objet
        animation (int, optional): est l'animation de l'objet. Defaults to 0.
    """

    def __init__(
        self,
        coordonnee: list,
        texture: list[str, Image, pygame.Surface],
        taille,
        animation=0,
    ):
        self.texture: list[Image] = []
        for i in texture:
            if isinstance(i, str):
                i = Image(i)
            if isinstance(i, pygame.Surface):
                i = Image(i)
            self.texture.append(i)
        self.coordonnee = coordonnee
        self.taille = taille
        self.animation = animation

    def get_coordonnee(self) -> tuple[int, int] | int:
        """renvoi les coordonées de l'objet
        Args:
            axe (int, optional): {0= axe x, 1= axe y}. Defaults to None."""

        return self.coordonnee

    def set_coordonnee(self, valu):
        """defini les coordonées de l'objet"""
        self.coordonnee = valu

    def get_taille(self) -> tuple[int, int] | int:
        """renvoi la taille de l'objet"""
        return self.taille

    def get_center(self) -> tuple[float, float]:
        """renvoi le centre de l'objet"""
        return (
            self.coordonnee[0] + self.taille[0] / 2,
            self.coordonnee[1] + self.taille[1] / 2,
        )

    def image_actuel(self) -> pygame.Surface:
        """donne l'image actuel"""
        return self.texture[self.animation]

    def redimentione_all_image(self, taille: tuple[int]):
        """redimentionne toute les images"""
        for image in self.texture:
            image.redimentione(taille)

    def point_dans_objet(self, point):
        """pour savoir si un point est dans l'objet

        entre :
            x (int) : est les coordonees du point sur l'axe x
            y (int) : est les coordonees du point sur l'axe y

        retun (bool) : si le point est dans l'objet

        """
        return (
            self.coordonnee[0] <= point[0] < self.coordonnee[0] + self.taille[0]
        ) and (self.coordonnee[1] <= point[1] < self.coordonnee[1] + self.taille[1])

    def collision_in_axe(self, obj_pos: int, obj_size: int, axe: int) -> bool:
        """pemet de voir si un objet a une colisiont sur un plan

        Args:
            obj_pos (int): est la position de l'objet sur l'axe
            obj_size (int): est la taille de l'objet sur l'axe
            axe (int): {1= axe x, 2= axe y}

        Returns: (bool)
        """
        coin_1_self = self.get_coordonnee()[axe]
        coin_2_self = self.get_coordonnee()[axe] + self.get_taille()[axe]

        coin_1_obj = obj_pos
        coin_2_obj = obj_pos + obj_size

        return (
            coin_1_obj <= coin_1_self < coin_2_obj
            or coin_1_self <= coin_1_obj < coin_2_self
        )

    def collision(self, obj_pos: tuple[int], obj_size: tuple[int]) -> bool:
        """pemet savoir l'objet à une colision avec un autre objet dans l'espace
        args:
            obj_pos (tuple[int]) : est la position de l'objet
            obj_size (tuple[int]) : est la taille de l'objet
        """
        return self.collision_in_axe(
            obj_pos[0], obj_size[0], 0
        ) and self.collision_in_axe(obj_pos[1], obj_size[1], 1)

    def objet_dans_zone(self, pos_zone: tuple, size_zone: tuple) -> bool:
        """permet de savoir si un bojet est dans une zone

        Args:
            axe_x (tuple): à une longuer de 2 (le premier est le plus petit)
            axe_y (tuple): à une longuer de 2 (le premier est le plus petit)

        Returns:
            bool: si l'objet
        """
        coin_1_self = self.coordonnee
        coin_2_self = [self.coordonnee[i] + self.taille[i] for i in range(2)]

        coin_1_zone = pos_zone
        coin_2_zone = [pos_zone[0] + size_zone[0], pos_zone[1] + size_zone[1]]

        return (
            coin_1_zone[0] <= coin_1_self[0] < coin_2_zone[0]
            or coin_1_self[0] <= coin_1_zone[0] < coin_2_self[0]
        ) and (
            coin_1_zone[1] <= coin_1_self[1] < coin_2_zone[1]
            or coin_1_self[1] <= coin_1_zone[1] < coin_2_self[1]
        )

    def afficher(
        self,
        decalage: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ) -> bool:
        """permet de l'affiché sur la sur une surface et de savoir si il est affiché

        Args:
            decalage (tuple[int, int], optional): est le decalage de l'objet. Defaults to None.
            surface (pygame.Surface, optional): est la surface sur laquel afficher. Defaults None.

        if la surface est None alors c'est directement sur l'écran
        """
        if surface is None:
            surface = screen
        if decalage is None:
            decalage = (0, 0)
        if self.objet_dans_zone(decalage, surface.get_size()):
            self.texture[self.animation].affiche(
                surface,
                (self.coordonnee[0] - decalage[0], self.coordonnee[1] - decalage[1]),
            )
            return True
        return False


def gener_texture(taille: tuple[int, int], color: tuple) -> pygame.Surface:
    """génere une texture rectangulaire

    Args:
        taile (tuple[int]): (x,y) est la taille de la texture
        color (tuple[int]): (Red,Green,Blue,trasparence "optionel") est la couleur de l'image

    Returns:
        Surface: est l'image généré
    """

    if len(color) == 3:  # permet de pas forcer de metre des couleurs
        # print(taille)
        image = pygame.Surface(taille)
        image.fill(color)
    elif len(color) == 4:
        image = pygame.Surface(taille, pygame.SRCALPHA)
        image.fill(color)
    return image


def gener_texture_arc_ciel(taille: list[int], decalage: int = 0):
    """génere une texture arc en ciel
    créer à cause de lgwythyr
    je n'avais pas le choix

    agrs:
        taille (list[int]) : est la taille de l'image
        decalage (int) : est le décalage de l'arc en ciel
    """
    couleur = [
        (255, 0, 0),
        (255, 125, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (125, 0, 255),
    ]
    min_taille = 0
    if taille[0] < taille[1]:
        min_taille = taille[0]
    else:
        min_taille = taille[1]
        texture = gener_texture(taille, couleur[0 + decalage])
    for i in range(1, min_taille // 10):
        texture.blit(
            gener_texture(
                [taille[0] - 10 * i, taille[1] - i * 10],
                couleur[(i + decalage) % len(couleur)],
            ),
            (i * 5, i * 5),
        )
    return texture


def decoupe_texte(
    texte: str, longueur_ligne: int, police: pygame.font.Font
) -> list[str]:
    """decoupe un texte en plusieur ligne
    en sorte que chaque ligne ne dépasse pas la longueur donnée

    Args:
        texte (str): est le texte à découper
        taille (int): est la taille de la ligne
        police (pygame.font.Font): est la police du texte

    Returns:
        list[str]: est le texte découpé
    """
    texte = texte.split("\n")
    texte_decoupe = []
    for fragment in texte:
        fragment = fragment.split(" ")
        ligne = ""
        for i in fragment:
            if police.size(ligne + i)[0] < longueur_ligne:
                ligne += i + " "
            elif len(ligne) > 0:
                texte_decoupe.append(ligne[:-1])
                ligne = i + " "
            else:
                texte_decoupe.append(i)
        if len(ligne) > 0:
            texte_decoupe.append(ligne[:-1])

    return texte_decoupe


def place_texte_in_texture(
    image: pygame.Surface,
    texte: str,
    police: pygame.font.Font,
    color: tuple[int],
    mode: str = "centrage",
) -> pygame.Surface:
    """ajoute du texte sur une image
    la fonction gère les saut de ligne quand le texte est trop long ou qu'il y a des "\\n"

    Args:
        image (pygame.Surface): est l'image qui recevera le texte
        texte (str): est le texte rajouter
        police (pygame.font.Font): est la police du texte
        color (tuple[int]): est la couleur du texte
        mode (str, optional): est le mode de placement du texte. Defaults to "centrage".
                              ("centrage", "haut_gauche")
    Returns:
        image (pygame.Surface): est image avec son texte
    """
    dimention_image = image.get_size()
    texte_decoupe = decoupe_texte(texte, dimention_image[0], police)
    if mode == "centrage":
        for i, ligne in enumerate(texte_decoupe):
            dimention_ligne = police.size(ligne)
            image.blit(
                police.render(ligne, 2, color),
                (
                    (dimention_image[0] - dimention_ligne[0]) // 2,
                    (dimention_image[1] - dimention_ligne[1] * len(texte_decoupe)) // 2
                    + i * dimention_ligne[1],
                ),
            )
    elif mode == "haut_gauche":
        for i, ligne in enumerate(texte_decoupe):
            dimention_ligne = police.size(ligne)
            image.blit(
                police.render(ligne, 2, color),
                (0, i * dimention_ligne[1]),
            )
    elif mode == "centrage_haut":
        for i, ligne in enumerate(texte_decoupe):
            dimention_ligne = police.size(ligne)
            image.blit(
                police.render(ligne, 2, color),
                (
                    (dimention_image[0] - dimention_ligne[0]) // 2,
                    i * dimention_ligne[1],
                ),
            )
    return image


def vider_affichage(couleur_du_fond: tuple | int = 0):
    """permet de vider l'affichage
    donc de tout retire et met la couleur qui est entre en fond

    Args:
        couleur_du_fond (tuple or int): bref c'est une couleur RGB (red, green, blue)
    """
    screen.fill(couleur_du_fond)


def quitter():
    """permet de quitter"""
    pygame.quit()
    exit()


pygame.init()
screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
screen.fill((200, 200, 200))

if __name__ == "__main__":
    pygame.display.set_caption("projet")
