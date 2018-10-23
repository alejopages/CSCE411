import mysql.connector
import os
from math import ceil
import struct


class Stage2:

    def __init__(self, data_dir='./data', max_num_files=2000):
        self.data_dir = data_dir
        self.__max_num_files = max_num_files


    def write_db_to_files(self):
        self.__connect_db()

        if not hasattr(self, "__tables"):
            self.__fetch_tables()

        for (table,) in self.__tables:
            fields = self.__get_table_columns()

            


    def __get_table_columns(self, table):
        cur = self.__db.cursor()
        cur.execute("DESC " + table)
        fields = cur.fetchall()
        return fields


    def __fetch_tables(self):

        if not hasattr(self, "__db"):
            self.__connect_db()

        cur1 = self.__db.cursor()
        cur1.execute('SHOW TABLES')
        self.__tables = cur1.fetchall()
        cur1.close()


    def __write_table_to_file(self, table):
        return


    def __connect_db(self):

        config = {
            'user': 'cfarmer',
            'password': 'eKd65T',
            'host': 'cse.unl.edu',
            'database': 'cfarmer'
        }

        try:
            self.__db = mysql.connector.connect(**config)
        except Exception as e:
            print('Could not connect to database')
            raise e


def main():

    # default constants
    max_num_files = 2000
    dat_dir = os.path.normpath('./data')

    oper = Stage2()

    oper.write_db_to_files()
    quit()

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

            dat_file.write(bytes(dat))

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
