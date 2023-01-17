import config as cfg
import util   as u
import telegram
from telegram     import Update, ForceReply
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import ContextTypes, Application, filters



class Bot:
    app     = None
    config  = None

    def __init__(self, cfgfn):
        self.config = cfg.Config(cfgfn)
        self.app = Application.builder().token(self.config.getToken()).build()
        self.addCmdHandlers()
        self.addMsgHandlers()
        print("Bot corriendo")

    def addCmdHandlers(self):
        self.app.add_handler(CommandHandler("start", self.start))

    def addMsgHandlers(self):
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                            self.handleMsg))
    def run(self):
        self.app.run_polling()
        # Para aquí por algún motivo
        print("\nBot terminado")

    async def handleMsg(self,
                   update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg = update.message
        try:
            chatType = msg.chat.type
            
            if chatType == telegram.constants.ChatType.CHANNEL:
                pass
            else:
                sender = msg.from_user
                userid = sender.id
                username = sender.username
                if chatType == telegram.constants.ChatType.PRIVATE:
                    u.screen(userid, username, msg.text)
                    await msg.reply_text("Sólo comandos en chats privados")
                else: # GROUP or SUPERGROUP
                    u.screen(userid, username, msg.text, msg.chat.id)
                    resp = "Eres el usuario " + str(userid)
                    if (username != None):
                        resp += " y tu @ es " + username
                    else:
                        resp += " y no tienes @"
                    await msg.reply_text(resp)
        except Exception as e:
            print("Error - Bot::handleMsg")
            print(str(e))

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
