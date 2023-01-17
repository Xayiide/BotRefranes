from bs4 import BeautifulSoup as bs
import config as cfg
import scrap as scp


CONFIG = "config.json"

def guardaRefranes(fichero, refranes):
    print("La letra {} tiene {} refr".format(fichero, len(refranes)), end="")
    if (len(refranes) == 1):
        print("án.")
    else:
        print("anes.")

    fn = '__refranes/{}.txt'.format(fichero)
    with open(fn, "w") as f:
        for refran in refranes:
            f.write(refran + "\n")

def main():
    cf    = cfg.Config(CONFIG)
    sc    = scp.Scraper()

    ruta  = cf.getUrls('ruta') + "{}" # /lengua/refranes/{}
    done  = False
    query = cf.getUrls('listado') + "{}" # llamaremos query a "listado.aspx?letra=X"

    sc.connect(cf.getUrls('dominio'))
    
    sopa     = sc.get(ruta.format(query.format(""))) #  /lengua/refranes/listado.aspx
    letras   = sc.retrieveIndex(sopa)
    refranes = sc.retrieveRefranes(sopa)
    actual   = letras.find('a', {'class':'activo'}) 

    guardaRefranes(actual.text, refranes)

    sig   = letras.findNext('a').findNext('a')
    query = sig.get('href') # listado.aspx?letra=B

    while (done == False):
        sopa     = sc.get(ruta.format(query))
        letras   = sc.retrieveIndex(sopa) # Guardamos el índice
        refranes = sc.retrieveRefranes(sopa) # Guardamos los refranes
        actual   = letras.find('a', {'class':'activo'})

        guardaRefranes(actual.text, refranes)

        if actual.text == 'Z':
            done = True
        else:
            sig   = actual.findNext('a')
            query = sig.get('href') # listado.aspx? = letra = X


if __name__ == '__main__':
    main()