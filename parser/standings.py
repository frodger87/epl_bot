import requests
import json
from epl_bot import settings


def get_league_standings(league, season):
    url = "https://v3.football.api-sports.io/standings"
    parameters = {"league": str(league), "season": str(season)}

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': settings.API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=parameters)

    data = response.json()

    league_table = {}
    for team in data['response'][0]['league']['standings'][0]:
        league_table[team['rank']] = \
            {
                'name': team['team']['name'],
                'played': team['all']['played'],
                'win': team['all']['win'],
                'draw': team['all']['draw'],
                'lose': team['all']['lose'],
                'goals for': team['all']['goals']['for'],
                'goals against': team['all']['goals']['against'],
                'points': team['points']
            }

    return league_table


league_id = 39
season_year = 2023
teams_data = get_league_standings(league_id, season_year)
print(json.dumps(teams_data, indent=4))
