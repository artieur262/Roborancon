"""cette parti est la pour gérer l'interface graphique du jeu

il y a une class:
    ObjetGraphique : est un objet graphique qui a le but d'etre affiché

il y a des fonctions:
    - gener_texture : génere une texture rectangulaire
    - gener_texture_arc_ciel : génere une texture arc en ciel
    - decoupe_texte : découpe un texte en plusieur ligne
    - place_texte_in_texture : ajoute du texte sur une image
    - vider_affichage : permet de vider l'affichage
    - quitter : permet de quitter


"""

# pylint: disable=no-member
import pygame


class Image:
    def __init__(self, texture: str | pygame.Surface, ancre: tuple[int, int] = None):
        if ancre == None:
            ancre = (0, 0)
        if isinstance(texture, str):
            texture = pygame.image.load(texture)
            texture.convert()
        self.ancre: tuple[int, int] = ancre
        self.__texture: pygame.surface = texture
        self.__dimention: tuple[int, int] = self.__texture.get_size()

    def get_texture(self) -> pygame.surface:
        """retourne la texture de l'objet"""
        return self.__texture

    def get_dimention(self):
        """retourne la dimention de l'objet"""
        return self.__dimention

    def get_ancre(self):
        return self.ancre

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
        if self.if_in_zone(position, (0, 0), surface.get_size):
            emplacement = (position[0] - self.ancre[0], position[1] - self.ancre[1])
            surface.blit(self.__texture, emplacement)


def gener_texture(taille: tuple[int], color: tuple[int] = False) -> pygame.Surface:
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


def vider_affichage(couleur_du_fond: list | int = 0):
    """permet de vider l'affichage
    donc de tout retire et met la couleur qui est entre en fond

    Args:
        couleur_du_fond (list or tuple or int): bref c'est une couleur RGB (red, green, blue)
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
