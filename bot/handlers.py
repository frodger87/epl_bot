from epl_bot import settings
from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.loader import get_or_create_user
from epl_bot.db_utils.models import NewsFeedTable, User
from sqlalchemy import update
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

from utils import get_header_list, get_last_value_from_db_table


async def greet_user(update: Update, context):
    my_keyboard = ReplyKeyboardMarkup(
        [['Таблица'], ['Новости'], ['Ближайшие матчи'], ['Любимая команда']])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Привет! Я бот по Английской Премьер лиге',
                                   reply_markup=my_keyboard)
    await get_or_create_user(update.effective_user, update.message.chat.id)


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


async def choose_favourite_team(update: Update, context):
    inline_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f'{team}', callback_data=f'{team}')] for team in settings.TEAMS]
    )
    favourite_team = db_session.query(User).where(
        User.user_id == str(update.effective_user.id)).first().favourite_team
    if favourite_team == None:
        await  update.message.reply_text(
            f'Выберите команду из списка\n(введите /skip что бы пропустить этот шаг)',
            reply_markup=inline_keyboard
        )

        return "favourite_team"
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Твоя любимая команда: {favourite_team.capitalize()}'
        )


async def skip_choosing_fav_team(update: Update, context):
    return ConversationHandler.END


async def fetch_favourite_team(update: Update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f'Твоя любимая команда: {update.callback_query.data}')
    db_session.query(User).where(
        User.user_id == str(update.effective_user.id)).update(
        {'favourite_team': f'{update.callback_query.data}'})
    db_session.commit()
