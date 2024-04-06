import matplotlib.pyplot as plt
from epl_bot import settings
from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.models import PointTable, FixturesTable
from datetime import datetime


def transform_raw_point_table(raw_table: dict) -> dict:
    data_transformed = {}
    pos_list = [k for k, v in raw_table.items()]
    teams_lst = [v['name'] for k, v in raw_table.items()]
    played_lst = [v['played'] for k, v in raw_table.items()]
    win_lst = [v['win'] for k, v in raw_table.items()]
    draw_lst = [v['draw'] for k, v in raw_table.items()]
    lose_lst = [v['lose'] for k, v in raw_table.items()]
    goals_for_lst = [v['goals for'] for k, v in raw_table.items()]
    goals_against_lst = [v['goals against'] for k, v in raw_table.items()]
    points_lst = [v['points'] for k, v in raw_table.items()]

    data_transformed['pos'] = pos_list[::-1]
    data_transformed['teams'] = teams_lst[::-1]
    data_transformed['played'] = played_lst[::-1]
    data_transformed['win'] = win_lst[::-1]
    data_transformed['draw'] = draw_lst[::-1]
    data_transformed['lose'] = lose_lst[::-1]
    data_transformed['goals for'] = goals_for_lst[::-1]
    data_transformed['goals against'] = goals_against_lst[::-1]
    data_transformed['points'] = points_lst[::-1]

    return data_transformed


def transform_raw_fixtures(raw_fixtures: dict) -> dict:
    fixture_dict = {}
    if len(raw_fixtures) > 0:
        fixture_dict['date'] = [datetime.strptime(k, '%Y-%m-%dT%H:%M:%S').strftime('%d %B   %H:%M') for k, v in raw_fixtures.items()][::-1]
        fixture_dict['fix'] = [v for k, v in raw_fixtures.items()][::-1]
    else:
        fixture_dict['date'] = ['В ближайшую неделю матчей нет']
        fixture_dict['fix'] = [' ']

    return fixture_dict


def create_point_table_png(data: dict):
    fig = plt.figure(figsize=(6, 4), dpi=300)
    ax = plt.subplot(111)

    ncols = 5
    nrows = 20

    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_axis_off()

    for y in range(0, nrows):
        ax.annotate(
            xy=(0.0, y),
            text=data['pos'][y],
            ha='left',
            color='grey',
        )
        ax.annotate(
            xy=(1.0, y),
            text=data['teams'][y],
            ha='center',
        )
        ax.annotate(
            xy=(2.0, y),
            text=data['played'][y],
            ha='center',
            color='grey',
        )
        ax.annotate(
            xy=(2.5, y),
            text=data['win'][y],
            ha='center',
            color='grey',
        )
        ax.annotate(
            xy=(3.0, y),
            text=data['draw'][y],
            ha='center',
            color='grey',
        )
        ax.annotate(
            xy=(3.5, y),
            text=data['lose'][y],
            ha='center',
            color='grey',
        )
        ax.annotate(
            xy=(4.0, y),
            text=data['goals for'][y],
            ha='center',
            color='grey',
        )
        ax.annotate(
            xy=(4.5, y),
            text=data['goals against'][y],
            ha='center',
            color='grey',
        )
        ax.annotate(
            xy=(5.0, y),
            text=data['points'][y],
            ha='center',
        )

    ax.annotate(
        xy=(1.0, nrows),
        text='TEAM',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(2.0, nrows),
        text='P',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(2.5, nrows),
        text='W',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(3.0, nrows),
        text='D',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(3.5, nrows),
        text='L',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(4.0, nrows),
        text='G+',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(4.5, nrows),
        text='G-',
        weight='bold',
        ha='center'
    )
    ax.annotate(
        xy=(5.0, nrows),
        text='PTS',
        weight='bold',
        ha='center'
    )

    plt.savefig(
        f'{settings.SAVE_PNG_PATH}' + 'point_table.png',
        dpi=300,
        transparent=True
    )


def create_fixtures_png(data: dict):
    picture_height = len(data['date'])//2 + 1
    fig = plt.figure(figsize=(6, picture_height), dpi=250)
    ax = plt.subplot(111)

    ncols = 2
    nrows = len(data['date'])

    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_axis_off()

    for y in range(0, nrows):
        ax.annotate(
            xy=(0.0, y),
            text=data['date'][y],
            ha='left',
            fontsize=12,
            color='grey'
        )
        ax.annotate(
            xy=(0.8, y),
            text=data['fix'][y],
            ha='left',
            fontsize=12
        )

    plt.savefig(
        f'{settings.SAVE_PNG_PATH}' + 'fixtures.png',
        dpi=300,
        transparent=True
    )


def get_last_value_from_db_table(table_model):
    return (
        db_session
        .query(table_model)
        .order_by(
            table_model
            .create_date
            .desc()
        )
        .limit(1)
        .first()
        .data
    )


def save_png_point_table():
    raw_table = (
        get_last_value_from_db_table(PointTable)
    )
    create_point_table_png(transform_raw_point_table(raw_table))


def save_png_fixtures():
    raw_table = (
        get_last_value_from_db_table(FixturesTable)
    )
    create_fixtures_png(transform_raw_fixtures(raw_table))


def string_to_hyperlink(string, link):
    return f"<a href='{link}'>{string}</a>"


def get_header_list(news_raw: dict):
    return '\n\n'.join(
        [string_to_hyperlink(string=k, link=v) for k, v in
         news_raw.items()])


if __name__ == '__main__':
    save_png_fixtures()
    save_png_point_table()
