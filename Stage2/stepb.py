import MySQLdb

def main():
  max_files = 2000

  try:
    db = connect_db()
  except Exception as e:
    quit("Quitting")

  db.query("SHOW DATABASES")

  return


def connect_db():
  try:
      db = MySQLdb.connect(
      host="cse.unl.edu",
      user="apages",
      passwd="Wtpt4R",
      db="apages"
    )
  except Exception as e:
    print("Could not connect to DB. {}".format(e))
    raise e
  return db




if __name__ == '__main__':
  main()
