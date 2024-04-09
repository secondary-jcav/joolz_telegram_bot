import logging
from dotenv import load_dotenv, find_dotenv
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from film_journalist import FilmJournalist

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tmdb_key = os.environ['TMDB_API_KEY']
    critic = FilmJournalist(tmdb_key)
    await critic.session_start()
    await critic.session_start()
    movies = await critic.get_movie_score(update.message.text)
    if movies:
        for movie in movies:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'{movie["name"]} ({movie["date"]}). Score:{movie["rating"]}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'No movies found')
    await critic.session_close()


if __name__ == '__main__':
    _ = load_dotenv(find_dotenv())  # read local .env file
    telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
    tmdb_key = os.environ['TMDB_API_KEY']
    critic = FilmJournalist(tmdb_key)

    application = ApplicationBuilder().token(telegram_token).build()
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
