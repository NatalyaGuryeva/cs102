import requests
from bs4 import BeautifulSoup

def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

def extract_news(soup):
    """ Extract news from a given web page """
    news_list = []
    table = soup.table.findAll('table')[1]
    tags = table.find_all('tr')
    del tags[2::3]
    tags.pop()
    tags.pop()
    for i in range(31):
        title = tags[0].find('a', class_= "storylink").text
        url = tags[0].find('a', class_="storylink").get('href')
        author = tags[1].find('a', class_="hnuser").text
        points = [int(s) for s in tags[1].find('span', class_= "score").text if s.isdigit()]
        comments = tags[1].find_all('td')[1].find_all('a')[5].text
        if comments != 'discuss':
            comments = [int(s) for s in tags[1].find_all('td')[1].find_all('a')[5].text if s.isdigit()]
        else:
            comments = 0
        news_list.append({
            'title': title,
            'author': author,
            'url': url,
            'points': points,
            'comments': comments
        })
        del tags[0]
        del tags[1]
    return news_list


def extract_next_page(soup):
    """ Extract next page URL """
    n = soup.find('a', class_= "morelink")
    next_page = str(n.get('href'))
    return next_page
