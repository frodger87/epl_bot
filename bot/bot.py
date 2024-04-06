import logging

from epl_bot import settings
from epl_bot.db_utils.models import NewsFeedTable
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters

from utils import get_header_list, get_last_value_from_db_table

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)


async def greet_user(update: Update, context):
    my_keyboard = ReplyKeyboardMarkup(
        [['Таблица'], ['Новости'], ['Ближайшие матчи'], ['Любимая команда']])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Привет! Я бот по Английской Премьер лиге',
                                   reply_markup=my_keyboard)


async def send_point_table(update: Update, context):
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=open(
                                     f'{settings.SAVE_PNG_PATH}' + 'point_table.png',
                                     'rb'))


async def send_news_headers(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=get_header_list(
                                       get_last_value_from_db_table(
                                           NewsFeedTable)), parse_mode='html')


async def send_fixtures(update: Update, context):
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=open(
                                     f'{settings.SAVE_PNG_PATH}' + 'fixtures.png',
                                     'rb'))


def main():
    application = ApplicationBuilder().token(settings.BOT_API_KEY).build()
    start_handler = CommandHandler('start', greet_user)
    application.add_handler(start_handler)
    application.add_handler(
        MessageHandler(filters.Regex('^(Таблица)$'), send_point_table))
    application.add_handler(
        MessageHandler(filters.Regex('^(Новости)$'), send_news_headers))
    application.add_handler(
        MessageHandler(filters.Regex('^(Ближайшие матчи)$'), send_fixtures))

    logging.info('Бот стартовал')

    application.run_polling()


if __name__ == '__main__':
    main()
