import time
import pygame
from interface.graphique import screen
from game.entity.playeur import Playeur
from game.inventaire.item import Item, Membre, MembreSens, Corps


# pylint: disable=no-member
def main():
    corps = Corps(
        "corps",
        "j'aime les chatons",
        "textures/entity/playeur/corps/corps0.png",
        "textures/entity/playeur/corps",
        1,
        1,
        {},
        {
            "tete": (0, 0),
            "corps": (0, 0),
            "bras_droit": (0, 0),
            "bras_gauche": (0, 0),
            "jambe_droit": (0, 0),
            "jambe_gauche": (0, 0),
        },
        ["corps", "tete", "bras_droit", "bras_gauche", "jambe_droit", "jambe_gauche"],
    )
    tete = Membre(
        "tete",
        "j'aime les chatons",
        "textures/entity/playeur/tete/tete0.png",
        "textures/entity/playeur/tete/",
        1,
        1,
        {},
    )

    bras_d = MembreSens(
        "bras",
        "j'aime les chatons",
        "textures/entity/playeur/bras d/bras0 d.png",
        {
            sens: f"textures/entity/playeur/bras {lettre}"
            for lettre, sens in zip(("d", "g"), ("droit", "gauche"))
        },
        1,
        1,
        {},
        "droit",
    )
    jambe_d = MembreSens(
        "jambe",
        "j'aime les chatons",
        "textures/entity/playeur/jambe d/jambe0 d.png",
        {
            sens: f"textures/entity/playeur/jambe {lettre}"
            for lettre, sens in zip(("d", "g"), ("droit", "gauche"))
        },
        1,
        1,
        {},
        "droit",
    )
    bras_g = MembreSens(
        "bras",
        "j'aime les chatons",
        "textures/entity/playeur/bras g/bras0 g.png",
        {
            sens: f"textures/entity/playeur/bras {lettre}"
            for lettre, sens in zip(("d", "g"), ("droit", "gauche"))
        },
        1,
        1,
        {},
        "gauche",
    )
    jambe_g = MembreSens(
        "jambe",
        "j'aime les chatons",
        "textures/entity/playeur/jambe g/jambe0 g.png",
        {
            sens: f"textures/entity/playeur/jambe {lettre}"
            for lettre, sens in zip(("d", "g"), ("droit", "gauche"))
        },
        1,
        1,
        {},
        "gauche",
    )
    playeur = Playeur(
        (0, 0),
        (100, 100),
        {"vie": 100, "force": 10, "vitesse": 10},
    )

    playeur.membre_equipe["corps"] = corps
    playeur.membre_equipe["tete"] = tete
    playeur.membre_equipe["bras_droit"] = bras_d
    playeur.membre_equipe["jambe_droit"] = jambe_d
    playeur.membre_equipe["bras_gauche"] = bras_g
    playeur.membre_equipe["jambe_gauche"] = jambe_g
    playeur.calcul_stats()
    playeur.actualise_texture()

    playeur.action = "marche"
    clok = pygame.time.Clock()
    tick = 0
    vitesse = 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playeur.action = "marche" if playeur.action == "rien" else "rien"
                if event.key == pygame.K_r:
                    playeur.set_pos((10, 10))
                if event.key == pygame.K_UP:
                    vitesse += 1
                if event.key == pygame.K_DOWN:
                    vitesse -= 1

        screen.fill((0, 0, 0))
        if tick % 7 == 0:
            playeur.actualise_animation()
            if playeur.action == "marche":

                playeur.add_pos((0, vitesse))
        playeur.afficher((-100, -100))
        pygame.display.flip()
        clok.tick(60)
        tick += 1


main()
