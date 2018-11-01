import mysql.connector
import os
from math import ceil
import json
import traceback
import datetime
import Stage2
import sys
from glob import glob

def main():
	sb = Stage2.stage2()
	sb.stepb('State', 'name')

	files = glob(r'C:\data\State_*_sorted.dat')
	reg = glob(r'C:\data\State_*.dat')
	files.sort()
	reg.sort()
	print([json.load(open(file, 'r')) for file in files])
	print([json.load(open(file, 'r')) for file in reg])

	return
	print("Bin search State for {}".format(sys.argv[1]))
	print(sb.file_binary_search('State', sys.argv[1], 'name'))

if __name__ == '__main__':
	main()
