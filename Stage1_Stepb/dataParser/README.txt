# =============================================================================
# HOW TO LOAD THE DATABASE
# =============================================================================
Go into data folder:
	cd data/
Run this command:
	./fileRangeReader 0 1999 > data.txt
Move data.txt upward into the dataParser folder:
	mv data.txt ../
Move upward into the dataParser folder:
	cd ../
run dbLoader.py:
	python3 dbLoader.py
