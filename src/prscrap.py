from bs4 import BeautifulSoup as bs
import config as cfg
import scrap as scp


CONFIG = "config.json"

def guardaRefranes(fichero, refranes):
    with open(fichero, "w") as f:
        for refran in refranes:
            f.write(refran + "\n")

def main():
    cf = cfg.Config(CONFIG)

    dominio  = cf.getUrls('dominio')
    ruta     = cf.getUrls('ruta')
    listado  = cf.getUrls('listado')
    busqueda = cf.getUrls('busqueda')

    sc = scp.Scraper(dominio, ruta, listado, busqueda)

    refranes = sc.parseRefranero()
    guardaRefranes(cf.getRefFile(), refranes)

if __name__ == '__main__':
    main()