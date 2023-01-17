import bot

from telegram.ext import Application
from telegram.ext import CommandHandler, MessageHandler, filters

CONFIG = "config.json"

def main():
    paremias = bot.Bot(CONFIG)
    paremias.run()

if __name__ == '__main__':
    main()
