remplace : dict[str,any] = {}


def transforme( text: str)->str:
    for cle in remplace:
        text = text.replace(cle, remplace[cle])
    return text

def actualise_control( dict_control: dict):
    for clee, valeur in dict_control[1].items():
        remplace["{{"+clee+"}}"] = valeur

def get_remplace():
    return remplace