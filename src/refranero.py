
class Refranero:
    refranes = set()

    def __init__(self):
        pass
    
    def load(self, refranes):
        self.refranes = refranes

    def loadFromFile(self, file):
        with open(file, "r") as f:
            refranes = f.readlines()
            for refran in refranes:
                self.refranes.add(refran)
    
    def randomRefran(self):
        item = self.refranes.pop()
        self.refranes.update(item)
        return item
    
    def refranApropiado(self, mensaje):
        apropiados = set()
        for palabra in mensaje.split(" "):
            print(palabra)
            return str(self.randomRefran())

        
