from epl_bot import settings
from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.loader import get_or_create_user
from epl_bot.db_utils.models import NewsFeedTable, User
from sqlalchemy import update
from telegram import Update, ReplyKeyboardMarkup
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
    favourite_team = db_session.query(User).where(
        User.user_id == str(update.effective_user.id)).first().favourite_team
    if favourite_team == None:
        await  update.message.reply_text(
            f'Выбери команду из списка(введите /skip что бы пропустить этот шаг):\n{", ".join(settings.TEAMS)}')
        return "favourite_team"
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Твоя любимая команда {favourite_team.capitalize()}'
        )


async def check_team_name(update: Update, context):
    team_name = update.message.text
    if team_name == '/skip':
        return ConversationHandler.END
    elif team_name not in settings.TEAMS:
        await update.message.reply_text(
            f'Пожалуйста введите команду из списка (введите /skip что бы пропустить этот шаг): \n{", ".join(settings.TEAMS)}',
        )
        return "favourite_team"
    else:
        context.user_data["favourite_team"] = {"favourite_team": team_name}
        await update.message.reply_text(
            f'Твоя любимая команда {team_name}')
        db_session.query(User).where(
            User.user_id == str(update.effective_user.id)).update(
            {'favourite_team': f'{team_name}'})
        db_session.commit()
        return ConversationHandler.END


async def skip_choosing_fav_team(update: Update, context):
    return ConversationHandler.END
