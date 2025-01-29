from interface.graphique import Image, ObjetGraphique, charge_png_dans_dossier, LienSpritesheet


class Item:
    def __init__(
        self, nom: str, description: str, icone: str, quantite: int, max_quantite: int
    ):
        self.nom = nom
        self.description = description
        self.icone_lien = icone
        self.icone = Image(icone)
        self.quantite = quantite
        self.max_quantite = max_quantite

    def ajoute_quantite(self, quantite: int):
        """Ajoute ou retire de la quantité
        return False quand l'opération est impossible
        l'opération est impossible quand la quantité est supérieur à max_quantite ou inférieur à 0
        """

        if self.quantite + quantite > self.max_quantite:
            return False
        if self.quantite + quantite < 0:
            return False
        self.quantite += quantite

    def set_quantite(self, quantite):
        """set la quantité"""
        self.quantite = quantite

    def tranfere(self, item: "Item"):
        """transfère une quantité d'item"""
        quantite = item.quantite
        if self.quantite + quantite > self.max_quantite:
            quantite = self.max_quantite - self.quantite
        self.ajoute_quantite(quantite)
        item.ajoute_quantite(-quantite)

    def divise(self, quantite: int):
        """Divise un item en deux"""
        if quantite >= self.quantite:
            return None
        self.quantite -= quantite
        return Item(
            self.nom, self.description, self.icone_lien, quantite, self.max_quantite
        )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Item):
            return value.nom == self.nom
        return False
    def convert_to_dict(self):
        return {
            "type": "item",
            "nom": self.nom,
            "description": self.description,
            "icone": self.icone_lien,
            "quantite": self.quantite,
            "max_quantite": self.max_quantite,
        }

    @staticmethod
    def genere_self(data: dict):
        return Item(
            data["nom"],
            data["description"],
            data["icone"],
            data["quantite"],
            data["max_quantite"],
        )

class Membre(Item):
    """Classe de base pour les membres

    args:
        stats (dict): stats du membre
        texture (str): lien du dossier contenant les textures

    """

    def __init__(
        self,
        nom: str,
        description: str,
        icone: str,
        texture: dict[str, str|tuple[int,int]|None],
        quantite: int,
        max_quantite: int,
        stats: dict,
    ):
        super().__init__(nom, description, icone, quantite, max_quantite)
        self.stats = stats
        self.texture_lien = texture
        self.charge_texture()
        self.etat = "normal"

    def charge_texture(self):
        """charge les textures"""
        if isinstance(self.texture_lien, list):
            raise ValueError("les textures doivent être un dictionnaire")
        else:
            self.texture = LienSpritesheet(self.texture_lien["lien"], self.texture_lien["taille"]).decoupe()

    def get_etat(self):
        """retourne l'état"""
        return self.etat

    def get_texture(self, index: int) -> Image:
        """retourne la texture à l'index"""
        return self.texture[index]

    def get_stat(self, stat: str):
        """retourne la valeur de la stat"""
        return self.stats[stat]

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, Membre)
            and super().__eq__(value)
            and value.stats == self.stats
        )
    def convert_to_dict(self):
        sorti= {
            **super().convert_to_dict(),
            "stats": self.stats,
            "texture": self.texture_lien,
        }
        sorti["type"] = "membre"
        return sorti
    @staticmethod
    def genere_self(data: dict):
        return Membre(
            data["nom"],
            data["description"],
            data["icone"],
            data["texture"],
            data["quantite"],
            data["max_quantite"],
            data["stats"],
        )
class MembreSens(Membre):
    """Classe pour les membres avec sens

    agrs:
        textures: dict[str, list[str]] dictionnaire des liens des textures
        sens: str sens du membre
    """

    def __init__(
        self,
        nom: str,
        description: str,
        icone: str,
        texture: dict[list[str]|dict[str, str|tuple[int,int]|None]],
        quantite: int,
        max_quantite: int,
        stats: dict,
        sens: str,
    ):
        self.sens = sens
        super().__init__(
            nom,
            description,
            icone,
            texture,
            quantite,
            max_quantite,
            stats,
        )

    def charge_texture(self):
        """charge les textures"""
        if isinstance(self.texture_lien, list):
            raise ValueError("les textures doivent être un dictionnaire")
        else:
            self.texture = LienSpritesheet(self.texture_lien[self.sens]["lien"], self.texture_lien[self.sens]["taille"]).decoupe()


    def get_sens(self):
        """retourne le sens"""
        return self.sens

    def __eq__(self, value: object) -> bool:
        return isinstance(value, MembreSens) and super().__eq__(value)

    def convert_to_dict(self):
        sorti= super().convert_to_dict()
        sorti["sens"] = self.sens
        sorti["type"] = "membre_sens"
        return sorti


    @staticmethod
    def genere_self(data: dict):
        return MembreSens(
            data["nom"],
            data["description"],
            data["icone"],
            data["texture"],
            data["quantite"],
            data["max_quantite"],
            data["stats"],
            data["sens"],
        )
class Corps(Membre):
    """Classe pour les corps

    agrs:
        membre_emplacement: dict[str, tuple[int, int]]
            dictionnaire des emplacements des membres
            clé: nom de l'emplacement
            valeur: list de tuple de 2 int (x, y) position de l'emplacement
        ordre_affichage: list[str] ordre d'affichage des membres
    """

    def __init__(
        self,
        nom: str,
        description: str,
        icone: str,
        texture: list[str]|dict[str, str|tuple[int,int]|None],
        quantite: int,
        max_quantite: int,
        stats: dict,
        membre_emplacement: dict[str, list[tuple[int, int]]],
        ordre_affichage: list[str],
    ):
        super().__init__(
            nom, description, icone, texture, quantite, max_quantite, stats
        )
        self.membre_emplacement = membre_emplacement
        self.ordre_affichage = ordre_affichage

    def get_emplacement(self, emplacement: str):
        """retourne la position de l'emplacement"""
        return self.membre_emplacement[emplacement]

    def get_ordre_affichage(self):
        """retourne l'ordre d'affichage"""
        return self.ordre_affichage

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, Corps)
            and super().__eq__(value)
            and value.membre_emplacement == self.membre_emplacement
            and value.ordre_affichage == self.ordre_affichage
        )
    

    def convert_to_dict(self):
        sorti= {
            **super().convert_to_dict(),
            "membre_emplacement": self.membre_emplacement,
            "ordre_affichage": self.ordre_affichage,
        }
        sorti["type"] = "corps"
        return sorti


    @staticmethod
    def genere_self(data: dict):
        return Corps(
            data["nom"],
            data["description"],
            data["icone"],
            data["texture"],
            data["quantite"],
            data["max_quantite"],
            data["stats"],
            data["membre_emplacement"],
            data["ordre_affichage"],
        )
    
def genere_item(data: dict):
    if data["type"] == "item":
        return Item.genere_self(data)
    if data["type"] == "membre":
        return Membre.genere_self(data)
    if data["type"] == "membre_sens":
        return MembreSens.genere_self(data)
    if data["type"] == "corps":
        return Corps.genere_self(data)
    else:
        print(data)
        raise ValueError("type inconnu")