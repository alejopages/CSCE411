import mysql.connector

def connect_db():
  try:
    db = mysql.connector.connect(
      host="cse.unl.edu",
      user="cfarmer",
      password="..."
    )
  except Exception as e:
    print("Could not connect to DB. {}".format(e))
    raise e
  return db

def main():
  max_files = 2000

  try:
    db = connect_db
  except Exception as e:
    quit("Quitting")

  cr = db.cursor()

  cr.execute("SHOW DATABASES")

  return

if __name__ == '__main__':
  main()
