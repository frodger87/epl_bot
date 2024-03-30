import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.content.decode('cp1251')
        return html_content
    except (requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.find_all('div', class_='block news')
    news_title_with_link = {}
    for news in all_news:
        title = news.find('h3').text
        link = news.find('a')['href']
        full_link = f"http://fapl.ru{link}"
        news_title_with_link[title] = full_link

    return news_title_with_link


if __name__ == '__main__':
    news_from_fapl = get_html('http://fapl.ru/news/')
    print(get_news(news_from_fapl))
