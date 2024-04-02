from epl_bot import settings
from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.models import PointTable, NewsFeedTable
from epl_bot.parser.news_epl import get_news, get_html
from epl_bot.parser.standings import get_league_standings


def load_string_point_table():
    new_string = PointTable(data=get_league_standings(league=39, season=2023))

    db_session.add(new_string)
    db_session.commit()


def load_string_news_feed_table():
    new_string = NewsFeedTable(data=get_news(get_html(settings.HTML_NEWS)))

    db_session.add(new_string)
    db_session.commit()


if __name__ == '__main__':
    load_string_point_table()
    load_string_news_feed_table()
