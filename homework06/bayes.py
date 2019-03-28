from collections import defaultdict
from collections import namedtuple
from math import log
from db import News, session
import random
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import defaultdict
import util.parameters as param
import string


def clean(text):
    tokens = [token.lower() for token in word_tokenize(text)]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]

    if not param.PRESERVE_STOP_WORDS:
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if w not in stop_words]

    if param.TOKEN_CLEANING_MODE == 'stemming':
        porter = PorterStemmer()
        cleaned = [porter.stem(word) for word in words]
    elif param.TOKEN_CLEANING_MODE == 'lemmatization':
        wordnet_lemmatizer = WordNetLemmatizer()
        cleaned = [wordnet_lemmatizer.lemmatize(word) for word in words]

    cleaned = list(set(cleaned))

    return cleaned


def get_stats(pool):
    stats = defaultdict(lambda: defaultdict(int))

    for entry in pool:
        stats[entry[1]][entry[0]] += 1

    return stats


def parse_train_data(X):
    pool = {'titles': [], 'authors': [], 'domains': []}

    for record in X:
        label, author, title, url = record.label, record.author, clean(record.title), record.url
        domain = url.split('//')[-1].split('/')[0]
        pool['titles'].extend([(label, word) for word in title])
        pool['authors'].extend([(label, author)])
        pool['domains'].extend([(label, domain)])
    return pool






def train_test_split(X, y, random_seed=None, train_size=0.7):
    random.seed(random_seed if random_seed != None else param.SEED)
    batch = list(zip(X, y))
    random.shuffle(batch)

    train = []
    for i in range(round(train_size * len(batch))):
        train.append(batch.pop())

    test = batch
    return ([X_train[0] for X_train in train],
            [y_train[1] for y_train in train],
            [X_test[0] for X_test in test],
            [y_test[1] for y_test in test])


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.smoothing_factor = alpha

    def fit(self, X, y):
        pool = parse_train_data(X)

        self.labels = list(set(news.label for news in X))
        self.train_data = namedtuple('Train', ['titles', 'authors', 'domains'])
        self.train_data.titles = get_stats(pool['titles'])
        self.train_data.authors = get_stats(pool['authors'])
        self.train_data.domains = get_stats(pool['domains'])

    def predict(self, X):
        prediction = []

        for news in X:

            tokens = clean(news.title)
            args = []

            for label in self.labels:

                logged_probabilities = []
                logged_probabilities.append(log(self.prior(label)))

                for token in tokens:
                    logged_probabilities.append(log(self.likelihood(token, label)))

                logged_probabilities.append(log(self.likelihood(news.author, label, mode='author')))

                domain = news.url.split('//')[-1].split('/')[0]
                logged_probabilities.append(log(self.likelihood(domain, label, mode='domain')))

                args.append((label, sum(logged_probabilities)))

            prediction.append((news, max(args, key=lambda x: x[1])))

        return prediction

    def score(self, X_test, y_test):
        total = 0
        correct = 0
        for i, result in enumerate(self.predict(X_test)):
            if int(result[1][0]) == int(y_test[i]):
                correct += 1
            total += 1
        return round(correct / total, 2)

    def nwords(self, def_dict, label=None):
        stat = defaultdict(int)

        for token in def_dict:
            for counts in def_dict[token].items():
                stat[str(counts[0])] += counts[1]

        return stat[label] if label != None else stat

    def likelihood(self, word, label, mode='title'):
        if mode == 'title':
            pool = self.train_data.titles
        elif mode == 'author':
            pool = self.train_data.authors
        elif mode == 'domain':
            pool = self.train_data.domains

        enc_of_this_word = pool[word][label] if pool[word] else 0
        all_words_in_class = self.nwords(pool, label)
        feature_vector_length = len(list(set(word for word in pool)))

        return (enc_of_this_word + self.smoothing_factor) / (all_words_in_class + self.smoothing_factor * feature_vector_length)

    def prior(self, label):
        data = s.query(News).filter(News.label == None).all()
        batch = list(filter(lambda news: news.label == label, data))
        return len(batch) / len(data)
