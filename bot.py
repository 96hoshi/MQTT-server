import os
import logging
import time

# from datetime import datetime
from sqlalchemy.sql import func
from dotenv import load_dotenv
from telegram import Update, ForceReply, BotCommand, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from database import DBHandler

load_dotenv()

DEBUG = True
dev = 1 #TODO: rimuovere var globale e sostituire con device dell'utente
TOKEN = os.environ['TOKEN']
bot = Bot(token=TOKEN)
db = DBHandler()



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
    """Send a message when the command /help is issued."""
    db.add_Temperature(100, dev, func.now())
    update.message.reply_text('temp!')

def show_temp_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    temp = db.get_last_Temperature(dev)
    if temp is not None:
        update.message.reply_text('Last Temp: ' + str(temp.value))
    else:
        update.message.reply_text('NO Temp!')

# def echo(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     # update.message.reply_text(update.message.text)
#     update.message.reply_text("ok")


def error(update, context: CallbackContext) -> None:
    logger.warning("Update {0} caused error {1}".format(update, context.error))


# def send_message(text):
#     bot.send_message(chat_id=92491394, text=text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("show_temp", show_temp_command))
    dispatcher.add_handler(CommandHandler("add_temp", add_temp_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    commands = [
        BotCommand("start", "Starts the bot"),
        BotCommand("show_temp", "Shows the last temperature of your Plant!"),
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

    # if not check:
    #     print("check")
    #     if user_id:
    #         print("user_id")
    #         print(user_id)
    #         bot.send_message(chat_id=user_id, text='Innaffia la paintaa')
    #         check = True

    # updater.idle()


if __name__ == '__main__':
    main()
