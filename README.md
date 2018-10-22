CSCE 411 - assignments

Stage 2:

  Tech:
     mysql connection in python:
     
      conda install -c anaconda mysql-connector-python
      or
      pip instal mysql-connector-python

  * step a:
      Define:
        n: max number of files (default = 2,000)
        m: number of records in table
        num records per file = ceil( m / n )

        naming convention:
          <table name>_######.dat

        Script to read from database into files:
          connect to mysql
          count number of records in table
          determine number of recs per file and number of a files
          pull all records from table (100? at a time)
          write records to files


      * step b:
