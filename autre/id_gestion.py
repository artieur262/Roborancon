all_id={0}
dernière_id = 0
def genere_id() -> int:
    """Génère un id unique"""
    global dernière_id
    dernière_id += 1
    while dernière_id in all_id:
        dernière_id += 1
    ajoute_id(dernière_id)
    return dernière_id

def ajoute_id(id):
    """Ajoute un id"""
    global all_id
    all_id.add(id)

def supprime_id(id):
    """Supprime un id"""
    global all_id
    all_id.remove(id)
