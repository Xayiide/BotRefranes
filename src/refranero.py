
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
        return self.refranes[0]