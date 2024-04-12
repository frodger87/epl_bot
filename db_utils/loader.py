from epl_bot import settings
from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.models import PointTable, NewsFeedTable, FixturesTable, \
    User
from epl_bot.parser.fixtures import get_fixtures
from epl_bot.parser.news_epl import get_news, get_html
from epl_bot.parser.standings import get_league_standings


def load_string_point_table():
    new_string = PointTable(
        data=get_league_standings(league=39, season=2023))

    db_session.add(new_string)
    db_session.commit()


def load_string_news_feed_table():
    new_string = NewsFeedTable(
        data=get_news(get_html(settings.HTML_NEWS)))

    db_session.add(new_string)
    db_session.commit()


def load_string_fixtures_table():
    new_string = FixturesTable(data=get_fixtures(39, 2023, "NS"))

    db_session.add(new_string)
    db_session.commit()


def get_or_create_user(effective_user, chat_id):
    if str(effective_user.id) not in [user.user_id for user in
                                      db_session.query(User)]:
        user_string = User(
            user_id=effective_user.id,
            chat_id=chat_id,
            subscribe=False,
        )

        db_session.add(user_string)
        db_session.commit()
