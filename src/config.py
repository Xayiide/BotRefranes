import json

class Config:
    token    = None
    admins   = None
    cvcurls  = None
    rffile   = None

    def __init__(self, cfgfn):
        self.readConfig(cfgfn)
        print("Lectura de la configuración finalizada")

    def readConfig(self, cfgfn):
        with open(cfgfn, 'r') as fd:
            config       = json.load(fd)
            self.token   = self.readToken(config)
            self.admins  = self.readAdmins(config)
            self.rffile  = self.readRffile(config)
            self.cvcurls = self.readUrls(config)

    def readToken(self, cfg):
        with open (cfg['tkfile'], 'r') as f:
            return f.readline().strip('\n')

    def readAdmins(self, cfg):
        return [admin for admin in cfg['bot']['admins']]

    def readRffile(self, cfg):
        return cfg['rffile']

    def readUrls(self, cfg):
        ret  = {}
        urls = cfg['scraper']['urls']
        ret['dominio']  = urls['dominio']
        ret['ruta']     = urls['ruta']
        ret['listado']  = urls['listado']
        ret['busqueda'] = urls['busqueda']
        return ret

    def getToken(self):
        return self.token

    def isAdmin(self, userId):
        return (userId in self.admins)

    def getRefFile(self):
        return self.rffile

    def getUrls(self, url=None):
        if url == None:
            return self.cvcurls
        else:
            try:
                return self.cvcurls[url]
            except:
                print("No existe la URL solicitada")