import requests
import datetime
import json
from epl_bot import settings


def get_api_fixtures(league, season):
    url = "https://v3.football.api-sports.io/fixtures"
    parameters = {"league": str(league),
                  "season": str(season),
                  "timezone": "Europe/Moscow"}

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': settings.API_KEY_PARSER
        }

    response = requests.request("GET", url, headers=headers, params=parameters)
    raw_data = response.json()
    return raw_data


def filtering_api_data(data, status):
    matches_dict = {}
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=6)
    for match in data["response"]:
        match_date = datetime.datetime.strptime(match["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z").date()
        if match["fixture"]["status"]["short"] == "NS" and today <= match_date <= future_date:
            date_time = match["fixture"]["date"]
            home_team = match["teams"]["home"]["name"]
            away_team = match["teams"]["away"]["name"]
            matches_dict[date_time] = f"{home_team} - {away_team}"
    return matches_dict


def get_fixtures(league, season, status):
    raw_api_data = get_api_fixtures(league, season)
    fixtures_data = filtering_api_data(raw_api_data, status)
    return fixtures_data


if __name__ == '__main__':
    fixtures = get_fixtures(39, 2023, "NS")
    print(json.dumps(fixtures, indent=4))
