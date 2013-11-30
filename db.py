import sqlite3

DATABASE = "author.db"
SCHEMA_DOUBLES = """
pid int primaryKey,
firstWord varchar(255),
secondWord varchar(255),
UNIQUE(firstWord, secondWord)
"""
SCHEMA_THIRD = """
pid int primaryKey,
src int foreignKey,
word varchar(255),
freq int,
coherency int,
style int
"""
createTable = "CREATE TABLE %s(%s);"
insertInto = "INSERT INTO %s(%s) VALUES(%s)";

def getDB():
	return sqlite3.connect(DATABASE)

def initTable(name,db):
	db.execute(createTable%(name,
if __name__ == "__main__":
	print getDB()
