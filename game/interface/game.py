import pygame

from game.entity.playeur import Playeur  # [import-error]
from game.entity.entity import Entity
from interface.class_clavier import Clavier, Souris
from interface.graphique import screen


class Game:
    def __init__(
        self,
        playeur: Playeur,
        clavier: Clavier,
        souris: Souris,
        controls: dict[str, int],
    ):
        self.playeur = playeur
        self.clavier = clavier
        self.souris = souris
        self.controls = controls
