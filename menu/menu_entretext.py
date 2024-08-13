import pygame

from interface.actualisation_pygame import change_fullscreen
from interface.graphique import (
    ObjetGraphique,
    Image,
    gener_texture,
    place_texte_in_texture,
    decoupe_texte,
)
from interface.bouton import BoutonText
from interface.class_clavier import Clavier, Souris

from textures import assembleur


class MenuEntreText:
    """Menu pour entrer du texte

    agrs:
        fenetre: pygame.Surface
        largeur: int
        titre: str
        max_len_text: int
        liste_caractere: str
        mode_liste: str = "whitelist" ou "blacklist"
    """

    langue_bouton = {
        "fr": ["valider", "vider", "anuler"],
        "en": ["validate", "clear", "cancel"],
    }

    def __init__(
        self,
        fenetre: pygame.Surface | str | Image,
        fond: pygame.Surface | str | Image,
        largeur: int,
        titre: str,
        max_len_text: int,
        langue: str,
        liste_caractere: str,
        mode_liste: str = "whitelist",
        texte_de_base: str = "",
    ):
        self.fenetre = fenetre
        self.fond = Image(fond)
        self.max_len_text = max_len_text
        self.liste_caractere = liste_caractere
        self.mode_liste = mode_liste
        self.largeur = largeur

        # titre
        police_titre = pygame.font.Font(None, 36)
        taille_titre = (
            largeur,
            len(decoupe_texte(titre, largeur, police_titre))
            * police_titre.get_linesize(),
        )
        self.titre = ObjetGraphique(
            (0, 0), [gener_texture(taille_titre, (0, 0, 0, 0))], taille_titre
        )
        self.titre.texture[0].texture = place_texte_in_texture(
            self.titre.texture[0].texture, titre, police_titre, (255, 255, 255)
        )

        # zone de texte
        self.texte = texte_de_base
        self.police_texte = pygame.font.Font(None, 36)
        # print(self.police_texte.get_linesize())
        hauteur_text = 50
        taille_texte = (largeur - 20, hauteur_text)

        self.image_texte_vide = assembleur.cadre(
            taille_texte, (150, 150, 150), (120, 120, 120), 5
        )
        self.obj_texte = ObjetGraphique(
            (0, 0),
            [self.image_texte_vide],
            taille_texte,
        )
        self.change_text(texte_de_base)

        # bouton
        police_bouton = pygame.font.Font(None, 25)
        self.bouton: list[BoutonText] = []
        for bouton in self.langue_bouton[langue]:
            self.bouton.append(
                BoutonText(
                    (0, 0),
                    [assembleur.bouton2(100, i) for i in (1, 2)],
                    (100, 50),
                    bouton,
                    (0, 0, 0),
                    police_bouton,
                    data=bouton,
                )
            )

    def actualise_dimensions(self):
        """actualise les dimensions"""
        self.fond.ancre = (
            -self.fenetre.get_width() // 2 + self.fond.get_size()[0] // 2,
            -self.fenetre.get_height() // 2 + self.fond.get_size()[1] // 2,
        )
        hauteur_total = (
            self.fenetre.get_height() // 2
            - (
                10
                + self.titre.get_size()[1]
                + 20
                + self.obj_texte.get_size()[1]
                + 20
                + self.bouton[0].get_size()[1]
                + 10
            )
            // 2
        )
        # print((
        #     + self.titre.get_size()[1]
        #     + 20
        #     + self.obj_texte.get_size()[1]
        #     + 20
        #     + self.bouton[0].get_size()[1]
        # ))

        self.titre.set_pos(
            (
                self.fenetre.get_width() // 2 - self.titre.get_size()[0] // 2,
                hauteur_total + 10,
            )
        )
        self.obj_texte.set_pos(
            (
                self.fenetre.get_width() // 2 - self.obj_texte.get_size()[0] // 2,
                self.titre.get_size()[1] + self.titre.get_pos()[1] + 20,
            )
        )

        distance_bouton = (
            self.largeur - sum([bouton.get_size()[0] for bouton in self.bouton])
        ) // (len(self.bouton) + 1)

        for i, bouton in enumerate(self.bouton):
            bouton.set_pos(
                (
                    self.fenetre.get_width() // 2
                    + self.largeur // 2
                    - distance_bouton * (i + 1)
                    - sum([bouton.get_size()[0] for bouton in self.bouton[: i + 1]]),
                    self.obj_texte.get_pos()[1] + self.obj_texte.get_size()[1] + 20,
                )
            )

    def hover(self, pos_souris: tuple[int, int]):
        """gere le hover"""
        for bouton in self.bouton:
            if bouton.point_dans_objet(pos_souris):
                bouton.animation = 1
            else:
                bouton.animation = 0

    def click(self, souris: Souris):
        """gere le click"""
        if souris.get_pression(1) == "vien_presser":
            for bouton in self.bouton:
                if bouton.point_dans_objet(souris.get_pos()):
                    print(bouton.data)
                    match bouton.data:
                        case "valider":
                            return self.texte
                        case "vider":
                            self.change_text("")
                        case "anuler":
                            return ""
        return None

    def afficher(self):
        """affiche le menu"""
        self.fond.afficher((0, 0), self.fenetre)
        self.titre.afficher(surface=self.fenetre)
        self.obj_texte.afficher(surface=self.fenetre)
        for bouton in self.bouton:
            bouton.afficher(surface=self.fenetre)

    def change_text(self, texte: str):
        """change le texte"""
        self.texte = texte
        self.obj_texte.texture[0].texture = place_texte_in_texture(
            self.image_texte_vide.copy(), texte, self.police_texte, (0, 0, 0)
        )

    def actualise_event(self, souris: Souris, clavier: Clavier) -> set:
        """actualise les événement"""
        # pylint: disable=no-member
        event_autre = set()
        souris.actualise_all_clique()
        clavier.update_all_key()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_autre.add("quitter")
            elif event.type in (
                pygame.VIDEORESIZE,
                pygame.WINDOWSIZECHANGED,
            ):
                event_autre.add("redimentione")

            elif event.type == pygame.KEYDOWN:
                clavier.set_pression(event.key, "vien_presser")
                if event.key == pygame.K_BACKSPACE and len(self.texte) > 0:
                    self.change_text(self.texte[:-1])
                elif (
                    self.mode_liste == "whitelist"
                    and event.unicode in self.liste_caractere
                ):
                    self.change_text(self.texte + event.unicode)
                elif (
                    self.mode_liste == "blacklist"
                ) and event.unicode not in self.liste_caractere:
                    self.change_text(self.texte + event.unicode)
            elif event.type == pygame.KEYUP:
                clavier.set_pression(event.key, "vien_lacher")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                souris.set_pression(event.button, "vien_presser")

            elif event.type == pygame.MOUSEBUTTONUP:
                souris.set_pression(event.button, "vien_lacher")
            # if event.type not in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
            #     print(event)

        souris.update_pos()
        return event_autre

    def play(self, souris: Souris):
        """joue le menu"""
        self.hover(souris.get_pos())
        return self.click(souris)

    @staticmethod
    def main(
        souris: Souris,
        clavier: Clavier,
        fenetre: pygame.Surface | str | Image,
        fond: pygame.Surface | str | Image,
        largeur: int,
        langue: str,
        titre: str,
        max_len_text: int,
        liste_caractere: str,
        mode_liste: str = "whitelist",
        texte_de_base: str = "",
    ) -> str:
        """fonction principale"""
        # pylint: disable=no-member
        menu = MenuEntreText(
            fenetre,
            fond,
            largeur,
            titre,
            max_len_text,
            langue,
            liste_caractere,
            mode_liste,
            texte_de_base,
        )
        menu.actualise_dimensions()
        encours = True

        while encours:
            event = menu.actualise_event(souris, clavier)
            temp = menu.play(souris)
            if (
                "quitter" in event
                or clavier.get_pression(pygame.K_ESCAPE) == "vien_presser"
            ):
                return ""
            if clavier.get_pression(pygame.K_F11) == "vien_presser":
                change_fullscreen()
                event.add("redimentione")
            if "redimentione" in event:
                menu.actualise_dimensions()
            if isinstance(temp, str):
                return temp
            fenetre.fill((125, 125, 125))
            menu.afficher()
            pygame.display.update()
