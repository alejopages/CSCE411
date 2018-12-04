import pandas as pd
from mysql import connector as dbcon
import pandas as pd
import os.path as osp
import numpy as np
import pickle as pkl
import datetime as dt
import csv


def main():
    # do something
    print("Update stock predictions")
    update_stock_predictions()
    print("Updating word probability predictions")
    update_word_prob_occurances()

    return None


def update_stock_predictions():

    con = get_db_con()

    cur = con.cursor()

    query = "update TeslaStock set prediction = %s where date = %s"

    reader = csv.DictReader(open('predictions.csv'))

    data = []

    for row in reader:
        data.append((row['direction'], row['date']))

    cur.executemany(query, tuple(data))
    con.commit()
    cur.close()
    con.close()


def print_db_word_stats():

    con = get_db_con()

    cur = con.cursor()

    cur.execute("select * from word_stats")

    for row in cur.fetchall():
        print(row)

def data_proc_pipeline():
    word_count = get_word_counts() #TAKE OUT STORE DATA IN FUNCTIONS IN CASE CHANGES OF DATABASE
    stock_prices = get_stock_prices()

    word_data = pd.DataFrame(data=word_count, columns=['id', 'word', 'count', 'date'])
    stock_data = pd.DataFrame(data=stock_prices, columns=['id', 'openprice', 'closeprice', 'date'])

    while(pd.unique(word_data['date'].isin(stock_data['date'])).shape[0] > 1):
        word_data.loc[~word_data['date'].isin(stock_data['date']), 'date'] += dt.timedelta(days=1)

    agg = pd.merge(stock_data, word_data, how='right', on='date', sort=True, suffixes=('_stock', '_word'))

    word_stats = pd.DataFrame(pd.unique(agg['word']), columns=['word'])
    word_stats['count'] = word_stats['word'].apply(lambda x: np.sum(agg.loc[agg['word'] == x, 'count']))

    total_words = np.sum(word_stats['count'])
    word_stats['prob_occur'] = word_stats['count'].apply(lambda x: x / total_words * 100)

    word_stats['prob_inc'] = word_stats['word'].apply(lambda x: np.sum(agg.loc[(agg['word'] == x) & (agg['closeprice'] - agg['openprice'] >= 0), 'count']))
    word_stats['prob_inc'] = word_stats.apply(lambda x: x['prob_inc'] / x['count'], axis=1)

    word_stats['prob_dec'] = word_stats.apply(lambda x: 1.0 - x['prob_inc'], axis = 1)

    word_stats[['word', 'prob_inc', 'prob_occur']].to_csv('word_stats.csv')

    stock_data['num_words'] = stock_data.apply(lambda x: agg.loc[agg['date'] == x['date'], 'count'].sum(), axis=1)

    agg = agg.merge(word_stats[['word', 'prob_inc']], how='left', on='word')

    agg['product'] = agg.apply(lambda x: x['count'] * x['prob_inc'], axis=1)

    stock_data['prediction'] = stock_data.apply(lambda x: agg.loc[x['date'] == agg['date'], 'product'].sum(), axis=1)

    stock_data['prediction'] = stock_data.apply(lambda x: x['prediction'] / x['num_words'] if (x['num_words'] > 0) else 0, axis=1)

    stock_data['direction'] = np.zeros((stock_data.shape[0]))
    stock_data['direction'] = stock_data.apply(lambda x: 1 if x['prediction'] > 0.5 else (-1 if x['prediction'] < 0.5 else 0), axis=1)
    stock_data['direction'] = stock_data.apply(lambda x: 0 if x['num_words'] == 0 else x['num_words'], axis=1)

    stock_data[['date','direction']].to_csv("predictions.csv")



def update_word_prob_occurances():

    reader = csv.DictReader(open('word_stats.csv'))

    con = get_db_con()

    cur = con.cursor()
    '''
    cur.execute("DROP TABLE word_stats")

    cur.execute("CREATE TABLE word_stats("
              + "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
              + "word VARCHAR(256) NOT NULL,"
              + "prob_increase FLOAT NOT NULL,"
              + "prob_occurred FLOAT NOT NULL)")
    '''

    query = "UPDATE RawWordCount SET prob_increase = %s, prob_occurres = %s "\
           +"WHERE word = %s"


    data = []

    for row in reader:


        data.append((float(row['prob_inc']), float(row['prob_occur']), str(row['word'])))


    cur.executemany(query, tuple(data))
    con.commit()

    cur.close()
    con.close()

def main1():
    word_count = get_word_counts() #TAKE OUT STORE DATA IN FUNCTIONS IN CASE CHANGES OF DATABASE
    stock_prices = get_stock_prices()

    word_data = pd.DataFrame(data=word_count, columns=['id', 'word', 'count', 'date'])

    stock_data = pd.DataFrame(data=stock_prices, columns=['id', 'openprice', 'closeprice', 'date'])

    fig = word_data.sort_values(by=['count'])[['count', 'word']].plot(x='word', y='count', kind='bar', figsize=(6,6), title='Word Counts')


def get_word_counts():

    if osp.exists('word_counts.pkl'):
        return pkl.load('word_counts.pkl')

    con = get_db_con()
    wordcur = con.cursor(buffered=True)
    wordcur.execute("SELECT rwc.id, rwc.word, rwc.count, w.date "\
                   +"FROM RawWordCount as rwc "\
                   +"RIGHT JOIN WordDate as w on rwc.dateId = w.id")

    word_count = []

    for id, word, count, date in wordcur.fetchall():
        word_count.append({'id'   : id,
                           'word' : word,
                           'count': int(count),
                           'date' : date})

    wordcur.close()
    con.close()

    # store_data(word_count)

    return word_count


def get_stock_prices():

    if osp.exists('stock_prices.pkl'):
        return pkl.load('stock_prices.pkl')

    con = get_db_con()
    stockcur = con.cursor(buffered=True)
    stockcur.execute("SELECT * FROM TeslaStock")

    stock_prices = []

    for id, date, openprice, closeprice in stockcur.fetchall():
        stock_prices.append({'id'         : id,
                             'date'       : date,
                             'openprice'  : openprice,
                             'closeprice' : closeprice})

    stockcur.close()
    con.close()

    # store_data(stock_prices)

    return stock_prices


def get_db_con():

    config = {
        'user': 'cfarmer',
        'password': 'eKd65T',
        'host': 'cse.unl.edu',
        'database': 'cfarmer'
    }

    try:
        con = dbcon.connect(**config)
    except Exception as e:
        print('Could not connect to database')
        raise e

    return con


if __name__ == '__main__':
    main()
