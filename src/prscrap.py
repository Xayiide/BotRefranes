from bs4 import BeautifulSoup as bs
import config as cfg
import scrap as scp


CONFIG = "config.json"


def main():
    cf = cfg.Config(CONFIG)
    sc = scp.Scraper()

    base  = cf.getUrls('base') + cf.getUrls('medio')
    lista = cf.getUrls('listado') + '?letra='


    sc.connect(base)
    # 1. Pedir la letra A, que siempre va a ser la primera
    #   1.1. Descargar todos los refranes de la A
    #   1.2. Descargar el índice
    #   1.3. Ir a la siguiente letra del índice



    for i in ['A', 'B', 'C']:
        fn = '__refranes/' + i + '.txt'
        refranes = sc.selectRefranes(sc.get(lista + i))
        with open(fn, "w") as f:
            for refran in refranes:
                f.write(refran + "\n")

    #print(refranes)


if __name__ == '__main__':
    main()