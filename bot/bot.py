import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters

import settings

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)


async def greet_user(update: Update, context):
    my_keyboard = ReplyKeyboardMarkup([['Таблица']])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Привет! Я бот по Английской Премьер лиге',
                                   reply_markup=my_keyboard)


async def send_point_table(update: Update, context):
    image_name = settings.IMAGE_TABLE_PATH
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=open(image_name, 'rb'))


def main():
    application = ApplicationBuilder().token(settings.API_KEY).build()
    start_handler = CommandHandler('start', greet_user)
    application.add_handler(start_handler)
    application.add_handler(
        MessageHandler(filters.Regex('^(Таблица)$'), send_point_table))

    logging.info('Бот стартовал')

    application.run_polling()


if __name__ == '__main__':
    main()
