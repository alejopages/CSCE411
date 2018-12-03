import pandas as pd
from mysql import connector as dbcon
import pandas as pd
import os.path as osp
import numpy as np
import pickle as pkl
import datetime as dt
import csv

def main3():

    con = get_db_con()

    cur = con.cursor()

    cur.execute("SELECT * FROM word_stats")

    for row in cur.fetchall():
        print(row)

def main2():

    reader = csv.DictReader(open('word_stats.csv'))

    con = get_db_con()

    cur = con.cursor()

    cur.execute("DROP TABLE word_stats")

    cur.execute("CREATE TABLE word_stats("
              + "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
              + "word VARCHAR(256) NOT NULL,"
              + "prob_increase FLOAT NOT NULL,"
              + "prob_occurred FLOAT NOT NULL)")

    data = []

    for row in reader:
         data += [(str(row['word']), float(row['prob_inc']), float(row['prob_occ']))]



    print(tuple(data))

    cur.executemany("INSERT INTO word_stats (word, prob_increase, prob_occurred) VALUES (%s, %s, %s)", tuple(data))
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
    main2()
