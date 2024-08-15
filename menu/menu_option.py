"""menu pour gérer les options du jeu

il y a 3 class:
    - MenuChangeTouche : menu de changement de touche
    - MenuChoixLangue : menu de choix de langue
    - MenuOption : menu des options du jeu

"""

import pygame
from interface.graphique import (
    screen,
    gener_texture,
    place_texte_in_texture,
    ObjetGraphique,
)
from interface.bouton import Bouton, BoutonText

# from interface.scrolling_bar import ScrollBar
from interface.class_clavier import Clavier, Souris
from interface.actualisation_pygame import (
    actualise_event,
    get_fullscreen,
    change_fullscreen,
)
from menu.pop_up import PopUp
from menu.sousmenu_option import MenuChangeTouche, MenuChoixLangue
from menu.menu_choix import MenuChoix
from textures import assembleur
from autre import save

# pylint: disable=no-member


class MenuOption:
    """menu de démarrage"""

    # ordre_touche = ["avancer", "reculer", "gauche", "droite"]
    onglet_langue = {
        "fr": ["graphisme", "controles", "langue"],
        "en": ["graphics", "controls", "language"],
    }
    bouton_langue = {
        "fr": ["démarrage", "activer", "sauvegarder", "par default", "quitter"],
        "en": ["start", "active", "save", "defaut", "quit"],
    }
    touche_langue = {
        "fr": {
            "avancer": "avancer",
            "reculer": "reculer",
            "gauche": "gauche",
            "droite": "droite",
        },
        "en": {
            "avancer": "forward",
            "reculer": "backward",
            "gauche": "left",
            "droite": "right",
        },
    }
    zonetexte_langue = {
        "fr": [
            "plein écran",
            "menu",
            "/!\\ Pour que le changement de langue soit appliqué,\nil faut redémarrer le jeu.",
        ],
        "en": [
            "fullscreen",
            "menu",
            "/!\\ For the language change to be applied,\nyou must restart the game.",
        ],
    }
    langue_popup = {
        "fr": [
            "sauvegarde réussie",
            "l'onglet viens de reprendre ses paramêtre par défault ",
            "voulez vous sauvegarder avant de quitter ?",
            ["oui", "non"],
        ],
        "en": [
            "Saved successfully",
            "the tab has just taken its default parameters",
            "do you want to save before quitting ?",
            ["yes", "no"],
        ],
    }
    lien_graphisme = "option/graphisme.json"
    lien_defaut_graphime = "option/graphisme_defaut.json"
    lien_controle = "option/control.json"
    lien_controle_defaut = "option/control_defaut.json"
    lien_langue = "option/langue.json"
    lien_langue_defaut = "option/langue_defaut.json"

    def __init__(
        self,
        clavier: Clavier,
        souris: Souris,
        menu_langue: str,
    ):
        self.clavier = clavier
        self.souris = souris
        self.graphisme = save.load_json(self.lien_graphisme)
        self.controle = save.load_json(self.lien_controle)
        self.langue_option = save.load_json(self.lien_langue)
        self.menu_langue = menu_langue

        self.onglet_actuel = "graphisme"
        taille_onget = (160, 50)
        self.onglet_nom = self.onglet_langue[
            "fr"
        ]  # ["graphisme", "controles", "langue"]
        self.onglet = [
            Bouton(
                (0, 0),
                [assembleur.bouton2(160, i) for i in (1, 3, 2)],
                (taille_onget),
                data,
            )
            for data in self.onglet_nom
        ]
        for i, onglet in enumerate(self.onglet):
            onglet.set_pos((50 + i * 170, 10))
            for texture in onglet.texture:
                texture.texture = place_texte_in_texture(
                    texture.texture,
                    self.onglet_langue[self.menu_langue][i],
                    pygame.font.Font(None, 40),
                    (0, 0, 0),
                )
        self.onglet[0].actif = True
        self.onglet[0].animation = 2
        self.bouton: dict[str, list[Bouton]] = {
            onglet: [] for onglet in self.onglet_nom + ["all"]
        }
        # (onglet, texture, position,taille,texte,couleur_texte,police,data)
        for onglet, texture, position, taille, texte, couleur_texte, police, data in (
            (
                "graphisme",
                [
                    gener_texture((1, 1), (200, 50, 50)),
                    gener_texture((1, 1), (50, 200, 50)),
                ],
                (270, 165),
                (150, 80),
                self.bouton_langue[self.menu_langue][0],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("active", "démarrage_fullscreen"),
            ),
            (
                "graphisme",
                [
                    gener_texture((1, 1), (200, 50, 50)),
                    gener_texture((1, 1), (50, 200, 50)),
                ],
                (440, 165),
                (150, 80),
                self.bouton_langue[self.menu_langue][1],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("active", "active_fullscreen"),
            ),
            (
                "all",
                [assembleur.bouton2(170, i) for i in (1, 2)],
                (0, 0),
                [170, 50],
                self.bouton_langue[self.menu_langue][2],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "save"),
            ),
            (
                "all",
                [assembleur.bouton2(170, i) for i in (1, 2)],
                [0, 50],
                (170, 50),
                self.bouton_langue[self.menu_langue][3],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "reset"),
            ),
            (
                "all",
                [assembleur.bouton2(170, i) for i in (1, 2)],
                [0, 100],
                (170, 50),
                self.bouton_langue[self.menu_langue][4],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "quitter"),
            ),
            (
                "langue",
                [
                    assembleur.cadre((60, 60), (125, 125, 125), couleur, 4)
                    for couleur in ((150, 150, 150), (100, 100, 100))
                ],
                (235, 200),
                (60, 60),
                self.langue_option["menu"],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "langue_menu"),
            ),
        ):

            self.bouton[onglet].append(
                BoutonText(
                    position, texture, taille, texte, couleur_texte, police, data=data
                )
            )

        self.zone_texte: dict[str, list[ObjetGraphique]] = {
            onglet: [] for onglet in self.onglet_nom + ["all"]
        }
        zone_texte = (
            (
                "graphisme",
                [gener_texture((215, 110), (0, 0, 0, 0))],
                (50, 150),
                (1, 1),
                self.zonetexte_langue[self.menu_langue][0],
                (0, 0, 0),
                pygame.font.Font(None, 50),
                "centrage",
            ),
            (
                "langue",
                [assembleur.bouton1([2, 0])],
                (75, 200),
                (560, 110),
                self.zonetexte_langue[self.menu_langue][1],
                (0, 0, 0),
                pygame.font.Font(None, 40),
                "centrage",
            ),
            (
                "langue",
                [gener_texture((800, 75), (0, 0, 0, 0))],
                (75, 100),
                (800, 75),
                self.zonetexte_langue[self.menu_langue][2],
                (200, 10, 10),
                pygame.font.Font(None, 40),
                "gauche_centre",
            ),
        )

        # (onglet, texture, position,taille,texte,couleur_texte,font)
        for (
            onglet,
            texture,
            position,
            taille,
            texte,
            couleur_texte,
            police,
            mode_palcement,
        ) in zone_texte:
            self.zone_texte[onglet].append(ObjetGraphique(position, texture, taille))
            self.zone_texte[onglet][-1].texture[0].texture = place_texte_in_texture(
                self.zone_texte[onglet][-1].texture[0].texture,
                texte,
                police,
                couleur_texte,
                mode_palcement,
            )

        # place les boutons et les zones de texte pour changer les controles
        for controle in self.controle[0]:
            self.bouton["controles"].append(
                BoutonText(
                    (0, 0),
                    [
                        assembleur.cadre((120, 60), (175, 175, 175), couleur, 5)
                        for couleur in ((150, 150, 150), (125, 125, 125))
                    ],
                    (120, 60),
                    self.controle[1][controle],
                    (0, 0, 0),
                    pygame.font.Font(None, 26),
                    data=(
                        "push",
                        "touche",
                        controle,
                        (self.controle[1][controle], self.controle[0][controle]),
                    ),
                )
            )
            self.zone_texte["controles"].append(
                ObjetGraphique(
                    (0, 0),
                    [assembleur.bouton1([1, 0])],
                    (110, 60),
                )
            )
            self.zone_texte["controles"][-1].texture[0].texture = (
                place_texte_in_texture(
                    self.zone_texte["controles"][-1].texture[0].texture,
                    controle,
                    pygame.font.Font(None, 26),
                    (0, 0, 0),
                )
            )
        self.fond = {onglet: [] for onglet in self.onglet_nom + ["all"]}
        # (onglet, texture, position,taille)
        for onglet, texture, position, taille in (
            (
                "graphisme",
                [assembleur.bouton1([10, 1])],
                (50, 150),
                (560, 110),
            ),
        ):
            self.fond[onglet].append(ObjetGraphique(position, texture, taille))

    def actualise_info_bouton(self):
        """actualise les textes"""
        for bouton in self.bouton["controles"]:
            bouton: BoutonText
            bouton.set_text(
                self.controle[1][bouton.data[2]],
                pygame.font.Font(None, 26),
                (0, 0, 0),
            )
            bouton.data = (
                "push",
                "touche",
                bouton.data[2],
                (self.controle[1][bouton.data[2]], self.controle[0][bouton.data[2]]),
            )
        for bouton in self.bouton["langue"]:
            bouton: BoutonText
            match bouton.data[1]:
                case "langue_menu":
                    bouton.set_text(
                        self.langue_option["menu"],
                        pygame.font.Font(None, 35),
                        (0, 0, 0),
                    )
        self.actualise_bouton()

    def desactive_onglet(self):
        """désactive les onglets"""
        for onglet in self.onglet:
            onglet.actif = False
            onglet.animation = 0

    def actualise(self):
        """actualise le menu de démarrage"""
        self.hover()
        self.actualise_bouton()
        return self.click()

    def actualise_dimention(self):
        """actualise les dimention des objets"""
        for bouton in self.bouton["all"]:
            match bouton.data[1]:
                case "save":
                    bouton.set_pos((screen.get_width() - bouton.get_size()[0], 0))
                case "reset":
                    bouton.set_pos((screen.get_width() - bouton.get_size()[0], 60))
                case "quitter":
                    bouton.set_pos((screen.get_width() - bouton.get_size()[0], 120))
        match self.onglet_actuel:
            case "controles":
                max_ligne = (screen.get_width() - 210) // 250
                if max_ligne < 2:
                    max_ligne = 2

                for i, bouton in enumerate(self.bouton["controles"]):
                    bouton.set_pos(
                        (160 + i % max_ligne * 250, 150 + 70 * (i // max_ligne))
                    )
                for i, zone_texte in enumerate(self.zone_texte["controles"]):
                    zone_texte.set_pos(
                        (50 + i % max_ligne * 250, 150 + 70 * (i // max_ligne))
                    )

    def actualise_bouton(self):
        """actualise les boutons"""
        for bouton in self.bouton[self.onglet_actuel]:
            bouton: Bouton
            match bouton.data[1]:
                case "démarrage_fullscreen":
                    if self.graphisme["fullscreen"]:
                        bouton.animation = 1
                    else:
                        bouton.animation = 0
                case "active_fullscreen":
                    if get_fullscreen():
                        bouton.animation = 1
                    else:
                        bouton.animation = 0

    def hover(self):
        """actualise les boutons"""
        for onglet in self.onglet:
            if not onglet.actif:
                if onglet.point_dans_objet(self.souris.pos):
                    onglet.animation = 1
                else:
                    onglet.animation = 0
        for bouton in self.bouton[self.onglet_actuel]:
            bouton: Bouton
            if bouton.data[0] == "push":
                if bouton.point_dans_objet(self.souris.pos):
                    bouton.animation = 1
                else:
                    bouton.animation = 0
        for bouton in self.bouton["all"]:
            bouton: Bouton
            if bouton.data[0] == "push":
                if bouton.point_dans_objet(self.souris.pos):
                    bouton.animation = 1
                else:
                    bouton.animation = 0

    def click(self):
        """actualise les boutons"""
        if self.souris.get_pression(1) == "vien_presser":
            for bouton in self.bouton[self.onglet_actuel]:
                bouton: Bouton
                if bouton.point_dans_objet(self.souris.pos):
                    match bouton.data[1]:
                        case "démarrage_fullscreen":
                            self.graphisme["fullscreen"] = not self.graphisme[
                                "fullscreen"
                            ]
                            # print("cat2")
                        case "active_fullscreen":
                            change_fullscreen()
                            # print("cat1")
                        case "touche":
                            # print(self.lien_controles_defaut)
                            par_default = save.load_json(self.lien_controle_defaut)

                            touche = MenuChangeTouche.main(
                                self.clavier,
                                self.souris,
                                bouton.data[3],
                                (
                                    par_default[1][bouton.data[2]],
                                    par_default[0][bouton.data[2]],
                                ),
                                self.menu_langue,
                            )
                            self.controle[1][bouton.data[2]] = touche[0]
                            self.controle[0][bouton.data[2]] = touche[1]
                            bouton.set_text(
                                touche[0], pygame.font.Font(None, 26), (0, 0, 0)
                            )
                            self.actualise_dimention()
                        case "langue_menu":
                            langue = MenuChoixLangue.main(
                                self.clavier,
                                self.souris,
                                ["fr", "en"],
                                self.langue_option["menu"],
                                self.menu_langue,
                            )
                            self.langue_option["menu"] = langue
                            bouton.set_text(
                                langue,
                                pygame.font.Font(None, 35),
                                (0, 0, 0),
                            )
                            self.actualise_dimention()
            for onglet in self.onglet:
                if onglet.point_dans_objet(self.souris.pos):
                    self.desactive_onglet()
                    onglet.actif = True
                    onglet.animation = 2
                    self.onglet_actuel = onglet.data
                    self.actualise_dimention()

            for bouton in self.bouton["all"]:
                bouton: Bouton
                if bouton.point_dans_objet(self.souris.pos):
                    match bouton.data[1]:
                        case "save":
                            save.save_json(self.lien_graphisme, self.graphisme)
                            save.save_json(self.lien_controle, self.controle)
                            save.save_json(self.lien_langue, self.langue_option)
                            texture = assembleur.cadre(
                                (500, 150), (125, 125, 125), (100, 100, 100), 5
                            )
                            texture = place_texte_in_texture(
                                texture,
                                self.langue_popup[self.menu_langue][0],
                                pygame.font.Font(None, 55),
                                (0, 0, 0),
                            )
                            PopUp.main(
                                self.clavier,
                                self.souris,
                                (
                                    screen.get_width() // 2 - 250,
                                    screen.get_height() // 2 - 75,
                                ),
                                texture,
                                2.5,
                            )
                            self.actualise_dimention()
                            return "save"
                        case "reset":
                            match self.onglet_actuel:
                                case "graphisme":
                                    self.graphisme = save.load_json(
                                        self.lien_defaut_graphime
                                    )
                                case "controles":
                                    self.controle = save.load_json(
                                        self.lien_controle_defaut
                                    )
                                case "langue":
                                    self.langue_option = save.load_json(
                                        self.lien_langue_defaut
                                    )
                            self.actualise_info_bouton()
                            self.afficher()
                            texture = assembleur.cadre(
                                (500, 150), (125, 125, 125), (100, 100, 100), 5
                            )
                            texture = place_texte_in_texture(
                                texture,
                                self.langue_popup[self.menu_langue][1],
                                pygame.font.Font(None, 55),
                                (0, 0, 0),
                            )
                            PopUp.main(
                                self.clavier,
                                self.souris,
                                (
                                    screen.get_width() // 2 - 250,
                                    screen.get_height() // 2 - 75,
                                ),
                                texture,
                                2.5,
                            )
                            self.actualise_dimention()
                        case "quitter":
                            return "quitter"

    def afficher(self):
        """affiche le menu de démarrage"""
        for onglet in self.onglet:
            onglet.afficher()
        for fond in self.fond[self.onglet_actuel]:
            fond.afficher()
        for fond in self.fond["all"]:
            fond.afficher()
        for zone_texte in self.zone_texte[self.onglet_actuel]:
            zone_texte.afficher()
        for zone_texte in self.zone_texte["all"]:
            zone_texte.afficher()
        for bouton in self.bouton[self.onglet_actuel]:
            bouton.afficher()
        for bouton in self.bouton["all"]:
            bouton.afficher()

    def play(self):
        """lance le menu de démarrage"""
        return self.actualise()

    @staticmethod
    def main(clavier: Clavier, souris: Souris, langue: str):
        """lance le menu de démarrage"""
        screen.fill((200, 200, 200))
        menu = MenuOption(clavier, souris, langue)
        menu.actualise_dimention()
        clock = pygame.time.Clock()
        encour = True

        while encour:
            event = actualise_event(clavier, souris)
            temp = menu.play()
            if clavier.get_pression(pygame.K_F11) == "vien_presser":
                change_fullscreen()
                event.add("redimentione")

            if (
                temp == "quitter"
                or "quitter" in event
                or clavier.get_pression(pygame.K_ESCAPE) == "vien_presser"
            ):
                if (
                    save.load_json(menu.lien_graphisme) != menu.graphisme
                    or save.load_json(menu.lien_controle) != menu.controle
                    or save.load_json(menu.lien_langue) != menu.langue_option
                ) and menu.langue_popup[menu.menu_langue][3][0] == MenuChoix.main(
                    clavier,
                    souris,
                    screen.copy(),
                    assembleur.cadre((250, 250), (125, 125, 125), (100, 100, 100), 5),
                    menu.langue_popup[menu.menu_langue][2],
                    menu.langue_popup[menu.menu_langue][3],
                ):
                    save.save_json(menu.lien_graphisme, menu.graphisme)
                    save.save_json(menu.lien_controle, menu.controle)
                    save.save_json(menu.lien_langue, menu.langue_option)
                encour = False
                temp = "quitter"
            if "redimentione" in event:
                menu.actualise_dimention()
            screen.fill((200, 200, 200))
            menu.afficher()
            pygame.display.flip()
            clock.tick(60)
        return temp
