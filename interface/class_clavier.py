"""ce module contien les class pour la souris et le clavier

il y a 2 class:
    - Clavier : class pour gérer le clavier
    - Souris : class pour gérer la souris
"""

import pygame


class Clavier:
    """cette class permet de gérer le clavier
    et de savoir si une touche est presser ou lacher
    """

    def __init__(self) -> None:
        self.alphabet_clee = {
            "back_space": 8,
            "tab": 9,
            "entrer": 13,
            "echap": 27,
            "space": 32,
            "!": 33,
            "$": 36,
            ")": 41,
            "*": 42,
            ",": 44,
            "0": 48,
            "1": 49,
            "2": 50,
            "3": 51,
            "4": 52,
            "5": 53,
            "6": 54,
            "7": 55,
            "8": 56,
            "9": 57,
            ":": 58,
            ";": 59,
            "<": 60,
            "=": 61,
            "^": 94,
            "a": 97,
            "b": 98,
            "c": 99,
            "d": 100,
            "e": 101,
            "f": 102,
            "g": 103,
            "h": 104,
            "i": 105,
            "j": 106,
            "k": 107,
            "l": 108,
            "m": 109,
            "n": 110,
            "o": 111,
            "p": 112,
            "q": 113,
            "r": 114,
            "s": 115,
            "t": 116,
            "u": 117,
            "v": 118,
            "w": 119,
            "x": 120,
            "y": 121,
            "z": 122,
            "suppr": 127,
            "²": 178,
            "ù": 249,
            "ctrl": 1073742048,
            "left shift": 1073742049,
            "left alt": 1073742050,
            "right shift": 1073742053,
            "alt gr": 1073742054,
            "caps lock": 1073741881,
            "f1": 1073741882,
            "f2": 1073741883,
            "f3": 1073741884,
            "f4": 1073741885,
            "f5": 1073741886,
            "f6": 1073741887,
            "f7": 1073741888,
            "f8": 1073741889,
            "f9": 1073741890,
            "f10": 1073741891,
            "f11": 1073741892,
            "f12": 1073741893,
            "right arrow": 1073741903,
            "left arrow": 1073741904,
            "down arrow": 1073741905,
            "up arrow": 1073741906,
            "end": 1073741901,
            "insert": 1073741897,
        }

        self.dict_touches = {}
        for key in self.alphabet_clee.values():
            self.dict_touches[key] = "lacher"

    def ajoute_touche(self, touche: str, value: int):
        """permet d'ajouter une touche au clavier"""
        if len(touche) > 0:
            self.alphabet_clee[touche] = value
        self.dict_touches[value] = "lacher"

    def actualise_all_touche(self):
        """actualise toute les touches"""
        for clee, touche in self.dict_touches.items():
            if touche == "vien_presser":
                self.dict_touches[clee] = "presser"
            elif touche == "vien_lacher":
                self.dict_touches[clee] = "lacher"

    def get_pression(self, clee: str | int):
        """get la pression d'une touche"""
        # print([clee])
        if isinstance(clee, str):  # c'est équivalen de type(clee)==str
            return self.dict_touches[self.convert_touche_key(clee)]
        return self.dict_touches[clee]

    def set_pression(self, clee: str, value: str):
        """change la pression d'une touche"""
        self.dict_touches[clee] = value

    def convert_touche_key(self, touche: str) -> int:
        """converti une touche en key
        exemple 't' -> 116
        """
        return self.alphabet_clee[touche]

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_touches.items():
            res += f"{clee}:{value},"
        res += "}-"
        return res


class Souris:
    """cette class permet de gérer la souris
    peremet de savoir la position de la souris
    et permet de savoir si un clique est presser ou lacher
    """

    def __init__(self):
        self.actualise_position()
        self.clique_clee = {"clique_gauche": 1, "clique_droit": 3}
        self.dict_clique = {}
        for key in self.clique_clee.values():
            self.dict_clique[key] = "lacher"

    def actualise_all_clique(self):
        """actualise toute les touches"""
        for clee, touche in self.dict_clique.items():
            if touche == "vien_presser":
                self.dict_clique[clee] = "presser"
            elif touche == "vien_lacher":
                self.dict_clique[clee] = "lacher"

    def get_pression(self, clee: str | int):
        """get la pression d'une touche"""
        if isinstance(clee, str):  # c'est équivalen de type(clee)==str
            return self.dict_clique[self.convert_clique_key(clee)]
        return self.dict_clique[clee]

    def set_pression(self, clee: str, value: str):
        """change la pression d'une touche"""
        self.dict_clique[clee] = value

    def get_pos(self):
        """get la position de la souris"""
        return self.pos

    def actualise_position(self):
        """actualise la position de la souris"""
        self.pos = pygame.mouse.get_pos()

    def convert_clique_key(self, touche: str) -> int:
        """converti une touche en key
        exemple 't' -> 116
        """
        return self.clique_clee[touche]

    def __str__(self) -> str:
        res = "-{"
        for clee, value in self.dict_clique.items():
            res += f"{clee}:{value},"
        res += "}-"
        return res


if __name__ == "__main__":
    pygame.init()
    # print(pygame.key.get_pressed())
    # print(pygame.key.get_repeat())
    # print(pygame.key.get_mods())
    # print(pygame.key.name(121))
    # print(pygame.key.key_code("y"))
    