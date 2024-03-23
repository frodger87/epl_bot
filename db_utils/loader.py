from db import db_session
from models import PointTable
from projects.epl_bot.parser.standings import get_league_standings

new_string = PointTable(data=get_league_standings(league=39, season=2023))

db_session.add(new_string)
db_session.commit()
