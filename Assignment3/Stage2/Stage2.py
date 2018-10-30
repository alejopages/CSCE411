import mysql.connector
import os
from math import ceil
import json
import traceback
import datetime
import pickle as pkl
from glob import glob

class stage2:


	def __init__(self, dat_dir='./data', max_num_files=2000):
		self.__max_num_files = max_num_files
		self.__dat_dir = os.path.normpath(dat_dir)


	def stepa(self):
		if not os.path.isdir(self.__dat_dir):
			os.mkdir(self.__dat_dir)

		self.__write_db_to_files()


	def stepb(self, table, column):
		'''
		Args:
			table is what table you want to sort
				options are:
					[City, Date, Location, Message, Person, Time, Timestamp]
			column: column to sort by
				options depend on table
		'''

		self.__get_metadata()

		if table not in self.__metadata:
			print("Invalid table name")
			return

		files = glob(os.path.join(self.__dat_dir, table + "_*.dat"))

		data = []
		for file in files:
			with open(file, 'r') as f:
				data.append(json.load(f))

		col_ind = -1
		for i,field in enumerate(self.__metadata[table]['fields']):
			if field[0] == column:
				col_ind = i
				break

		if col_ind == -1:
			print("Invalid column name")
			return

		files = data.sort(key=lambda x: x[col_ind])

		entries_per_file = ceil( float(num_entries) / self.__max_num_files )
		i_ent = 0
		i_file = 0
		temp = []
		for entry in data:
			if i_ent < entries_per_file:
				i_ent += 1
				temp.append(entry)
			else:
				with open("{}_{:06d}.dat".format(table, i_file), 'w') as dat_file:
					self.__dump_json(temp, dat_file)
				temp = []
				i_ent = 0
				i_file += 1

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

			self.__metadata[table] = {
				'num_entries':num_entries,
				'entries_per_file':entries_per_file,
				'fields':fields
			}

			print("TABLE: {}".format(table))
			print("Number of entries: {}".format(num_entries))
			print("Entries per file: {}".format(entries_per_file))

			cur2 = self.__db.cursor()
			cur2.execute("SELECT * FROM " + table)

			i_ent=0
			i_file=0
			dat_file = open(os.path.join(self.__dat_dir, "{}_{:06d}.dat".format(table, 0)), 'w')

			temp = []

			for vals in cur2.fetchall():

				if i_ent == entries_per_file:

					with open(os.path.join(self.__dat_dir, "{}_{:06d}.dat".format(table, i_file)), 'w')\
					as dat_file:
						try:
							self.__dump_json(temp, dat_file)
						except TypeError:
							traceback.print_exc()
							print("For: {}".format(vals))
							pass
						except:
							traceback.print_exc()
							quit()
					temp = []
					i_ent = 0
					i_file += 1

				else:
					temp.append(vals)
					i_ent += 1

		self.__db.close()
		pkl.dump(self.__metadata, open(os.path.join(self.__dat_dir, 'metadata.pkl'), 'wb'))


	def __get_metadata(self):
		if hasattr(self, '__metadata'):
			return
		elif os.path.isfile(os.path.join(self.__dat_dir, "metadata.pkl")):
			self.__metadata = pkl.load(open(os.path.join(self.__dat_dir, "metadata.pkl"), 'rb'))
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

		try:
			if isinstance(vals[0][1], datetime.date) \
			  or isinstance(vals[0][1], datetime.timedelta) \
			  or isinstance(vals[0][1], datetime.time):
				json.dump([(val[0], str(val[1])) for val in vals], dat_file)

			else:
				json.dump(vals, dat_file)

		except Exception as e:
			print("Error dumping json")
			raise e
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
