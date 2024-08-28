from game.inventaire.item import Item


class Inventaire:
    """Classe de base pour l'inventaire"""

    def __init__(self, max_quantite: int):
        self.max_quantite = max_quantite
        self.items: list[Item] = []

    def ajoute_item(self, item: Item):
        """Ajoute un item à l'inventaire"""
        for items in self.items:
            if items == item:
                items.tranfere(item.quantite)
                return True
        if item.quantite > 0:
            if len(self.items) >= self.max_quantite:
                return False
            self.items.append(item)
            return True
        return False

    def echanger(self, indice1: int, indice2: int):
        """Échange deux items"""
        if indice1 < 0 or indice1 >= len(self.items):
            raise IndexError("indice1 hors de la liste")
        if indice2 < 0 or indice2 >= len(self.items):
            raise IndexError("indice2 hors de la liste")
        self.items[indice1], self.items[indice2] = (
            self.items[indice2],
            self.items[indice1],
        )

    def remplacer(self, item: Item, indice: int):
        """Remplace un item et retourne l'ancien"""
        if indice < 0 or indice >= len(self.items):
            raise IndexError("indice hors de la liste")
        ancien_item = self.items[indice]
        self.items[indice] = item
        return ancien_item

    def supprime(self, indice: int):
        """Supprime un item"""

        if indice < 0 or indice >= len(self.items):
            raise IndexError("indice hors de la liste")
        return self.items.pop(indice)

    def get_item(self, indice: int):
        """Retourne un item"""
        if indice < 0 or indice >= len(self.items):
            raise IndexError("indice hors de la liste")
        return self.items[indice]

    def get_taille(self):
        """Retourne la taille de l'inventaire"""
        return len(self.items)

    def change_taille(self, taille: int):
        """Change la taille de l'inventaire"""
        if taille < len(self.items):
            return False
        self.max_quantite = taille
        return True
