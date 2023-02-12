import random

class Refranero:
    refranes = list()

    def __init__(self):
        pass

    def load(self, refranes):
        self.refranes = refranes

    def loadFromFile(self, file):
        with open(file, "r") as f:
            refranes = f.readlines()
            for refran in refranes:
                self.refranes.append(refran)

    def refranAleatorio(self):
        return random.choice(self.refranes)

    def refranApropiado(self, mensaje):
        pass
        #return self.refranAleatorio()
