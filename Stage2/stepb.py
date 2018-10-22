import mysql.connector
import os
from math import ceil


def main():

    # default constants
    max_num_files = 2000
    dat_dir = os.path.normpath('./data')

    try:
        db = connect_db()
    except:
        quit()

    cur = db.cursor()
    count_cur = db.cursor()
    table_cur = db.cursor()

    cur.execute('SHOW TABLES')

    for table in cur.fetchall():

        print("Fetching from {}".format(table[0]))

        count_cur.execute("SELECT COUNT(*) FROM " + table[0])
        num_entries = count_cur.fetchall()[0][0]
        num_entries_per_file = ceil(num_entries / max_num_files)

        table_cur.execute("SELECT * FROM " + table[0])

        i = 0
        entries_per_file_counter = 0
        dat_file = open(os.path.join(dat_dir, "{}_{:06d}.dat".format(table[0], 0)), 'wb')

        for vals in table_cur.fetchall():

            if entries_per_file_counter == num_entries_per_file:
                dat_file.close()
                dat_file = open(os.path.join(dat_dir, "{}_{:06d}.dat".format(table[0], i)), 'wb')
                entries_per_file_counter = 0
            else:
                entries_per_file_counter += 1

            dat = stringifyVals(vals)

            dat_file.write(dat.encode())

    db.close()
    return


def stringifyVals(vals):
    string = ""
    for val in vals:
        string += " " + str(val) + " "
    return string

def connect_db():

    config = {
        'user': 'cfarmer',
        'password': 'eKd65T',
        'host': 'cse.unl.edu',
        'database': 'cfarmer'
    }

    try:
        db = mysql.connector.connect(**config)
    except Exception as e:
        print('Could not connect to database: {}'.format(e))
        raise e

    return db


if __name__ == '__main__':

    main()
