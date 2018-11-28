import csv
import mysql.connector
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import pickle as pkl
import numpy as np
from collections import OrderedDict
import copy


def main():

    stock_prices = get_stock_prices()
    prior, dates = get_prior()

    prior = OrderedDict(sorted(prior.items(), key=lambda x: x[0]))
    dates = OrderedDict(sorted(dates.items(), key=lambda x: x[0]))

    template = OrderedDict([(word, 0) for word in prior.keys()])

    features = []
    labels = []

    missing_dates = []

    for date, words in dates.items():
        current = copy.deepcopy(template)
        for word in words:
            current[word] += 1

        features.append(list(current.values()))
        if date in stock_prices:
            if stock_prices[date][1] - stock_prices[date][0] < 0:
                val = -1
            elif stock_prices[date][1] - stock_prices[date][0] > 0:
                val = 1
            else:
                val = 0
        else:
            val = 0
            print("Missing date: {} in stock prices".format(str(date)))
            missing_dates.append(str(date))

        labels.append(val)

    if missing_dates != []:
        with open("missing_dates.txt", 'w') as file:
            file.write("\n".join(missing_dates))
    print(labels[:1])
    print(features[:1])

    # features and labels created, pass through naive bayes classifier


def get_stock_prices():

    stock_prices = {}

    con = connect_db()
    stockcur = con.cursor(buffered=True)
    stockcur.execute("SELECT * FROM TeslaStock")
    for _, date, openprice, closeprice in stockcur.fetchall():
        stock_prices[date] = [openprice, closeprice]

    stockcur.close()
    con.close()

    return stock_prices


def get_prior():
    con = connect_db()
    word = con.cursor()
    word.execute("SELECT rwc.word, rwc.count, w.date FROM RawWordCount as rwc LEFT JOIN WordDate as w on rwc.dateId = w.id")

    prior = {}
    dates = {}

    for word, count, date in word.fetchall():
        if word in prior:
            prior[word] += count
        else:
            prior[word] = count
        if date not in dates:
            dates[date] = {word:count}
        else:
            dates[date][word] = count

    return prior, dates

'''
def get_tweets():

    tweets = []
    dates = []
    currdate = ""
    currwords = ""

    con = connect_db()
    tweetcur = con.cursor()
    tweetcur.execute("SELECT * FROM RawTweet")

    #replace_chars = {"\"":"", "!":" !", "?":" ?", )

    for _, tweetdatetime, tweettext in tweetcur.fetchall():
        if not str(tweetdatetime).split(" ")[0] == currdate:
            for terms in
            currwords.replaceall("\"", "")
            currwords.replaceall()
            tweets.append(currwords)
            currdate = str(tweetdatetime).split(" ")[0]
            dates.append(currdate)
            currwords = tweettext
        else:
            currwords += " " + tweettext

    tweets.remove("")

    tweetcur.close()
    con.close()

    return tweets, dates
'''

def connect_db():

    config = {
        'user': 'cfarmer',
        'password': 'eKd65T',
        'host': 'cse.unl.edu',
        'database': 'cfarmer'
    }

    try:
        con = mysql.connector.connect(**config)
    except Exception as e:
        print('Could not connect to database')
        raise e

    return con

if __name__ == '__main__':
    main()
