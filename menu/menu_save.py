import os
import time

import pygame

from interface.graphique import (
    screen,
    ObjetGraphique,
    Zone,
    place_texte_in_texture,
    genere_texture,
)
from interface.actualisation_pygame import actualise_event, change_fullscreen
from interface.bouton import BoutonText
from interface.scrolling_bar import ScrollBar
from interface.class_clavier import Clavier, Souris
from menu.menu_entretext import MenuEntreText
from menu.pop_up import PopUp
from textures import assembleur
from autre import save

# pylint: disable=no-member


class Save:
    """Classe pour les utilisateurs"""

    def __init__(
        self,
        name: str,
        type_: str,
        date_creation: str,
        temps: int,
        coordonnee: list[int, int],
    ):
        self.name = name
        self.date = date_creation
        self.type = type_
        self.temps = temps
        self.actualise_graphique(coordonnee)

    def set_animation(self, value: int):
        """Change l'animation"""
        self.graphique.animation = value
        # print(self.graphique.animation)

    def get_animation(self):
        """Renvoie l'animation"""
        return self.graphique.animation

    def actualise_graphique(self, coordonnee):
        """Actualise le graphique"""

        self.graphique = ObjetGraphique(
            coordonnee,
            [
                genere_texture((850, 50), couleur)
                for couleur in (
                    (175, 175, 175),
                    (125, 125, 125),
                    (50, 50, 200),
                )
            ],
            (850, 50),
        )
        for texte, pos, taille in (
            (self.name, (5, 5), (250, 40)),
            (self.type, (260, 5), (140, 40)),
            (convertir_temps(self.temps), (405, 5), (220, 40)),
            (self.date, (630, 5), (215, 40)),
        ):
            for image in self.graphique.texture:
                image.texture.blit(
                    place_texte_in_texture(
                        genere_texture(taille, (75, 75, 75)),
                        texte,
                        pygame.font.SysFont("monospace", 20),
                        (255, 255, 255),
                    ),
                    pos,
                )

    def set_pos(self, pos: tuple[int, int]):
        """Change la position"""
        self.graphique.set_pos(pos)

    def point_dans_objet(self, point: tuple[int, int]):
        """dit si les coordonnées sont dans l'objet"""
        return self.graphique.point_dans_objet(point)

    def afficher(
        self,
        decalage_camera: tuple[int, int] = None,
        surface: pygame.Surface = None,
    ):
        """Affiche l'objet"""
        self.graphique.afficher(decalage_camera, surface)

    def convert_to_dict(self) -> dict:
        """Convertit en dict"""
        return {
            "name": self.name,
            "date": self.date,
            "type": self.type,
            "temps": self.temps,
            "temps_str": convertir_temps(self.temps),
        }

    @staticmethod
    def convert_from_dict(dict_: dict) -> "Save":
        """Convertit en objet"""
        return Save(
            dict_["name"],
            dict_["type"],
            dict_["date"],
            dict_["temps"],
            (0, 0),
        )

    def __lt__(self, other) -> bool:
        return self.date < other.date


