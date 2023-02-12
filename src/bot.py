import config as cfg
import util   as u
import scrap
import refranero as rfn

import telegram
from telegram     import Update, ForceReply
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import ContextTypes, Application, filters



class Bot:
    config    = None
    app       = None
    refranero = None

    def __init__(self, cfgfn):
        self.config = cfg.Config(cfgfn)
        self.app = Application.builder().token(self.config.getToken()).build()
        self.refranero = rfn.Refranero()
        self.addCmdHandlers()
        self.addMsgHandlers()
        self.retrieveRefranes()
        print("Bot corriendo.")

    def addCmdHandlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("diRefran", self.diRefran))

    def addMsgHandlers(self):
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                            self.handleMsg))

    def run(self):
        self.app.run_polling()
        # Para aquí por algún motivo
        print("\nBot terminado.")

    def retrieveRefranes(self):
        if alreadyScraped(self.config.getRefFile()):
            print("Existen refranes en fichero. No se escrapea.")
            self.refranero.loadFromFile(self.config.getRefFile())
        else:
            dominio  = self.config.getUrls('dominio')
            ruta     = self.config.getUrls('ruta')
            listado  = self.config.getUrls('listado')
            busqueda = self.config.getUrls('busqueda')
            self.sc  = scrap.Scraper(dominio, ruta, listado, busqueda)

            print("No existen refranes en ficheros. Escrapeando...")
            self.refranero.load(sc.parseRefranero())
            print("Escrapeo finalizado.")


    async def handleMsg(self,
                   update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg  = update.message
        chat = chatType(update)

        if chat == "private":
            await msg.reply_text("Sólo comandos en chats privados")
        elif chat == "group":
            pass # TODO decidir qué hacer aquí

    async def echo(self,
                   update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(update.message.text)
        userid   = update.message.chat.id
        username = update.message.chat.username
        text     = update.message.text
        u.screen(userid, username, text)

    async def start(self,
                    update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def diRefran(self,
                    update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg  = update.message
        chat = chatType(update)

        if chat == "group":
            await msg.reply_text(self.refranero.refranAleatorio())


def alreadyScraped(file):
    try:
        with open(file, "r") as f:
            if len(f.readlines()) < 1627:
                return False
            return True
    except:
        return False

def chatType(update):
    msg = update.message
    try:
        chatType = msg.chat.type

        if chatType == telegram.constants.ChatType.CHANNEL:
            return "channel"
        else:
            sender = msg.from_user
            userid = sender.id
            uname  = sender.username
            if chatType == telegram.constants.ChatType.PRIVATE:
                u.screen(userid, uname, msg.text)
                return "private"
            else: # GROUP or SUPERGROUP
                u.screen(userid, uname, msg.text, msg.chat.id)
                return "group"

    except Exception as e:
        print("Error - Bot::isPrivateChat")
        print(str(e))
