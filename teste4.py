from menu.menu_save import MenuSave
from interface.class_clavier import Clavier, Souris

MenuSave.main(Souris(), Clavier(), "user/cat", "sauvegarde", "en")
MenuSave.main(Souris(), Clavier(), "user/cat", "chargement", "fr")
