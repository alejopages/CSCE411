import mysql.connector
from sys import exit

import parser
import dbCredentials

def main():
    if dbCredentials.USER == '' or dbCredentials.HOST == '' or dbCredentials.DATABASE == '':
        exit("ERROR: PLEASE ENTER DB INFORMATION IN dbCredentials")

    DATA_FILEPATH = "data.txt"
    data = parser.loadData(DATA_FILEPATH)
    print("DATA SUCCESSFULLY LOADED\n--------------------------------------")

    exportData(data)
    print("DATA SUCCESSFULLY EXPORTED\n--------------------------------------")

    # for entry in data:
        # messages = entry["messages"]
        # for message in messages:
            # print(message["value"])
#
    return


def exportData(data):
    connection = getDbConnection()
    cursor = connection.cursor()

    for entry in data:
        print("PROCESSING ENTRY WITH ID: " + entry["id"])
        exportPerson(connection, cursor, entry)
        messages = entry["messages"]
        print("# MESSAGES: " + str(len(messages)))
        if len(messages) > 0:
            exportMessages(connection, cursor, entry["id"], messages)
        connection.commit()

    cursor.close()
    connection.close()
    return

def exportMessages(connection, cursor, personId, messages):

    for message in messages:
        exportMessage(connection, cursor, personId, message)

    return

def exportMessage(connection, cursor, personId, message):
    # print("PROCESSING MESSAGE WITH DATE/TIME: " + message["date"] + " - " \
            # + message["time"])
    if "date" not in message:
        return

    date = message["date"]
    time = message["time"]
    if date == "" or time == "" or message == "":
        return
    exportTimestamp(connection, cursor, date, time)

    sql = "insert into `Message` (value, personId, timestampId) " \
    + "select (%s), P.id, TS.id " \
    + "from `Person` P, `Timestamp` TS, `Date` D, `Time` T " \
    + "where P.idStr = (%s) " \
    + "and TS.dateId = D.id " \
    + "and D.value = (%s) " \
    + "and TS.timeId = T.id " \
    + "and T.value = (%s)" \

    values = (message["value"], personId, date, time)
    cursor.execute(sql, values)

    return

def exportTimestamp(connection, cursor, date, time):
    exportDate(connection, cursor, date)
    exportTime(connection, cursor, time)

    sql = "insert into `Timestamp` (dateId, timeId) " \
            + "select D.id, T.id " \
            + "from `Date` D, `Time` T " \
            + "where D.value = (%s) " \
            + "and T.value = (%s)" \

    values = (date, time)
    try:
        if (date != "") and (time != ""):
            cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        # print("Values: (" + date + " - " + time + ") already in DB")
        return

    return

def exportDate(connection, cursor, date):
    if date == "":
        return

    sql = "insert into Date (value) values (%s)"
    values = (date,)

    try:
        cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        # print("Value: " + date + " already in DB")
        return

    return

def exportTime(connection, cursor, time):
    if time == "":
        return

    sql = "insert into Time (value) values (%s)"
    values = (time,)

    try:
        cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        # print("Value: " + time + " already in DB")
        return

    return

def exportPerson(connection, cursor, person):
    if ("state" in person) and ("city" in person):
        state = person["state"]
        city = person["city"]
        exportLocation(connection, cursor, state, city)

        sql = "insert into `Person` (idStr, name, locationId) " \
                + "select (%s), (%s), L.id " \
                + "from Location L, State S, City C " \
                + "where S.name =  (%s) " \
                + "and C.name = (%s) " \
                + "and L.stateId = S.id " \
                + "and L.cityId = C.id"

        values = (person["id"], person["name"], state, city)
    else:
        sql = "insert into `Person` (idStr, name) " \
                + "values (%s, %s)" \

        values = (person["id"], person["name"])

    try:
        cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        return
        # print("User: (" + person["id"] + " - " \
                # + person["name"] + ") already in DB")

    return


def exportLocation(connection, cursor, state, city):
    exportState(connection, cursor, state)
    exportCity(connection, cursor, city)

    sql = "insert into Location (stateId, cityId) " \
            + "select S.id, C.id " \
            + "from State S, City C " \
            + "where S.name = (%s) " \
            + "and C.name = (%s)"

    values = (state, city)
    try:
        cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        # print("Values: (" + state + " - " + city + ") already in DB")
        return

    return

def exportState(connection, cursor, name):
    if name == "":
        return

    sql = "insert into State (name) values (%s)"
    values = (name,)

    try:
        cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        # print("Value: " + name + " already in DB")
        return

    return


def exportCity(connection, cursor, name):
    if name == "":
        return

    sql = "insert into City (name) values (%s)"
    values = (name,)
    try:
        cursor.execute(sql, values)
    except mysql.connector.errors.IntegrityError as ie:
        # print("Value: " + name + " already in DB")
        return

    return

def getDbConnection():
	connection = mysql.connector.connect()

	try:
		connection = mysql.connector.connect(
        user=dbCredentials.USER, password=dbCredentials.PASSWORD,
		host=dbCredentials.HOST, database=dbCredentials.DATABASE)

	except mysql.connector.Error as err:
		if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
		    exit("Something is wrong with your user name or password")
		elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
		    exit("Database does not exist")
		else:
		    exit(err)

	return connection

if __name__ == '__main__':
	main()
