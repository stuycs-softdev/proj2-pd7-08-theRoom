import sqlite3

DATABASE = "author.db"
SCHEMA = """
"""

createTable = "CREATE TABLE %s(%s);"
insertInto = "INSERT INTO %s(%s) VALUES(%s)";

def getDB():
	return sqlite3.connect(DATABASE)

def initTable(name,db):
	db.execute(createTable%(name,
if __name__ == "__main__":
	print getDB()
