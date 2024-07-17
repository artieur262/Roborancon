import pygame
from interface.graphique import (
    screen,
    gener_texture,
    place_texte_in_texture,
    ObjetGraphique,
)
from interface.bouton import Bouton, BoutonText
from interface.scrolling_bar import ScrollBar
from interface.class_clavier import Clavier, Souris
from interface.actualisation_pygame import (
    actualise_event,
    get_fullscreen,
    change_fullscreen,
)
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
    zonetexte_langue = {"fr": ["plien écran"], "en": ["fullscreen"]}
    lien_graphisme = "option/graphisme.json"
    lien_defaut_graphime = "option/graphisme_defaut.json"
    lien_controle = "option/controle.json"
    lien_controle_defaut = "option/controle_defaut.json"
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
        taille_onget = (100, 50)
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
            onglet.set_pos((i * 100, 0))
            onglet.texture[0].texture.blit(
                gener_texture(
                    (taille_onget[0] - 10, taille_onget[1] - 10), (100, 100, 100)
                ),
                (5, 5),
            )
            onglet.texture[1].texture.blit(
                gener_texture(
                    (taille_onget[0] - 10, taille_onget[1] - 10), (150, 150, 150)
                ),
                (5, 5),
            )
            onglet.texture[2].texture.blit(
                gener_texture(
                    (taille_onget[0] - 10, taille_onget[1] - 10), (200, 200, 200)
                ),
                (5, 5),
            )
            for texture in onglet.texture:
                texture.texture = place_texte_in_texture(
                    texture.texture,
                    self.langue_option[self.menu_langue][i],
                    pygame.font.Font(None, 50),
                    (0, 0, 0),
                )

        self.bouton: dict[str, Bouton] = {i: [] for i in self.onglet_nom + ["all"]}
        # (onglet, texture, position,taille,texte,couleur_texte,font,data)
        for i in (
            (
                "graphique",
                ["textures/charançon.png", "textures/charançon2.png"],
                (250, 100),
                (150, 50),
                self.bouton_langue[self.menu_langue][0],
                (0, 0, 0),
                pygame.font.Font(None, 50),
                ("active", "démarrage_fullscreen"),
            ),
            (
                "graphique",
                ["textures/charançon.png", "textures/charançon2.png"],
                (400, 100),
                (150, 50),
                self.bouton_langue[self.menu_langue][1],
                (0, 0, 0),
                pygame.font.Font(None, 50),
                ("active", "active_fullscreen"),
            ),
            (
                "all",
                ["textures/charançon.png", "textures/charançon2.png"],
                (0, 0),
                [150, 50],
                self.bouton_langue[self.menu_langue][2],
                (0, 0, 0),
                pygame.font.Font(None, 50),
                ("push", "save"),
            ),
            (
                "all",
                ["textures/charançon.png", "textures/charançon2.png"],
                [0, 50],
                (150, 50),
                self.bouton_langue[self.menu_langue][3],
                (0, 0, 0),
                pygame.font.Font(None, 50),
                ("push", "reset"),
            ),
            (
                "graphique",
                ["textures/charançon.png", "textures/charançon2.png"],
                [0, 100],
                (150, 50),
                self.bouton_langue[self.menu_langue][4],
                (0, 0, 0),
                pygame.font.Font(None, 50),
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
                "graphique",
                ["textures/charançon.png"],
                (50, 200),
                (200, 50),
                self.zone_texte[self.menu_langue][0],
                (0, 0, 0),
                pygame.font.Font(None, 50),
            ),
        ):
            self.zone_texte[i[0]].append(
                ObjetGraphique(i[1], gener_texture(i[2], (200, 200, 200)), i[2])
            )
            self.zone_texte[i[0]][-1].texture[0] = place_texte_in_texture(
                self.zone_texte[i[0]][-1].texture[0],
                i[4],
                i[6],
                i[5],
            )

    def actualise(self):
        """actualise le menu de démarrage"""
        self.hover()
        self.click()
        self.actualise_bouton()

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
        for bouton in self.bouton[self.onglet_actuel]:
            bouton: Bouton
            if bouton.data[0] == "push":
                bouton.actif = bouton.point_dans_objet(self.souris.pos)
        for bouton in self.bouton["all"]:
            bouton: Bouton
            if bouton.data[0] == "push":
                bouton.actif = bouton.point_dans_objet(self.souris.pos)

    def click(self):
        """actualise les boutons"""
        if self.souris.get_pression(1):
            for bouton in self.bouton[self.onglet_actuel]:
                bouton: Bouton
                if bouton.data[0] == "push" and bouton.actif:
                    if bouton.data[1] == "démarrage_fullscreen":
                        self.graphisme["fullscreen"] = not self.graphisme["fullscreen"]
                    elif bouton.data[1] == "active_fullscreen":
                        change_fullscreen()
            for onglet in self.onglet:
                if onglet.point_dans_objet(self.souris.pos):
                    self.onglet_actuel = onglet.data
            for bouton in self.bouton["all"]:
                bouton: Bouton
                if bouton.data[0] == "push" and bouton.actif:
                    if bouton.data[1] == "save":
                        save.save_json(self.lien_graphisme, self.graphisme)
                        save.save_json(self.lien_controle, self.controle)
                        save.save_json(self.lien_langue, self.langue_option)
                        return "save"
                    elif bouton.data[1] == "reset":
                        self.graphisme = save.load_json(self.lien_graphisme)
                        self.controle = save.load_json(self.lien_controle)
                    elif bouton.data[1] == "quitter":
                        return "quitter"

    def affiche(self):
        """affiche le menu de démarrage"""
        for onglet in self.onglet:
            onglet.affiche()
        for bouton in self.bouton[self.onglet_actuel]:
            bouton.affiche()
        for zone_texte in self.zone_texte[self.onglet_actuel]:
            zone_texte.affiche()

    def play(self):
        """lance le menu de démarrage"""
        self.actualise()
        self.affiche()
        return
