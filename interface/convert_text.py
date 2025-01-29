# oui je sais j'aurais pu faire une classe mais je voulais pas 
# car flemme et je pense pas que ça soit nécessaire 
# et en vrai avec python c'est un peu la même chose selon moi 

# a optimser un jour (surtout la fonction transforme)
remplace : dict[str,any] = {}


def transforme( text: str)->str:
    for cle in remplace:
        text = text.replace(cle, remplace[cle])
    return text

def add_dico_and_balise( dico: dict):
    for clee, valeur in dico[1].items():
        remplace["{{"+clee+"}}"] = valeur

def add_dico( dico: dict):
    for clee, valeur in dico.items():
        remplace[clee] = valeur

def add_value( clee: str, valeur: any):
    remplace[clee] = valeur

def add_value_and_balise( clee: str, valeur: any):
    remplace["{{"+clee+"}}"] = valeur

def get_remplace():
    return remplace