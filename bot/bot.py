from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from projects.epl_football_bot import settings


async def greet_user(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Привет! Я бот по Английской Премьер лиге')


def main():
    application = ApplicationBuilder().token(settings.API_KEY).build()
    start_handler = CommandHandler('start', greet_user)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
