import csv
import mysql.connector
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold, cross_validate
import pickle as pkl
import numpy as np
from collections import OrderedDict
import copy
from prettytable import PrettyTable as pt
import os

def main():

    features, labels = get_features_labels()

    features = np.array(features)
    labels = np.array(labels)



    predictions = {
                    'smoothMdl' : [],
                    'roughMdl'  : [],
                    'wPriorMdl' : [],
                    'woPriorMdl': []
                }

    smoothMdl = MultinomialNB(alpha=1.0, fit_prior=False)
    roughMdl = MultinomialNB(alpha=0, fit_prior=False)

    wPriorMdl = MultinomialNB(alpha=1.0, fit_prior=True)
    woPriorMdl = MultinomialNB(alpha=0, fit_prior=True)

    if not os.path.exists("model_predictions.pkl"):

        for i in np.arange(labels.shape[0]-1)[2:]:
            predictions['smoothMdl'].append(get_model_prediction(smoothMdl, features[:i+1,:], labels[:i+1]))
            predictions['roughMdl'].append(get_model_prediction(roughMdl, features[:i+1,:], labels[:i+1]))
            predictions['wPriorMdl'].append(get_model_prediction(wPriorMdl, features[:i+1,:], labels[:i+1]))
            predictions['woPriorMdl'].append(get_model_prediction(woPriorMdl, features[:i+1,:], labels[:i+1]))

        with open("model_predictions.pkl", 'wb') as predf:
            pkl.dump(predictions, predf)

    else:
        with open("model_predictions.pkl", 'rb') as predf:
            predictions = pkl.load(predf)

    smoothAcc = (predictions['smoothMdl'] == labels).mean()
    roughAcc = (predictions['roughMdl'] == labels).mean()
    wPriorAcc = (predictions['wPriorMdl'] == labels).mean()
    woPriorAcc = (predictions['woPriorMdl'] == labels).mean()

    print("Model Prediction Accuracies: ")
    tab = pt(['Prior', 'alpha', 'Accuracy'])
    tab.add_row(['No', '1.0', smoothAcc])
    tab.add_row(['No', '0', roughAcc])
    tab.add_row(['Yes', '1.0', wPriorAcc])
    tab.add_row(['Yes', '0', woPriorAcc])

    print(tab)


def get_model_prediction(model, features, labels):
    model.fit(features[:-1,:], labels[:-1])
    return model.predict(features[-1,:].reshape(1,-1))


def get_features_labels():

    if os.path.exists('features.npy') and os.path.exists('labels.npy'):
        return np.load('features.npy'), np.load('labels.npy')

    stock_prices = get_stock_prices()
    prior, dates = get_prior()

    prior = OrderedDict(sorted(prior.items(), key=lambda x: x[0]))
    dates = OrderedDict(sorted(dates.items(), key=lambda x: x[0]))

    template = OrderedDict([(word, 0) for word in prior.keys()])

    features = []
    labels = []

    missing_dates = []

    temp_word_join = []
    weekend_day_validation = 0
    current = copy.deepcopy(template)

    for date, words in dates.items():

        for word in words:
            if not word.startswith("http"):
                current[word] += 1

        if date in stock_prices:

            features.append(list(current.values()))
            current = copy.deepcopy(template)

            if stock_prices[date][1] - stock_prices[date][0] < 0:
                val = -1
            elif stock_prices[date][1] - stock_prices[date][0] > 0:
                val = 1
            else:
                val = 0

            labels.append(val)

    np.save('features.npy', features)
    np.save('labels.npy', labels)

    return features, labels


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
    word.execute("SELECT rwc.word, rwc.count, w.date "\
                +"FROM RawWordCount as rwc "\
                +"LEFT JOIN WordDate as w on rwc.dateId = w.id")

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
    import sys
    if len(sys.argv) > 0:
        if sys.argv[1] == '--refresh':
            os.system("rm *.pny; rm *.pkl")
    main()
