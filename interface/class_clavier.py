"""ce module contien les class pour la souris et le clavier

il y a 2 class:
    - Clavier : class pour gérer le clavier
    - Souris : class pour gérer la souris

et 2 dictionnaire:
    - key_names : dictionnaire pour les noms des touches
    - mouse_names : dictionnaire pour les noms des cliques de la souris
"""

import pygame


class Clavier:
    """cette class permet de gérer le clavier
    et de savoir si une touche est presser ou lacher
    """

    key_names = {
        "en": {
            8: "backspace",
            9: "tab",
            13: "return",
            27: "escape",
            32: "space",
            127: "delete",
            1073741881: "caps lock",
            1073741903: "right",
            1073741904: "left",
            1073741905: "down",
            1073741906: "up",
            1073742048: "left ctrl",
            1073742049: "left shift",
            1073742050: "left alt",
            1073742051: "left windows",
            1073742052: "right ctrl",
            1073742053: "right shift",
            1073742054: "right alt",
            1073742055: "right windows",
        },
        "fr": {
            8: "retour arrière",
            9: "tabulation",
            13: "entrée",
            27: "échap",
            32: "espace",
            127: "suppr",
            1073741881: "verr maj",
            1073741903: "droite",
            1073741904: "gauche",
            1073741905: "bas",
            1073741906: "haut",
            1073742048: "ctrl gauche",
            1073742049: "shift gauche",
            1073742050: "alt gauche",
            1073742051: "windows gauche",
            1073742052: "ctrl droit",
            1073742053: "shift droit",
            1073742054: "alt droit",
            1073742055: "windows droit",
        },
    }

    def __init__(self) -> None:
        self.dict_touches = {}

    def actualise_all_touche(self):
        """actualise toute les touches"""
        clee_a_supprimer = []
        for clee, touche in self.dict_touches.items():
            if touche == "vien_presser":
                self.dict_touches[clee] = "presser"
            elif touche in ("vien_lacher", "lacher"):
                clee_a_supprimer.append(clee)
        for clee in clee_a_supprimer:
            del self.dict_touches[clee]

    def get_pression(self, clee: int):
        """get la pression d'une touche"""
        if clee in self.dict_touches:
            return self.dict_touches[clee]
        else:
            return "lacher"

    def set_pression(self, clee: str, value: str):
        """change la pression d'une touche"""
        self.dict_touches[clee] = value

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_touches.items():
            res += f"{clee}:{value},"
        res += "}-"
        return res


class Souris:
    """cette class permet de gérer la souris
    peremet de savoir la position de la souris
    et permet de savoir si un clique est vien_presser, presser, vien_lacher ou lacher
    """

    click_names = {
        "en": {1: "left click", 2: "wheel click", 3: "right click"},
        "fr": {1: "clique gauche", 2: "clique molette", 3: "clique droit"},
    }

    def __init__(self):
        self.actualise_position()
        self.dict_clique = {}

    def actualise_all_clique(self):
        """actualise toute les touches"""
        clee_a_supprimer = []
        for clee, touche in self.dict_clique.items():
            if touche == "vien_presser":
                self.dict_clique[clee] = "presser"
            elif touche in ("vien_lacher", "lacher"):
                clee_a_supprimer.append(clee)
        for clee in clee_a_supprimer:
            del self.dict_clique[clee]

    def get_pression(self, clee: int):
        """get la pression d'une touche
        retrun : Literal["vien_presser", "presser", "vien_lacher", "lacher"]
        """
        if clee in self.dict_clique:
            return self.dict_clique[clee]
        else:
            return "lacher"

    def set_pression(self, clee: str, value: str):
        """change la pression d'une touche"""
        self.dict_clique[clee] = value

    def get_pos(self):
        """get la position de la souris"""
        return self.pos

    def actualise_position(self):
        """actualise la position de la souris"""
        self.pos = pygame.mouse.get_pos()

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_clique.items():
            res += f"{clee}:{value},"
        res += "}-"
        return res


# if __name__ == "__main__":
#     pygame.init()
#     print(pygame.key.get_pressed())
#     print(pygame.key.get_repeat())
#     print(pygame.key.get_mods())
#     print(pygame.key.name(121))
#     print(pygame.key.key_code("y"))
