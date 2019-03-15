s = session()
data = get_news('https://news.ycombinator.com/newest', n_pages = 35)
for i in data:
    news = News(title = i.get('title'),
                author = i.get('author'),
                url = i.get('url'),
                points = i.get('points'),
                comments = i.get('comments'),)
    s.add(news)
    s.commit()
