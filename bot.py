import os
import logging
import time

from datetime import datetime
from sqlalchemy.sql import func
from dotenv import load_dotenv
from telegram import Update, ForceReply, BotCommand, ParseMode, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from database import DBHandler


load_dotenv()

DEBUG = True
token = os.environ['TOKEN']
dev = os.environ['DEVICE']
bot = Bot(token=token)
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
        fr'Hello {user.mention_markdown_v2()}\, use the /help command to see all the possible commands'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "*Utilities:*\n"
        "/help - "
        "Shows a list of all possible commands\n"
        "/start - "
        "Starts the monitoring of your plant\n"
        "/status - "
        "Gives you the status of your plant\n"
        "\n*Return Records*\n"
        "/avgtemp - "
        "Returns the average temperature of the last hour\n"
        "/avghum - "
        "Returns the average humidity of the last hour\n"
        "/lasttemp - "
        "Shows the last recorded temperature\n"
        "/lasthum - "
        "Shows the last recorded humidity\n"
        "/lastwater - "
        "Shows the last time you watered your plant\n",
        parse_mode=ParseMode.MARKDOWN)


def status_command(update: Update, context: CallbackContext) -> None:
    temp, water, hum_status = db.get_status(dev)
    if temp and water:
        update.message.reply_text('Your plant needs some water and a better temperature!\nThe humidity of the environment is ' + hum_status)
    elif temp:
        update.message.reply_text('Your plant needs a better temperature!\nThe humidity of the environment is ' + hum_status)
    elif water:
        update.message.reply_text('Your plant needs still some water!\nThe humidity of the environment is ' + hum_status)
    else:
        update.message.reply_text('Good job! Your plant is healty and watered!\nThe humidity of the environment is ' + hum_status)


def last_temperature_command(update: Update, context: CallbackContext) -> None:
    temp = db.get_last_temperature(dev)
    if temp is not None:
        update.message.reply_text('Last temperature detected is: \n' + str(temp.value) + ' degrees')
    else:
        update.message.reply_text('There are no records for temperature')


def last_humidity_command(update: Update, context: CallbackContext) -> None:
    hum = db.get_last_humidity(dev)
    if hum is not None:
        update.message.reply_text('Last humidity detected is: \n' + str(hum.value) + '%')
    else:
        update.message.reply_text('There are no records for humidity')


def last_water_command(update: Update, context: CallbackContext) -> None:
    time = db.get_last_watered(dev)
    if time is not None:
        format_data = "%d/%m/%y at %H:%M:%S"
        timestr = time.strftime(format_data)
        update.message.reply_text('Last time your plant was watered: \n' + timestr)
    else:
        update.message.reply_text('There are no records for water')


def avg_temperature_command(update: Update, context: CallbackContext) -> None:
    avgtemp = db.get_avg_temperature(dev)
    if avgtemp is not None:
        update.message.reply_text('Average temperature detected is: \n' + str("{:.2f}".format(avgtemp)) + ' degrees')
    else:
        update.message.reply_text('There are no records for temperature in the last hour')


def avg_humidity_command(update: Update, context: CallbackContext) -> None:
    avghum = db.get_avg_humidity(dev)
    if avghum is not None:
        update.message.reply_text('Average humidity detected is: \n' + str("{:.2f}".format(avghum)) + '%')
    else:
        update.message.reply_text('There are no records for humidity in the last hour')


def error(update, context: CallbackContext) -> None:
    logger.warning("Update {0} caused error {1}".format(update, context.error))


def main() -> None:
    """Start the bot."""
    updater = Updater(token)

    # get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("lasttemp", last_temperature_command))
    dispatcher.add_handler(CommandHandler("lasthum", last_humidity_command))
    dispatcher.add_handler(CommandHandler("lastwater", last_water_command))
    dispatcher.add_handler(CommandHandler("avgtemp", avg_temperature_command))
    dispatcher.add_handler(CommandHandler("avghum", avg_humidity_command))

    commands = [
        BotCommand("start", "Starts the bot"),
        BotCommand("help", "Shows a list of all possible commands"),
        BotCommand("status", "Shows the status of your plant"),
        BotCommand("lasttemp", "Shows the last temperature detected"),
        BotCommand("lasthum", "Shows the last humidity detected"),
        BotCommand("lastwater", "Shows the last moment your plant was watered"),
        BotCommand("avgtemp", "Shows the last temperature detected"),
        BotCommand("avghum", "Shows the avarage humidity detected")
    ]
    dispatcher.bot.set_my_commands(commands)
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

if __name__ == '__main__':
    main()
