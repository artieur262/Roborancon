class convert_text:
    remplace : dict = {}
    
    def __init__(self, remplace: dict):
        self.remplace = remplace
    
    def transforme(self, text: str)->str:
        for cle in self.remplace:
            text = text.replace(cle, self.remplace[cle])
        return text

