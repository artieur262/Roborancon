import pygame

from interface.actualisation_pygame import actualise_event
from interface.graphique import screen
from interface.bouton import BoutonText
from interface.class_clavier import Clavier, Souris
from interface.graphique import ObjetGraphique, gener_texture, place_texte_in_texture
from interface.actualisation_pygame import change_fullscreen

from textures import assembleur

# pylint: disable=no-member


class MenuChangeTouche:
    """menu de changement de touche"""

    traduction = {
        "fr": {
            "bouton": ["retour", "par default", "sauvegarder"],
            "texte": "Veuillez choisir votre touche\n pour ",
        },
        "en": {
            "bouton": ["back", "default", "save"],
            "texte": "Please choose your key\n for ",
        },
    }

    def __init__(
        self,
        clavier: Clavier,
        souris: Souris,
        touche: tuple[str, int],
        nom_touche: str,
        langue: str,
        etat_defaut: str = "en attente",
    ):
        self.clavier = clavier
        self.souris = souris
        self.__touche = touche
        self.langue = langue
        self.etat = etat_defaut
        self.fond = ObjetGraphique(
            (0, 0),
            [assembleur.cadre((450, 450), (150, 150, 150), (200, 200, 200), 10)],
            (450, 450),
        )
        self.zone_texte = ObjetGraphique(
            (0, 0), [gener_texture((430, 150), (0, 0, 0, 0))], (430, 150)
        )
        self.zone_texte.texture[0].texture = place_texte_in_texture(
            self.zone_texte.texture[0].texture,
            self.traduction[self.langue]["texte"] + nom_touche,
            pygame.font.Font(None, 40),
            (0, 0, 0),
        )
        self.bouton: list[BoutonText] = [
            BoutonText(
                (0, 0),
                [
                    assembleur.cadre((300, 75), (175, 175, 175), couleur, 5)
                    for couleur in ((150, 150, 150), (200, 200, 200), (50, 225, 50))
                ],
                (300, 75),
                self.__touche[0],
                (0, 0, 0),
                pygame.font.Font(None, 26),
                data=("push_active", "touche"),
            )
        ]
        # (position,taille,nom_bouton,indice_langue)
        for position, taille, nom_bouton, indice_langue in (
            ((0, 0), (120, 60), "retour", 0),
            ((0, 0), (120, 60), "par default", 1),
            ((0, 0), (120, 60), "sauvegarder", 2),
        ):

            self.bouton.append(
                BoutonText(
                    position,
                    [
                        assembleur.cadre(taille, (175, 175, 175), couleur, 5)
                        for couleur in ((150, 150, 150), (125, 125, 125))
                    ],
                    taille,
                    self.traduction[self.langue]["bouton"][indice_langue],
                    (0, 0, 0),
                    pygame.font.Font(None, 26),
                    data=("push", nom_bouton),
                )
            )

    def actualise_dimention(self):
        """actualise la position des boutons"""
        taille_fond = self.fond.get_size()
        self.fond.set_pos(
            (
                screen.get_width() // 2 - taille_fond[0] // 2,
                screen.get_height() // 2 - taille_fond[1] // 2,
            )
        )
        taille_texte = self.zone_texte.get_size()
        self.zone_texte.set_pos(
            (
                screen.get_width() // 2 - taille_texte[0] // 2,
                screen.get_height() // 2 - taille_texte[1] // 2 - 120,
            )
        )
        for bouton in self.bouton:
            match bouton.data[1]:
                case "touche":
                    bouton.set_pos(
                        (screen.get_width() // 2 - 150, screen.get_height() // 2 - 20)
                    )
                case "retour":
                    bouton.set_pos(
                        (screen.get_width() // 2 - 205, screen.get_height() // 2 + 80)
                    )
                case "par default":
                    bouton.set_pos(
                        (screen.get_width() // 2 - 60, screen.get_height() // 2 + 80)
                    )
                case "sauvegarder":
                    bouton.set_pos(
                        (screen.get_width() // 2 + 85, screen.get_height() // 2 + 80)
                    )

    def afficher(self):
        """affiche le menu de changement de touche"""
        self.fond.afficher()
        self.zone_texte.afficher()
        for bouton in self.bouton:
            bouton.afficher()

    def hover(self):
        """actualise les boutons"""
        for bouton in self.bouton:
            bouton: BoutonText
            match bouton.data[0]:
                case "push":
                    if bouton.point_dans_objet(self.souris.pos):
                        bouton.animation = 1
                    else:
                        bouton.animation = 0
                case "push_active":
                    if bouton.animation != 2 and bouton.point_dans_objet(
                        self.souris.pos
                    ):
                        bouton.animation = 1
                    elif bouton.animation != 2:
                        bouton.animation = 0

    def click(self):
        """actualise les boutons"""
        if self.souris.get_pression(1) == "vien_presser":
            for bouton in self.bouton:
                bouton: BoutonText
                if bouton.point_dans_objet(self.souris.pos):
                    match bouton.data[1]:
                        case "touche":
                            self.etat = "en attente"
                            return "touche"
                        case "retour":
                            self.etat = "en attente"
                            return "retour"
                        case "sauvegarder":
                            return "sauvegarder"
                        case "par default":
                            self.etat = "en attente"
                            return "par default"

    def actualise_event(self):
        """actualise les événement et retourne les événement autre que les touches et les cliques"""
        event_autre = set()
        self.souris.actualise_all_clique()
        self.clavier.update_all_key()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_autre.add("quitter")

            elif event.type in (
                pygame.VIDEORESIZE,
                pygame.WINDOWSIZECHANGED,
            ):
                event_autre.add("redimentione")

            elif event.type == pygame.KEYDOWN:
                self.clavier.set_pression(event.key, "vien_presser")
                if self.etat == "en attente" and event.key != pygame.K_ESCAPE:
                    if event.key in Clavier.key_names[self.langue]:
                        nom_touche = Clavier.key_names[self.langue][event.key]
                    elif len(pygame.key.name(event.key)) != 0:
                        nom_touche = pygame.key.name(event.key)
                    elif len(str(event.unicode)) != 0:
                        nom_touche = event.unicode
                    else:
                        nom_touche = str(event.key)
                    self.set_touche((nom_touche, event.key))
                    self.etat = "attente"
                    self.bouton[0].animation = 0

            elif event.type == pygame.KEYUP:
                self.clavier.set_pression(event.key, "vien_lacher")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.souris.set_pression(event.button, "vien_presser")

            elif event.type == pygame.MOUSEBUTTONUP:
                self.souris.set_pression(event.button, "vien_lacher")
            # if event.type not in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
            #     print(event)

        self.souris.update_pos()
        return event_autre

    def set_touche(self, touche: tuple[str, int]):
        """change la touche"""
        self.__touche = touche
        self.bouton[0].set_text(self.__touche[0], pygame.font.Font(None, 26), (0, 0, 0))

    def get_touche(self):
        """retourne la touche"""
        return self.__touche

    def actualise_bouton(self):
        """actualise les boutons"""
        if self.etat == "en attente":
            self.bouton[0].animation = 2

    def actualise(self):
        """actualise le menu de changement de touche"""
        self.actualise_bouton()
        self.hover()
        return self.click()

    def play(self):
        """joue le menu de changement de touche"""
        event = self.actualise_event()
        temp = self.actualise()
        if (
            "quitter" in event
            or self.clavier.get_pression(pygame.K_ESCAPE) == "vien_presser"
        ):
            return "retour"
        if self.clavier.get_pression(pygame.K_F11) == "vien_presser":
            change_fullscreen()
            event.add("redimentione")
        if (
            "redimentione" in event
            or self.clavier.get_pression(pygame.K_F11) == "vien_presser"
        ):
            self.actualise_dimention()
        if temp == "touche":
            self.etat = "en attente"

        screen.fill((200, 200, 200))
        self.afficher()
        pygame.display.flip()
        return temp

    @staticmethod
    def main(
        clavier,
        souris,
        touche: tuple[int, int],
        nom_touche: str,
        touche_default: tuple[int, int],
        langue: str,
    ):
        """lance le menu de changement de touche"""
        screen.fill((200, 200, 200))
        touche_depart = touche
        menu = MenuChangeTouche(clavier, souris, touche, nom_touche, langue)
        menu.actualise_dimention()
        clock = pygame.time.Clock()
        encour = True

        while encour:
            temp = menu.play()
            if temp in ("sauvegarder", "retour"):
                encour = False

            if temp == "par default":
                menu.set_touche(touche_default)
            clock.tick(60)
        if temp == "sauvegarder":
            return menu.get_touche()
        elif temp == "retour":
            return touche_depart


class MenuChoixLangue:
    """menu de choix de langue"""

    traduction = {
        "fr": {
            "langue": {"fr": "français", "en": "anglais"},
            "bouton": ["retour", "sauvegarder"],
            "texte": "Veuillez choisir votre langue",
        },
        "en": {
            "langue": {"fr": "french", "en": "english"},
            "bouton": ["back", "save"],
            "texte": "Please choose your language",
        },
    }
    

    def __init__(
        self,
        clavier: Clavier,
        souris: Souris,
        langue_dispo: list[str],
        langue_base: str,
        menu_langue: str,
    ):
        self.nouvelle_langue = langue_base
        self.clavier = clavier
        self.souris = souris
        self.menu_langue = menu_langue
        self.fond = ObjetGraphique(
            (0, 0),
            [assembleur.cadre((450, 450), (150, 150, 150), (200, 200, 200), 10)],
            (450, 450),
        )
        self.zone_texte = ObjetGraphique(
            (0, 0), [gener_texture((430, 150), (0, 0, 0, 0))], (430, 150)
        )
        self.zone_texte.texture[0].texture = place_texte_in_texture(
            self.zone_texte.texture[0].texture,
            self.traduction[self.menu_langue]["texte"],
            pygame.font.Font(None, 40),
            (0, 0, 0),
        )
        self.bouton: list[BoutonText] = []
        # (position,taille,nom_bouton,indice_langue)
        for position, taille, nom_bouton, indice_langue in (
            ((0, 0), (150, 50), "retour", 0),
            ((0, 0), (150, 50), "sauvegarder", 1),
        ):
            self.bouton.append(
                BoutonText(
                    position,
                    [
                        assembleur.cadre((150, 50), (175, 175, 175), couleur, 5)
                        for couleur in ((150, 150, 150), (125, 125, 125))
                    ],
                    taille,
                    self.traduction[self.menu_langue]["bouton"][indice_langue],
                    (0, 0, 0),
                    pygame.font.Font(None, 26),
                    data=("push", nom_bouton),
                )
            )
        for i, langue in enumerate(langue_dispo):
            self.bouton.append(
                BoutonText(
                    (0, 0),
                    [
                        assembleur.cadre((300, 75), (175, 175, 175), couleur, 5)
                        for couleur in ((150, 150, 150), (200, 200, 200), (50, 225, 50))
                    ],
                    (300, 75),
                    self.traduction[langue]["langue"][langue]
                    + "/"
                    + self.traduction[self.menu_langue]["langue"][langue],
                    (0, 0, 0),
                    pygame.font.Font(None, 26),
                    data=("push_active", "langue", langue, i),
                )
            )

    def actualise_dimention(self):
        """actualise la position des boutons"""
        taille_fond = self.fond.get_size()
        self.fond.set_pos(
            (
                screen.get_width() // 2 - taille_fond[0] // 2,
                screen.get_height() // 2 - taille_fond[1] // 2,
            )
        )
        taille_texte = self.zone_texte.get_size()
        self.zone_texte.set_pos(
            (
                screen.get_width() // 2 - taille_texte[0] // 2,
                screen.get_height() // 2 - taille_texte[1] // 2 - 100,
            )
        )
        for bouton in self.bouton:
            match bouton.data[1]:
                case "langue":
                    bouton.set_pos(
                        (
                            screen.get_width() // 2 - 150,
                            screen.get_height() // 2 - 20 + 110 * bouton.data[3],
                        )
                    )
                case "retour":
                    bouton.set_pos(
                        (screen.get_width() // 2 - 215, screen.get_height() // 2 - 215)
                    )
                case "sauvegarder":
                    bouton.set_pos(
                        (screen.get_width() // 2 + 65, screen.get_height() // 2 - 215)
                    )

    def afficher(self):
        """affiche le menu de changement de langue"""
        self.fond.afficher()
        self.zone_texte.afficher()
        for bouton in self.bouton:
            bouton.afficher()

    def actualise_bouton(self):
        """actualise les boutons"""
        for bouton in self.bouton:
            bouton: BoutonText
            match bouton.data[1]:
                case "langue":
                    if bouton.data[2] == self.nouvelle_langue:
                        bouton.animation = 2
                    else:
                        bouton.animation = 0

    def hover(self):
        """actualise les boutons"""
        for bouton in self.bouton:
            bouton: BoutonText
            match bouton.data[0]:
                case "push":
                    if bouton.point_dans_objet(self.souris.pos):
                        bouton.animation = 1
                    else:
                        bouton.animation = 0
                case "push_active":
                    if bouton.animation != 2 and bouton.point_dans_objet(
                        self.souris.pos
                    ):
                        bouton.animation = 1
                    elif bouton.animation != 2:
                        bouton.animation = 0

    def click(self):
        """actualise les boutons"""
        if self.souris.get_pression(1) == "vien_presser":
            for bouton in self.bouton:
                bouton: BoutonText
                if bouton.point_dans_objet(self.souris.pos):
                    match bouton.data[1]:
                        case "langue":
                            self.nouvelle_langue = bouton.data[2]
                        case "retour":
                            return "retour"
                        case "sauvegarder":
                            return "sauvegarder"

    def actualise(self):
        """actualise le menu de changement de langue"""
        self.actualise_bouton()
        self.hover()
        return self.click()

    def play(self):
        """joue le menu de changement de langue"""
        event = actualise_event(self.clavier, self.souris)
        temp = self.actualise()
        if (
            "quitter" in event
            or self.clavier.get_pression(pygame.K_ESCAPE) == "vien_presser"
        ):
            return "retour"
        if self.clavier.get_pression(pygame.K_F11) == "vien_presser":
            change_fullscreen()
            event.add("redimentione")
        if (
            "redimentione" in event
            or self.clavier.get_pression(pygame.K_F11) == "vien_presser"
        ):
            self.actualise_dimention()
        screen.fill((200, 200, 200))
        self.afficher()
        pygame.display.flip()
        return temp

    @staticmethod
    def main(
        clavier: Clavier,
        souris: Souris,
        langue_dispo: list[str],
        langue_de_base: str,
        langue: str,
    ):
        """lance le menu de changement de langue"""
        langue_debut = langue_de_base
        screen.fill((200, 200, 200))
        menu = MenuChoixLangue(clavier, souris, langue_dispo, langue_de_base, langue)
        menu.actualise_dimention()
        clock = pygame.time.Clock()
        encour = True

        while encour:
            temp = menu.play()
            if temp in ("sauvegarder", "retour"):
                encour = False

            if temp in langue_dispo:
                return temp
            clock.tick(60)
        if temp == "sauvegarder":
            return menu.nouvelle_langue
        elif temp == "retour":
            return langue_debut
