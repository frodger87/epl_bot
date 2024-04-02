from epl_bot.bot.utils import save_png_table
from epl_bot.db_utils.loader import load_string_news_feed_table


def main():
    save_png_table()
    load_string_news_feed_table()


if __name__ == '__main__':
    main()
