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
from textures import assembleur
from autre import save


class MenuOption:
    """menu de démarrage"""

    onglet_langue = {
        "fr": ["graphisme", "controle", "langue"],
        "en": ["graphics", "control", "language"],
    }
    bouton_langue = {
        "fr": ["démarrage", "activer", "sauvegarder", "par default", "quitter"],
        "en": ["start", "active", "save", "defaut", "quit"],
    }
    touche_langue = {"fr": {"avancer": "avancer", "gauche": "gauche"}}
    zonetexte_langue = {"fr": ["plein écran"], "en": ["fullscreen"]}
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
        ]  # ["graphisme", "controle", "langue"]
        self.onglet = [
            Bouton(
                (0, 0),
                [
                    assembleur.cadre(taille_onget, (125, 125, 125), couleur, 5)
                    for couleur in ((150, 150, 150), (200, 200, 200), (100, 100, 100))
                ],
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
                ["textures/charançon.png", "textures/charançon2.png"],
                (270, 165),
                (150, 80),
                self.bouton_langue[self.menu_langue][0],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("active", "démarrage_fullscreen"),
            ),
            (
                "graphisme",
                ["textures/charançon.png", "textures/charançon2.png"],
                (440, 165),
                (150, 80),
                self.bouton_langue[self.menu_langue][1],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("active", "active_fullscreen"),
            ),
            (
                "all",
                [
                    assembleur.cadre((160, 50), (125, 125, 125), i, 5)
                    for i in ((100, 100, 100), (150, 150, 150))
                ],
                (0, 0),
                [160, 50],
                self.bouton_langue[self.menu_langue][2],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "save"),
            ),
            (
                "all",
                [
                    assembleur.cadre((160, 50), (125, 125, 125), couleur, 5)
                    for couleur in ((100, 100, 100), (150, 150, 150))
                ],
                [0, 50],
                (160, 50),
                self.bouton_langue[self.menu_langue][3],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "reset"),
            ),
            (
                "all",
                [
                    assembleur.cadre((160, 50), (125, 125, 125), couleur, 5)
                    for couleur in ((100, 100, 100), (150, 150, 150))
                ],
                [0, 100],
                (160, 50),
                self.bouton_langue[self.menu_langue][4],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "quitter"),
            ),
        ):

            self.bouton[onglet].append(
                BoutonText(
                    position, texture, taille, texte, couleur_texte, police, data=data
                )
            )
        for valeur_touche, nom_touche in zip(
            self.controle[0].values(), self.controle[1].values()
        ):
            self.bouton["controle"].append(
                BoutonText(
                    (0, 0),
                    [
                        assembleur.cadre((100, 100), (175, 175, 175), couleur, 5)
                        for couleur in ((150, 150, 150), (125, 125, 125))
                    ],
                    (100, 100),
                    nom_touche,
                    (0, 0, 0),
                    pygame.font.Font(None, 26),
                    data=("push", "touche", valeur_touche),
                )
            )

        self.zone_texte: dict[str, ObjetGraphique] = {
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
        ) in zone_texte:
            self.zone_texte[onglet].append(ObjetGraphique(position, texture, taille))
            self.zone_texte[onglet][-1].texture[0].texture = place_texte_in_texture(
                self.zone_texte[onglet][-1].texture[0].texture,
                texte,
                police,
                couleur_texte,
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
                    bouton.set_pos((screen.get_width() - 160, 0))
                case "reset":
                    bouton.set_pos((screen.get_width() - 160, 60))
                case "quitter":
                    bouton.set_pos((screen.get_width() - 160, 120))
        match self.onglet_actuel:
            case "controle":
                for i, bouton in enumerate(self.bouton["controle"]):
                    bouton.set_pos((50 + i * 110, 200))

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
                            return "save"
                        case "reset":
                            self.graphisme = save.load_json(self.lien_defaut_graphime)
                            self.controle = save.load_json(self.lien_controle_defaut)
                            self.langue_option = save.load_json(self.lien_langue_defaut)
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
    def main(clavier, souris, langue):
        """lance le menu de démarrage"""
        screen.fill((200, 200, 200))
        menu = MenuOption(clavier, souris, langue)
        menu.actualise_dimention()
        clock = pygame.time.Clock()
        encour = True

        while encour:
            event = actualise_event(clavier, souris)
            temp = menu.play()
            if temp == "quitter" or "quitter" in event:
                encour = False
            if "redimentione" in event:
                menu.actualise_dimention()
            screen.fill((200, 200, 200))
            menu.afficher()
            pygame.display.flip()
            clock.tick(60)
        return temp
