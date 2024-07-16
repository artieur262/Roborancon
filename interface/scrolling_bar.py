"""Module qui gère les barres de défilement"""

from pygame import Surface
from interface.graphique import ObjetGraphique, Image, screen


class ScrollBar(ObjetGraphique):
    """Classe qui gère les barres de défilement

    agrs:
        - coordonnee : tuple[int, int] : coordonnée de la barre de défilement
        - taille : tuple[int, int] : taille de la barre de défilement
        - texture : Image | Surface | str : texture de la barre de défilement
        - texture_scroll : Image | Surface | str : texture de la barre de défilement
        - taille_scroll : int : taille de la barre de défilement
        - sens : str : sens de la barre de défilement (vertical ou horizontal)
        - marge : int : marge de la barre de défile (default 3)
    """

    def __init__(
        self,
        coordonnee: tuple[int, int],
        taille: tuple[int, int],
        texture: Image | Surface | str,
        texture_scroll: Image | Surface | str,
        taille_scroll: int,
        sens: str,
        marge: int = 3,
    ):
        super().__init__(coordonnee, [texture], taille)
        self.__taille = taille
        self.redimentione_all_image(taille)

        self.__taille_scroll = taille_scroll
        self.position_scroll = 0
        self.__sens = sens
        self.__marge = marge

        if sens == "vertical":
            if not isinstance(texture_scroll, Image):
                texture_scroll = Image(texture_scroll)
            self.__scroll = texture_scroll
            self.__scroll.redimentione((taille[0] - 2 * marge, taille_scroll))
        elif sens == "horizontal":
            if not isinstance(texture_scroll, Image):
                texture_scroll = Image(texture_scroll)
            self.__scroll = texture_scroll
            self.__scroll.redimentione((taille_scroll, taille[1] - 2 * marge))

    def afficher(
        self, decalage: tuple[int, int] = None, surface: Surface = None
    ) -> bool:
        if decalage is None:
            decalage = (0, 0)
        if surface is None:
            surface = screen
        super().afficher(decalage, surface)
        if self.__sens == "vertical":
            self.__scroll.afficher(
                (
                    self.coordonnee[0] - decalage[0] + self.__marge,
                    self.coordonnee[1] + self.position_scroll - decalage[1],
                ),
                surface,
            )
        elif self.__sens == "horizontal":
            self.__scroll.afficher(
                (
                    self.coordonnee[0] + self.position_scroll - decalage[0],
                    self.coordonnee[1] - decalage[1] + self.__marge,
                ),
                surface,
            )

    def corrige_scroll(self):
        """corrige la position de la barre de défilement si elle est en dehors des limites"""
        if self.__sens == "vertical":
            if self.position_scroll < self.__marge:
                self.position_scroll = self.__marge
            elif (
                self.position_scroll
                > self.__taille[1] - self.__taille_scroll - self.__marge
            ):
                self.position_scroll = (
                    self.__taille[1] - self.__taille_scroll - self.__marge
                )

        elif self.__sens == "horizontal":
            if self.position_scroll < self.__marge:
                self.position_scroll = self.__marge
            elif (
                self.position_scroll
                > self.__taille[0] - self.__taille_scroll - self.__marge
            ):
                self.position_scroll = (
                    self.__taille[0] - self.__taille_scroll - self.__marge
                )

    def souris_scroll(self, pos_souris: tuple[int, int]):
        """déplace la barre de défilement en fonction de la position de la souris"""
        if self.point_dans_objet(pos_souris):
            if self.__sens == "vertical":
                self.position_scroll = (
                    pos_souris[1] - self.coordonnee[1] - self.__taille_scroll / 2
                )
                self.corrige_scroll()

            elif self.__sens == "horizontal":
                self.position_scroll = (
                    pos_souris[0] - self.coordonnee[0] - self.__taille_scroll / 2
                )
                self.corrige_scroll()

    def set_scroll(self, pos: int):
        """change la position de la barre de défilement"""
        self.position_scroll = pos
        self.corrige_scroll()

    def ajout_scroll(self, ajout: int):
        """ajoute un déplacement à la barre de défilement"""
        self.position_scroll += ajout
        self.corrige_scroll()

    def get_pourcentage(self):
        """retourne la position de la barre de défilement en pourcentage"""
        if self.__sens == "vertical":
            return (self.position_scroll - self.__marge) / (
                self.__taille[1] - self.__taille_scroll - 2 * self.__marge
            )
        elif self.__sens == "horizontal":
            return (self.position_scroll - self.__marge) / (
                self.__taille[0] - self.__taille_scroll - 2 * self.__marge
            )

    def set_taille_scroll(self, taille_scroll: int):
        """change la taille de la barre de défilement"""
        self.__taille_scroll = taille_scroll
        if self.__sens == "vertical":
            self.__scroll.redimentione(
                (self.__taille[0] - 2 * self.__marge, taille_scroll)
            )
        elif self.__sens == "horizontal":
            self.__scroll.redimentione(
                (taille_scroll, self.__taille[1] - 2 * self.__marge)
            )
