import logging

from epl_bot import settings
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters, CallbackQueryHandler

from handlers import greet_user, send_point_table, send_news_headers, \
    send_fixtures, choose_favourite_team, skip_choosing_fav_team, fetch_favourite_team

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)


def main():
    application = ApplicationBuilder().token(settings.BOT_API_KEY).build()

    application.add_handler(MessageHandler(filters.Regex('^(Любимая команда)$'), choose_favourite_team))
    application.add_handler(CallbackQueryHandler(fetch_favourite_team))
    application.add_handler(CommandHandler('start', greet_user))
    application.add_handler(
        MessageHandler(filters.Regex('^(Таблица)$'), send_point_table))
    application.add_handler(
        MessageHandler(filters.Regex('^(Новости)$'), send_news_headers))
    application.add_handler(
        MessageHandler(filters.Regex('^(Ближайшие матчи)$'), send_fixtures))
    application.add_handler(CommandHandler('skip', skip_choosing_fav_team))

    logging.info('Бот стартовал')

    application.run_polling()


if __name__ == '__main__':
    main()