class MenuSave:
    """Menu pour charger une sauvegarde ou sauvegarder une partie

    Attributs:
        lien_save: str -- Lien de la sauvegarde
        mode: str -- Mode de la sauvegarde ("sauvegarde" ou "chargement")

    """

    traduction = {
        "fr": {
            "bouton": ["retour", "sauvegarder", "charger", "ajouter"],
            "menu": [
                "nom déjà utilisé",
                "entrez le nom de la sauvegarde",
                "selectionner une sauvegarde",
                "selectionner une sauvegarde\n ou creer une nouvelle",
            ],
            "en_tete": ["nom", "type", "temps", "date"],
            "titre": [
                "veuillez sauvegarder votre partie",
                "veuillez charger une partie",
            ],
        },
        "en": {
            "bouton": ["back", "save", "load", "add"],
            "menu": [
                "name already used",
                "enter the name of the save",
                "select a save",
                "select a save\n or create a new one",
            ],
            "en_tete": ["name", "type", "time", "date"],
            "titre": ["please save your game", "please load a game"],
        },
    }

    def __init__(self, lien_save: str, mode: str, langue: str):
        self.langue = langue
        self.mode = mode
        self.lien_save = lien_save
        self.decalle = 0

        # titre
        titre_str = (
            self.traduction[langue]["titre"][0]
            if mode == "sauvegarde"
            else self.traduction[langue]["titre"][1]
        )
        self.titre = ObjetGraphique(
            (0, 0),
            [
                place_texte_in_texture(
                    genere_texture((800, 50), (0, 0, 0, 0)),
                    titre_str,
                    pygame.font.Font(None, 36),
                    (255, 255, 255),
                )
            ],
            (800, 50),
        )

        # en tête
        self.en_tete = ObjetGraphique(
            (0, 0),
            [genere_texture((870, 50), (135, 135, 135))],
            (870, 50),
        )
        for indice_texte, pos, taille in (
            (0, (5, 5), (250, 40)),
            (1, (260, 5), (140, 40)),
            (2, (405, 5), (220, 40)),
            (3, (630, 5), (215, 40)),
        ):

            self.en_tete.texture[0].texture.blit(
                place_texte_in_texture(
                    genere_texture(taille, (50, 50, 50)),
                    self.traduction[langue]["en_tete"][indice_texte],
                    pygame.font.SysFont("monospace", 20),
                    (255, 255, 255),
                ),
                pos,
            )

        # barre de scroll
        self.barscroll = ScrollBar(
            [0, 0],
            (20, 450),
            genere_texture((20, 450), (125, 125, 125)),
            genere_texture((14, 100), (100, 100, 100)),
            100,
            "vertical",
        )

        # sauvegarde
        self.actualise_save()
        self.surfaces_save = genere_texture((850, 450), (50, 50, 50))
        self.zone_save = Zone((0, 0), (850, 450))

        # génération bouton
        self.bouton: list[BoutonText] = []
        nouveaux_boutons = [0]
        if self.mode == "sauvegarde":
            nouveaux_boutons.append(3)
            nouveaux_boutons.append(1)
        elif self.mode == "chargement":
            nouveaux_boutons.append(2)

        # data_boutons = [self.langue_bouton["fr"][i] for i in nouveaux_boutons]
        taille_bouton = (100, 50)
        for i in nouveaux_boutons:
            self.bouton.append(
                BoutonText(
                    (
                        0,
                        700,
                    ),
                    [
                        assembleur.cadre(taille_bouton, (100, 100, 100), couleur, 5)
                        for couleur in ((150, 150, 150), (175, 175, 175))
                    ],
                    taille_bouton,
                    self.traduction[self.langue]["bouton"][i],
                    (0, 0, 0),
                    pygame.font.Font(None, 20),
                    data=self.traduction["fr"]["bouton"][i],
                )
            )
        # actualisation
        self.actualise_dimensions()

    def actualise(self, souris: Souris, clavier: Clavier):
        """Actualise le menu"""
        self.actualise_decalle()
        self.hover(souris.get_pos())
        return self.click(souris, clavier)

    def actualise_dimensions(self):
        """Actualise les dimensions"""
        taille_save = (self.zone_save.get_size()[0], max(screen.get_height() - 170, 50))
        self.zone_save.set_size(taille_save)
        self.barscroll.set_size((self.barscroll.get_size()[0], taille_save[1]))
        self.barscroll.redimentione_all_image(
            (self.barscroll.get_size()[0], taille_save[1])
        )
        self.actualise_taille_scroll()
        self.surfaces_save = pygame.transform.scale(self.surfaces_save, taille_save)

        self.place_elements()

    def place_elements(self):
        """Place les éléments"""
        self.place_titre()
        self.place_en_tete()
        self.place_zone_save()
        self.place_barscroll()
        self.place_bouton()

    def place_titre(self):
        """Place le titre"""
        self.titre.set_pos(
            (
                screen.get_width() // 2 - self.titre.get_size()[0] // 2,
                0,
            )
        )

    def place_en_tete(self):
        """Place l'en tête"""
        self.en_tete.set_pos(
            (screen.get_width() // 2 - self.zone_save.get_size()[0] // 2, 50)
        )

    def place_zone_save(self):
        """Place la zone de sauvegarde"""
        self.zone_save.set_pos(
            (
                screen.get_width() // 2 - self.zone_save.get_size()[0] // 2,
                self.en_tete.get_pos()[1] + self.en_tete.get_size()[1],
            )
        )

    def place_barscroll(self):
        """Place la barre de scroll"""
        self.barscroll.set_pos(
            (
                self.zone_save.get_pos()[0] + self.zone_save.get_size()[0],
                self.zone_save.get_pos()[1],
            )
        )

    def place_bouton(self):
        """Place les boutons"""
        taille_bouton = self.bouton[0].get_size()
        distance = self.zone_save.get_size()[0] // (len(self.bouton) + 1)
        for i, bouton in enumerate(self.bouton):
            bouton.set_pos(
                (
                    self.zone_save.get_pos()[0]
                    + distance * (i + 1)
                    - taille_bouton[0] // 2,
                    self.zone_save.get_pos()[1] + self.zone_save.get_size()[1] + 20,
                )
            )

    def desactive_save(self):
        """Désactive les sauvegardes"""
        for save_ in self.save:
            save_.set_animation(0)

    def actualise_save(self):
        """Actualise les sauvegardes dans le fichier"""
        self.save = charge_save(self.lien_save)
        self.save.sort(reverse=True)
        place_save(self.save)
        self.actualise_taille_scroll()

    def actualise_taille_scroll(self):
        """Actualise la taille du scroll"""
        maximum_size = self.barscroll.get_size()[1] - self.barscroll.get_marge() * 2
        longueur_save = len(self.save) * 50
        if longueur_save < maximum_size:
            longueur_save = maximum_size
        longueur_save = maximum_size * (maximum_size / longueur_save)
        if longueur_save < 30:
            longueur_save = 30
        self.barscroll.set_taille_scroll(longueur_save)

    def actualise_decalle(self):
        """Actualise le decalle"""
        longuer_save = len(self.save) * 50
        self.decalle = (
            longuer_save - self.zone_save.get_size()[1]
        ) * self.barscroll.get_pourcentage()
        if self.decalle < 0:
            self.decalle = 0

    def hover(self, pos_souris: tuple[int, int]):
        """Gère le survol"""

        # bouton hover
        for bouton in self.bouton:
            if bouton.point_dans_objet(pos_souris):
                bouton.set_animation(1)
            else:
                bouton.set_animation(0)

        # save hover
        for save_ in self.save:
            if save_.get_animation() != 2:
                if save_.point_dans_objet(
                    adition_tuple(
                        (pos_souris[0], pos_souris[1] - self.decalle),
                        (
                            -self.zone_save.get_pos()[0],
                            -self.zone_save.get_pos()[1],
                        ),
                    )
                ):
                    save_.set_animation(1)
                else:
                    save_.set_animation(0)

    def click(self, souris: Souris, clavier: Clavier):
        """Gère les clicks"""

        self.barscroll.souris_scroll(souris.get_pos())
        if souris.get_pression(1) == "vien_presser":
            if self.barscroll.point_dans_objet(souris.get_pos()):
                self.barscroll.activer()
            pos_souris = souris.get_pos()
            if self.zone_save.point_dans_objet(pos_souris):
                for save_ in self.save:
                    if save_.point_dans_objet(
                        adition_tuple(
                            (pos_souris[0], pos_souris[1] - self.decalle),
                            (
                                -self.zone_save.get_pos()[0],
                                -self.zone_save.get_pos()[1],
                            ),
                        )
                    ):
                        if save_.get_animation() == 2:
                            return "lien", save_.name
                        else:
                            self.desactive_save()
                            # print("cat")
                            save_.set_animation(2)
            for bouton in self.bouton:
                if bouton.point_dans_objet(pos_souris):
                    match bouton.data:
                        case "retour":
                            return "action", "retour"
                        case "sauvegarder":
                            for save_ in self.save:
                                if save_.get_animation() == 2:
                                    return "lien", save_.name
                            PopUp.main(
                                Clavier(),
                                Souris(),
                                (
                                    screen.get_width() // 2 - 360 // 2,
                                    screen.get_height() // 2 - 70 // 2,
                                ),
                                place_texte_in_texture(
                                    assembleur.cadre(
                                        (360, 70), (100, 100, 100), (130, 130, 130), 5
                                    ),
                                    self.traduction[self.langue]["menu"][3],
                                    pygame.font.Font(None, 30),
                                    (0, 0, 0),
                                ),
                                3,
                            )
                            clavier.lacher_tout()
                            souris.lacher_tout()
                            self.actualise_dimensions()

                        case "charger":
                            for save_ in self.save:
                                if save_.get_animation() == 2:
                                    return "lien", save_.name
                            PopUp.main(
                                Clavier(),
                                Souris(),
                                (
                                    screen.get_width() // 2 - 360 // 2,
                                    screen.get_height() // 2 - 0 // 2,
                                ),
                                place_texte_in_texture(
                                    assembleur.cadre(
                                        (360, 70), (100, 100, 100), (130, 130, 130), 5
                                    ),
                                    self.traduction[self.langue]["menu"][2],
                                    pygame.font.Font(None, 30),
                                    (0, 0, 0),
                                ),
                                3,
                            )
                            clavier.lacher_tout()
                            souris.lacher_tout()
                            self.actualise_dimensions()

                        case "ajouter":
                            temps = MenuEntreText.main(
                                Souris(),
                                Clavier(),
                                screen,
                                assembleur.cadre(
                                    (410, 187), (100, 100, 100), (130, 130, 130), 5
                                ),
                                400,
                                self.langue,
                                self.traduction[self.langue]["menu"][1],
                                10,
                                "0123456789"
                                + "abcdefghijklmnopqrstuvwxyz"
                                + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                + "._- ",
                                "whitelist",
                            )
                            souris.lacher_tout()
                            clavier.lacher_tout()
                            self.actualise_dimensions()

                            while temps and (
                                os.path.exists(
                                    self.lien_save + "/" + temps + "/info.json"
                                )
                            ):
                                PopUp.main(
                                    Clavier(),
                                    Souris(),
                                    (
                                        screen.get_width() // 2 - 360 // 2,
                                        screen.get_height() // 2 - 150,
                                    ),
                                    place_texte_in_texture(
                                        assembleur.bouton1((6, 0)),
                                        self.traduction[self.langue]["menu"][0],
                                        pygame.font.Font(None, 50),
                                        (225, 225, 225),
                                    ),
                                    3,
                                )
                                temps = MenuEntreText.main(
                                    Souris(),
                                    Clavier(),
                                    screen,
                                    assembleur.cadre(
                                        (410, 187), (100, 100, 100), (130, 130, 130), 5
                                    ),
                                    400,
                                    self.langue,
                                    self.traduction[self.langue]["menu"][1],
                                    10,
                                    "0123456789"
                                    + "abcdefghijklmnopqrstuvwxyz"
                                    + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                    + "._- ",
                                    "whitelist",
                                    temps,
                                )
                                souris.lacher_tout()
                                clavier.lacher_tout()
                                self.actualise_dimensions()

                            if temps:
                                return "lien", temps
        if souris.get_pression(1) == "vien_lacher":
            self.barscroll.desactiver()
        return "rien", None

    def afficher(self):
        """Affiche le menu"""
        self.titre.afficher()
        self.en_tete.afficher()
        self.surfaces_save.fill((50, 50, 50))
        for save_ in self.save:
            save_.afficher((0, self.decalle), self.surfaces_save)
        screen.blit(self.surfaces_save, self.zone_save.get_pos())
        for bouton in self.bouton:
            bouton.afficher()
        self.barscroll.afficher()
        pygame.display.flip()

    @staticmethod
    def main(
        souris: Souris, clavier: Clavier, lien_save: str, mode: str, langue: str
    ) -> str:
        """Fonction principale"""

        menu = MenuSave(lien_save, mode, langue)
        while True:
            event = actualise_event(clavier, souris)
            action, valeur = menu.actualise(souris, clavier)
            if clavier.get_pression(pygame.K_ESCAPE) == "vien_presser":
                return "retour"
            if clavier.get_pression(pygame.K_F11) == "vien_presser":
                change_fullscreen()
                event.add("redimentione")
            if "quitter" in event:
                return "retour", None
            if "redimentione" in event:
                menu.actualise_dimensions()
            if action == "action":
                if valeur == "retour":
                    return "retour", None
            elif action == "lien":
                return "lien", valeur
            screen.fill((0, 0, 0))
            menu.afficher()


def charge_save(lien_save) -> list[Save]:
    """Actualise les sauvegardes dans le fichier"""

    list_dossier = os.listdir(lien_save)
    list_potentiel = []
    list_save: list[Save] = []

    for dossier in list_dossier:
        # os.path.isdir(self.lien_save + dir)
        # print(dossier)
        if os.path.exists(lien_save + "/" + dossier + "/info.json"):
            list_potentiel.append(dossier)
    for dossier in list_potentiel:
        info = save.load_json(lien_save + "/" + dossier + "/info.json")
        list_save.append(Save.convert_from_dict(info))
    # print(list_save)
    return list_save


def place_save(liste_save: list[Save]):
    """Place les sauvegardes dans l'ordre"""
    liste_save.sort()
    for i, save_ in enumerate(liste_save):
        save_.set_pos((0, 50 * i))


def adition_tuple(tuple1: tuple[int], tuple2: tuple[int]) -> tuple[int]:
    """Additionne deux tuple"""
    return tuple(a + b for a, b in zip(tuple1, tuple2))


def convertir_temps(seconde: int) -> str:
    """Convertit le temps en str"""
    heure = seconde // 3600
    minute = (seconde % 3600) // 60
    seconde = seconde % 60
    sorti = ""
    if heure:
        sorti += f"{heure}h "
    if minute:
        sorti += f"{minute}m "
    if seconde:
        sorti += f"{seconde}s "
    if not sorti:
        sorti = "0s"
    return sorti[:-1]


def convertir_date(date: time.struct_time) -> str:
    """Convertit la date en str"""
    return (
        f"{date.tm_mday}/{date.tm_mon}/{date.tm_year}"
        + f" {date.tm_hour}:{date.tm_min}"
    )


def ajoute_save(lien_save: str, info: dict[str, any]):
    """Ajoute une sauvegarde"""
    save.save_json(lien_save + "/" + info["name"] + "/info.json", info)
