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

    onglet_langue = {
        "fr": ["graphisme", "controle", "langue"],
        "en": ["graphics", "control", "language"],
    }
    bouton_langue = {
        "fr": ["démarrage", "activer", "sauvegarder", "par default", "quitter"],
        "en": ["start", "active", "save", "defaut", "quit"],
    }
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
                [gener_texture((1, 1), (125, 125, 125)) for _ in range(3)],
                (taille_onget),
                data,
            )
            for data in self.onglet_nom
        ]
        for i, onglet in enumerate(self.onglet):
            onglet.set_pos((50 + i * 170, 10))
            onglet.texture[0].texture.blit(
                gener_texture(
                    (taille_onget[0] - 10, taille_onget[1] - 10), (150, 150, 150)
                ),
                (5, 5),
            )
            onglet.texture[1].texture.blit(
                gener_texture(
                    (taille_onget[0] - 10, taille_onget[1] - 10), (200, 200, 200)
                ),
                (5, 5),
            )
            onglet.texture[2].texture.blit(
                gener_texture(
                    (taille_onget[0] - 10, taille_onget[1] - 10), (100, 100, 100)
                ),
                (5, 5),
            )
            for texture in onglet.texture:
                texture.texture = place_texte_in_texture(
                    texture.texture,
                    self.onglet_langue[self.menu_langue][i],
                    pygame.font.Font(None, 40),
                    (0, 0, 0),
                )
        self.onglet[0].actif = True
        self.onglet[0].animation = 2
        self.bouton: dict[str, Bouton] = {i: [] for i in self.onglet_nom + ["all"]}
        # (onglet, texture, position,taille,texte,couleur_texte,font,data)
        for i in (
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
                ["textures/charançon.png", "textures/charançon2.png"],
                (0, 0),
                [150, 50],
                self.bouton_langue[self.menu_langue][2],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "save"),
            ),
            (
                "all",
                ["textures/charançon.png", "textures/charançon2.png"],
                [0, 50],
                (150, 50),
                self.bouton_langue[self.menu_langue][3],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "reset"),
            ),
            (
                "all",
                ["textures/charançon.png", "textures/charançon2.png"],
                [0, 100],
                (150, 50),
                self.bouton_langue[self.menu_langue][4],
                (0, 0, 0),
                pygame.font.Font(None, 35),
                ("push", "quitter"),
            ),
        ):

            self.bouton[i[0]].append(
                BoutonText(i[2], i[1], i[3], i[4], i[5], i[6], data=i[7])
            )

        self.zone_texte: dict[str, ObjetGraphique] = {
            i: [] for i in self.onglet_nom + ["all"]
        }
        # (onglet, texture, position,taille,texte,couleur_texte,font)
        for i in (
            (
                "graphisme",
                [gener_texture((215, 110), (0, 0, 0, 0))],
                (50, 150),
                (1, 1),
                self.zonetexte_langue[self.menu_langue][0],
                (0, 0, 0),
                pygame.font.Font(None, 50),
            ),
        ):
            self.zone_texte[i[0]].append(ObjetGraphique(i[2], i[1], i[3]))
            self.zone_texte[i[0]][-1].texture[0].texture = place_texte_in_texture(
                self.zone_texte[i[0]][-1].texture[0].texture,
                i[4],
                i[6],
                i[5],
            )
        self.fond = {i: [] for i in self.onglet_nom + ["all"]}
        # (onglet, texture, position,taille)
        for i in (
            (
                "graphisme",
                [assembleur.bouton1([10, 1])],
                (50, 150),
                (560, 110),
            ),
        ):
            self.fond[i[0]].append(ObjetGraphique(i[2], i[1], i[3]))

    def desactive_onglet(self):
        for onglet in self.onglet:
            onglet.actif = False
            onglet.animation = 0

    def actualise(self):
        """actualise le menu de démarrage"""
        self.hover()
        self.actualise_bouton()
        return self.click()

    def actualise_dimention(self):
        for bouton in self.bouton["all"]:
            if bouton.data[1] == "save":
                bouton.set_pos((screen.get_width() - 150, 0))
            elif bouton.data[1] == "reset":
                bouton.set_pos((screen.get_width() - 150, 60))
            elif bouton.data[1] == "quitter":
                bouton.set_pos((screen.get_width() - 150, 120))

    def actualise_bouton(self):
        """actualise les boutons"""
        for bouton in self.bouton[self.onglet_actuel]:
            bouton: Bouton
            if bouton.data[1] == "démarrage_fullscreen":
                if self.graphisme["fullscreen"]:
                    bouton.animation = 1
                else:
                    bouton.animation = 0
            elif bouton.data[1] == "active_fullscreen":
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
                    if bouton.data[1] == "démarrage_fullscreen":
                        self.graphisme["fullscreen"] = not self.graphisme["fullscreen"]
                        # print("cat2")
                    elif bouton.data[1] == "active_fullscreen":
                        change_fullscreen()
                        # print("cat1")
            for onglet in self.onglet:
                if onglet.point_dans_objet(self.souris.pos):
                    self.desactive_onglet()
                    onglet.actif = True
                    onglet.animation = 2
                    self.onglet_actuel = onglet.data

            for bouton in self.bouton["all"]:
                bouton: Bouton
                if bouton.point_dans_objet(self.souris.pos):
                    if bouton.data[1] == "save":
                        save.save_json(self.lien_graphisme, self.graphisme)
                        save.save_json(self.lien_controle, self.controle)
                        save.save_json(self.lien_langue, self.langue_option)
                        return "save"
                    elif bouton.data[1] == "reset":
                        self.graphisme = save.load_json(self.lien_defaut_graphime)
                        self.controle = save.load_json(self.lien_controle_defaut)
                        self.langue_option = save.load_json(self.lien_langue_defaut)
                    elif bouton.data[1] == "quitter":
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
