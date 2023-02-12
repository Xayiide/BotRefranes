import http.client as hc
from bs4 import BeautifulSoup as bs


class Scraper:
    conn     = None
    dominio  = None
    ruta     = None
    listado  = None
    busqueda = None

    def __init__(self, dominio, ruta, listado, busqueda):
        self.dominio  = dominio
        self.ruta     = ruta
        self.listado  = listado
        self.busqueda = busqueda

    def connect(self, dominio):
        self.conn = hc.HTTPSConnection(dominio)

    def GET(self, resource):
        # TODO: manejo de errores
        # Comprobar si la conexión sirve
        self.conn.request("GET", resource)
        resp = self.conn.getresponse()

        sopa = bs(resp.read(), 'html.parser')
        return sopa
    
    def retrieveIndex(self, sopa):
        return sopa.find('ol', {'id':'menu_az'})
    
    def retrieveRefranes(self, sopa):
        return [refran.text for refran in sopa.find('ol', {'id':'lista_az'}).find_all('li')]

    def parseRefranero(self):
        refranero = list()
        reachedz  = False
        query     = self.listado + "{}"
        ruta      = self.ruta + "{}"

        self.connect(self.dominio)

        sopa     = self.GET(ruta.format(query.format("")))
        letras   = self.retrieveIndex(sopa)
        refranes = self.retrieveRefranes(sopa)
        actual   = letras.find('a', {'class':'activo'})

        for refran in refranes:
            refranero.append(refran)

        sig   = letras.findNext('a').findNext('a')
        query = sig.get('href')

        while (reachedz == False):
            sopa = self.GET(ruta.format(query))
            letras = self.retrieveIndex(sopa)
            refranes = self.retrieveRefranes(sopa)
            actual = letras.find('a', {'class':'activo'})

            for refran in refranes:
                refranero.append(refran)
            
            if (actual.text == 'Z'):
                reachedz = True
            else:
                sig   = actual.findNext('a')
                query = sig.get('href')
        
        return refranero