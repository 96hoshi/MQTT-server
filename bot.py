import os
import logging
import time

from sqlalchemy.sql import func
from dotenv import load_dotenv
from telegram import Update, ForceReply, BotCommand, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from database import DBHandler

load_dotenv()

DEBUG = True
TOKEN = os.environ['TOKEN']
bot = Bot(token=TOKEN)
db = DBHandler()
dev = 1 #TODO: rimuovere var globale e sostituire con device dell'utente

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    if DEBUG:
        print(user.id)
        print(user.name)
    if not db.find_user(user.id):
        db.add_User(user.name, user.id, dev)

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def add_temp_command(update: Update, context: CallbackContext) -> None:
    db.add_Temperature(100, dev, func.now())
    update.message.reply_text('temp!')

def show_water_command(update: Update, context: CallbackContext) -> None:
    water = db.get_last_Water(dev)
    if water is not None:
        update.message.reply_text('Last Water: ' + str(water.value))
    else:
        update.message.reply_text('NO Water!')

def show_hum_command(update: Update, context: CallbackContext) -> None:
    hum = db.get_last_Humidity(dev)
    if hum is not None:
        
        if hum.value == 1:
            message = "Your Plant has enough water!"
        else:
            message = "Your Plant need for water!"

        update.message.reply_text(message)
    else:
        update.message.reply_text('NO Hum!')

def show_temp_command(update: Update, context: CallbackContext) -> None:
    
    temp = db.get_last_Temperature(dev)
    if temp is not None:
        update.message.reply_text('Last Temp: ' + str(temp.value))
    else:
        update.message.reply_text('NO Temp!')

def error(update, context: CallbackContext) -> None:
    logger.warning("Update {0} caused error {1}".format(update, context.error))

def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("show_temp", show_temp_command))
    dispatcher.add_handler(CommandHandler("show_hum", show_hum_command))
    dispatcher.add_handler(CommandHandler("show_water", show_water_command))
    dispatcher.add_handler(CommandHandler("add_temp", add_temp_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    commands = [
        BotCommand("start", "Starts the bot"),
        BotCommand("show_temp", "Shows the last temperature of your Plant!"),
        BotCommand("show_hum", "Shows the last humidity of your Plant!"),
        BotCommand("show_water", "Shows if your Plant needs for water!"),
        BotCommand("add_temp", "Add the last temperature of your Plant!"),
        BotCommand("help", "Shows a list of all possible commands")]
    dispatcher.bot.set_my_commands(commands)

    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,
    #                       webhook_url="https://{0}.herokuapp.com/{1}".format(HEROKU_NAME, TOKEN))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    time.sleep(5)

    # updater.idle()


if __name__ == '__main__':
    main()
