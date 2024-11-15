from game.map.composant import Composant,Sol
class Module:
    def __init__(self, position, taille):
        self.position = position
        self.taille = taille
        self.composants:list[Composant] = []
        self.sol:list[Sol] = []
        self.genere_comp
    
    def get_comp(self):
        """Retourne les composants du module"""
        return self.composants
    
    def get_sol(self):
        """Retourne le sol du module"""
        return self.sol
    
    def deplace_comp(self,position:tuple[int,int]):
        """Déplace les composants du module"""
        for composant in self.composants:
            composant.set_pos((composant.get_pos()[0]+position[0],composant.get_pos()[1]+position[1]))

    def genere_comp(self):
        """Génère les composants du module"""
        pass

class SousModule(Module):
    def __init__(self, position, taille,composants,sol):
        self.ancien_composants = composants
        self.ancien_sol = sol
        super().__init__(position, taille)
    