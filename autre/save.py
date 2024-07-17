"""
ce module contien des fonction pour sauvegarder ou charger des fichiers json
"""

import os
import json


def indent_map(lien, indentation: int):
    """indente un json"""
    with open(lien, encoding="utf8") as file:
        contenu = json.load(file)
        file = open(lien, "w", encoding="utf8")
        json.dump(contenu, file, indent=indentation)


def load_json(lien: str):
    """charge un json"""
    with open(lien, encoding="utf8") as file:
        contenu = json.load(file)
    return contenu


def save_json(lien: str, contenu):
    """crée un json

    Args:
        lien (str): est parcour de ficher est le nom.extention du ficher
        contenu (_type_): est le contenu du fiche
    """
    with open(lien, "w", encoding="utf8") as file:
        json.dump(contenu, file, indent=1)
        # file.close()


def force_input_y_or_n(texte: str):
    """cette foction va forcé l'utilisateur à entré y ou n pour sortir
    cette fonction est une fonction homme machine

    Args:
        texte (str): est le texte qui sera affiché au input()

    Returns:
        bool: dépend si l'utilisateur à répond y pour True et n pour False
    """
    repondu = False
    while not repondu:
        reponse = input(texte).lower().strip()
        if reponse == "y":
            repondu = True
            sortie = True
        elif reponse == "n":
            repondu = True
            sortie = False
        else:
            print("error inconnu")
    return sortie


def choisir_ficher(chemin: str):
    """permet de choisir un fichier dans un dosier
    si l'utilisateur annule l'action il renvoie l'information
    sinon il revoie le nom de fichier choisi

    Args:
        chemin (str): est le chemin du dossier

    Returns:
        str : si l'utilisateur anule l'action il va revoier anulation
               sinon il revoi le nom de fichier choisi
    """
    sortie = None
    dossier = os.listdir(chemin)
    stop = False
    list_str_index = []
    for index, _ in enumerate(dossier):
        list_str_index.append(str(index))
    while not stop:
        for index, ficher in enumerate(dossier):
            print(str(index) + ":", ficher)

        reponse = input("marque le nombre pour selectioner fichier ")
        if reponse in list_str_index and force_input_y_or_n(
            f"voulez vous la save {reponse} qui correpond à "
            + f"{dossier[int(reponse)]} y/n "
        ):
            sortie = dossier[int(reponse)]
            stop = True
        elif reponse in ("stop", "fin"):
            sortie = "anulation"
            stop = True
    return sortie


if __name__ == "main":
    pass
