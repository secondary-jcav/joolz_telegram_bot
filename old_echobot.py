import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola! Escribe el título en inglés de la película que quieres revisar')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    get_rotten_tomatoes_rating(update)


def get_rotten_tomatoes_rating(update):
    basic_url = 'https://www.rottentomatoes.com/api/private/v2.0/search?q='
    r = requests.get(basic_url + update.message.text)
    dict_response = r.json()
    # Print the movie name, year & score
    for movie_item in dict_response['movies']:
        if 'meterScore' in movie_item:
            update.message.reply_text(
                f"{movie_item['name']} ({movie_item['year']}) tiene una puntuación de {movie_item['meterScore']}/100")
    # Say that no movies were found
    if not dict_response['movies']:
        #  update.message.reply_text(update.message.text)
        update.message.reply_text("No se han conseguido películas con esa descripción")


def main():
    """Start the bot.

    Add the token when calling updater

    """
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    with open('token.json') as tj:
        data = json.load(tj)
    token = data["token"]
    # Token string goes here
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
