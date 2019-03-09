s = session()
data = get_news('https://news.ycombinator.com/newest', n_pages = 35)
for i in data:
    news = News(title = data.get('title'),
                author = data.get('author'),
                url = data.get('url'),
                points = data.get('points'),
                comments = data.get('comments'),)
    s.add(news)
    s.commit()
