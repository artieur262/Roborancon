import time
import pygame
from interface.graphique import screen
from game.entity.playeur import Playeur
from game.inventaire.item import Item, Membre, MembreSens, Corps
from autre import save

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
        [100, 100],
        (64, 64),
        {"vie": 100, "force": 10, "vitesse_min": 3, "vitesse_max": 6},
    )

    playeur.membre_equipe["corps"] = corps
    playeur.membre_equipe["tete"] = tete
    playeur.membre_equipe["bras_droit"] = bras_d
    playeur.membre_equipe["jambe_droit"] = jambe_d
    playeur.membre_equipe["bras_gauche"] = bras_g
    playeur.membre_equipe["jambe_gauche"] = jambe_g
    playeur.calcul_stats()
    playeur.actualise_texture()
    # print(playeur.coordonnee)
    # print(playeur.convert_to_dict()["coordonnee"])
    save.save_json("teste/playeur.json", playeur.convert_to_dict())
    

main()
