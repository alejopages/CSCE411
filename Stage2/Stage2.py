import mysql.connector
import os
from math import ceil
import json
import traceback
import datetime
import pickle as pkl


class stage2:


	def __init__(self, dat_dir='./data', max_num_files=2000):
		self.__max_num_files = max_num_files
		self.__dat_dir = dat_dir


	def stepa(self):
		if not os.path.isdir(self.__dat_dir):
			os.mkdir(self.__dat_dir)

		self.write_db_to_files()


	def stepb(self):
		return


	def __write_db_to_files(self):
		self.__connect_db()

		if not hasattr(self, "__tables"):
			self.__fetch_tables()

		print("Tables in database:\n{}".format(self.__tables))

		self.__metadata = {}

		for (table,) in self.__tables:
			cur1 = self.__db.cursor()
			cur1.execute("SELECT COUNT(*) FROM " + table)
			num_entries = cur1.fetchone()[0]

			entries_per_file = ceil( float(num_entries) / self.__max_num_files )

			fields = self.__get_table_columns(table)

			metadata[table] = {
				'num_entries':num_entries,
				'entries_per_file':entries_per_file,
				'fields':fields
			}

			print("TABLE: {}".format(tabls))
			print("Number of entries: {}".format(num_entries))
			print("Entries per file: {}".format(entries_per_file))

			cur2 = self.__db.cursor()
			cur2.execute("SELECT * FROM " + table)

			i_ent=0
			i_file=0
			dat_file = open(os.path.join(self.__dat_dir, "{}_{:06d}.dat".format(table, 0)), 'w')

			for vals in cur2.fetchall():

				if i_ent == entries_per_file:
					i_ent = 0
					i_file += 1
					dat_file.close()
					dat_file = open(os.path.join(self.__dat_dir, "{}_{:06d}.dat".format(table, i_file)), 'w')
				else:
					i_ent += 1

				try:
					self.__dump_json(vals, dat_file)
				except TypeError:
					traceback.print_exc()
					print("For: {}".format(vals))
					pass
				except:
					traceback.print_exc()
					quit()

			dat_file.close()

		self.__db.close()
		pkl.dump(self.__metadata, open(os.path.join(self.__dat_dir, 'metadata.pkl'), 'wb'))


	def get_metadata(self):
		if hasattr(self, '__metadata'):
			return
		elif os.path.isfile(os.path.join(self.__dat_dir, "metadata.pkl")):
			self.__metadata = pkl.load(os.path.join(self.__dat_dir, "metadata.pkl"))
		else:
			self.__connect_db()
			self.__fetch_tables()

			self.__metadata = {}

			for (table,) in self.__tables:

				cur1 = self.__db.cursor()
				cur1.execute("SELECT COUNT(*) FROM " + table)
				num_entries = cur1.fetchone()[0]
				entries_per_file = ceil( float(num_entries) / self.__max_num_files )

				self.__metadata[table] = {
					'num_entries':num_entries,
					'entries_per_file':entries_per_file,
					'fields':self.__get_table_columns(table)
				}

				pkl.dump(self.__metadata, open(os.path.join(self.__dat_dir, 'metadata.pkl'), 'wb'))

		return self.__metadata


	def __dump_json(self, vals, dat_file):
		if isinstance(vals[1], datetime.date) \
		  or isinstance(vals[1], datetime.timedelta) \
		  or isinstance(vals[1], datetime.time):
			json.dump((vals[0], str(vals[1])), dat_file)

		else:
			json.dump(vals, dat_file)

		return


	def __get_table_columns(self, table):

		cur = self.__db.cursor()
		cur.execute("DESC " + table)
		fields = cur.fetchall()
		cur.close()

		return tuple([field for field in fields])


	def __fetch_tables(self):

		if hasattr(self, '__tables'):
			return

		self.__connect_db()
		cur1 = self.__db.cursor()
		cur1.execute('SHOW TABLES')
		self.__tables = cur1.fetchall()
		cur1.close()
		return


	def __connect_db(self):

		if hasattr(self, '__db'):
			if self.__db.open:
				return

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
