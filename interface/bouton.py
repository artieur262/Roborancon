"""Module qui gère les boutons de l'interface graphique

Classes:
    - Bouton
    - BoutonText
"""

import pygame  # for typing

from interface.graphique import ObjetGraphique, place_texte_in_texture


class Bouton(ObjetGraphique):
    """Classe qui gère les boutons"""

    def __init__(
        self,
        coordonnee: tuple[int, int],
        texture: tuple,
        taille: tuple[int, int],
        data=None,
    ):
        super().__init__(coordonnee, texture, taille)
        self.data = data
        self.redimentione_all_image(taille)
        self.actif = False

    def change_activation(self):
        """change l'activation du bouton"""
        self.actif = not self.actif

    def active(self):
        """active le bouton"""
        self.actif = True

    def desactive(self):
        """desactive le bouton"""
        self.actif = False

    def get_actif(self):
        """retourne si le bouton est actif"""
        return self.actif

    def get_data(self):
        """retourne les data du bouton"""
        return self.data


class BoutonText(Bouton):
    """Classe qui gère les boutons"""

    def __init__(
        self,
        coordonnee: tuple[int, int],
        texture,
        taille: tuple[int, int],
        text: str,
        couleur_text: tuple | int,
        police: pygame.font.Font,
        mode: str = None,
        data=None,
    ):
        super().__init__(coordonnee, texture, taille, data)
        self.text = text
        self.image_original = [image.texture for image in self.texture]
        for image in self.texture:
            place_texte_in_texture(image.texture, text, police, couleur_text, mode)

    def get_text(self):
        """retourne le texte du bouton"""
        return self.text

    def set_text(self, text, police, couleur_text, mode="centrage"):
        """change le texte du bouton"""
        self.text = text
        for image, image_original in zip(self.texture, self.image_original):
            image.texture = image_original.copy()
            place_texte_in_texture(image.texture, text, police, couleur_text, mode)
