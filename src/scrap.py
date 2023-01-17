import http.client as hc
from bs4 import BeautifulSoup as bs


class Scraper:
    conn = None

    def __init__(self):
        pass

    def connect(self, base):
        self.conn = hc.HTTPSConnection(base)

    def get(self, resource):
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