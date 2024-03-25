import matplotlib.pyplot as plt
from epl_bot import settings
from epl_bot.db_utils.db import db_session
from epl_bot.db_utils.models import PointTable


def transform_table(raw_table: dict) -> dict:
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


def create_table_png(data: dict):
    fig = plt.figure(figsize=(6, 6), dpi=200)
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
            ha='left'
        )
        ax.annotate(
            xy=(1.0, y),
            text=data['teams'][y],
            ha='center'
        )
        ax.annotate(
            xy=(2.0, y),
            text=data['played'][y],
            ha='center'
        )
        ax.annotate(
            xy=(2.5, y),
            text=data['win'][y],
            ha='center'
        )
        ax.annotate(
            xy=(3.0, y),
            text=data['draw'][y],
            ha='center'
        )
        ax.annotate(
            xy=(3.5, y),
            text=data['lose'][y],
            ha='center'
        )
        ax.annotate(
            xy=(4.0, y),
            text=data['goals for'][y],
            ha='center'
        )
        ax.annotate(
            xy=(4.5, y),
            text=data['goals against'][y],
            ha='center'
        )
        ax.annotate(
            xy=(5.0, y),
            text=data['points'][y],
            ha='center'
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


def save_png_table():
    raw_table = (
        db_session
        .query(PointTable)
        .order_by(
            PointTable
            .create_date
            .desc()
        )
        .limit(1)
        .first()
        .data
    )
    create_table_png(transform_table(raw_table))


if __name__ == '__main__':
    save_png_table()
