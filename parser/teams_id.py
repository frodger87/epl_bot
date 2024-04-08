import requests
from epl_bot import settings


"""
England     Premier League   39
Spain       La Liga          140
Italy       Serie A          135 
Germany     Bundesliga       78                
"""


def teams_info(league, season):
    url = "https://v3.football.api-sports.io/teams"
    parameters = {"league": str(league),
                  "season": str(season),
                  }

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': settings.API_KEY_PARSER
    }

    response = requests.request("GET", url, headers=headers, params=parameters)
    raw_info_1 = response.json()
    return raw_info_1


def extracting_teams_id(league, season):
    team_id = {}
    raw_info = teams_info(league, season)
    for team in raw_info['response']:
        team_id[team['team']['name']] = team['team']['id']

    return team_id


if __name__ == '__main__':
    teams_id = extracting_teams_id(league=39, season=2023)
    print(teams_id)
