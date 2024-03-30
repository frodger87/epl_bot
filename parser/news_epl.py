import requests
from bs4 import BeautifulSoup

url = 'http://fapl.ru/news/'
response = requests.get(url)
html_content = response.content.decode('cp1251')

soup = BeautifulSoup(html_content, 'html.parser')

news_div = soup.find_all('div', class_='block news')

dict_links = {}
for news in news_div:
    title = news.find('h3').text
    link = news.find('a')['href']
    full_link = f"http://fapl.ru{link}"
    dict_links[title] = full_link

print(dict_links)