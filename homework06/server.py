from bottle import route, run, template, request
from bottle import redirect
from scraps import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from bayes import train_test_split

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    labels = {
        'good': 1,
        'maybe': 0,
        'never': -1
    }
    s = session()
    label = labels[request.query.label] or labels['maybe']
    id = request.query.id
    news_n = s.query(News).get(id)
    news_n.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    fresh_news = get_news('https://news.ycombinator.com/newest', n_pages = 1)
    for i in fresh_news:
        for j in s.query(News).all():
            if j.get('title') != i.get('title') and j.get('author') != i.get('author'):
                update = News(title = i.get('title'),
                              author = i.get('author'),
                              url = i.get('url'),
                              points = i.get('points'),
                              comments = i.get('comments'))
                s.add(update)
                s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    return template('classification', rows=s.query(News).filter(News.label == None).all())



@route('/recommendations')
def recommendations():
    s = session()
    list = s.query(News).filter(News.label != None).all()
    X, y = list, [news.label for news in list]
    X_train, y_train, X_test, y_test = train_test_split(X, y, param.SEED, train_size=param.TRAIN_SIZE)
    classifier = NaiveBayesClassifier(alpha=param.ALPHA)
    classifier.fit(X_train, y_train)

    data = []

    unlabeled = s.query(News).filter(News.label == None).all()

    for record in classifier.predict(unlabeled):
        data.append((record[0], int(record[1][0]), record[1][1]))

    classified_news = sorted(data, key=lambda x: (x[1], x[2]), reverse=True)
    return template('news_recommendations', rows=classified_news)

if __name__ == "__main__":
    run(host="localhost", port=8080)
