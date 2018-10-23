import mysql.connector
import os
from math import ceil
import struct
import pickle as pkl
import json


class Stage2:

    def __init__(self, dat_dir='./data', max_num_files=2000):
        self.__dat_dir = dat_dir
        self.__max_num_files = max_num_files


    def write_db_to_files(self):
        self.__connect_db()

        if not hasattr(self, "__tables"):
            self.__fetch_tables()

        for (table,) in self.__tables:
            cur1 = self.__db.cursor()
            cur1.execute("SELECT COUNT(*) FROM " + table)
            num_entries = cur1.fetchone()[0]

            entries_per_file = ceil( float(num_entries) / self.__max_num_files )

            cur2 = self.__db.cursor()
            cur2.execute("SELECT * FROM " + table)

            i_ent=0
            i_file=0
            dat_file = open(os.path.join(self.__dat_dir, "{}_{:06d}.dat".format(table, 0)), 'w')

            for vals in cur2.fetchall():

                if i_ent == entries_per_file:
                    i_ent = 0
                    dat_file.close()
                    dat_file = open(os.path.join(self.__dat_dir, "{}_{:06d}.dat".format(table, i_file)), 'w')
                else:
                    i_ent += 1

                json.dump(vals, dat_file)

            dat_file.close()


    def __get_table_columns(self, table):
        cur = self.__db.cursor()
        cur.execute("DESC " + table)
        fields = cur.fetchall()
        cur.close()
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

    thing = Stage2()
    thing.write_db_to_files()



if __name__ == '__main__':

    main()
