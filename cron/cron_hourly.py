from epl_bot.bot.utils import save_png_point_table, save_png_fixtures
from epl_bot.db_utils.loader import load_string_news_feed_table


def main():
    save_png_point_table()
    load_string_news_feed_table()
    save_png_fixtures()


if __name__ == '__main__':
    main()
