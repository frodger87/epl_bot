from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.models import PointTable
from epl_bot.parser.standings import get_league_standings


def load_string_point_table():
    new_string = PointTable(data=get_league_standings(league=39, season=2023))

    db_session.add(new_string)
    db_session.commit()


if __name__ == '__main__':
    load_string_point_table()
