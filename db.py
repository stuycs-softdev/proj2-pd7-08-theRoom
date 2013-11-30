import sqlite3

DATABASE = "author.db"
TABLE_PAIRS = "pairs"
TABLE_CHOICES = "choices"


SCHEMA_PAIRS = """
pid int primaryKey autoincrement,
firstWord varchar(255),
secondWord varchar(255),
UNIQUE(firstWord, secondWord)
"""
SCHEMA_CHOICES = """
pid int primaryKey autoincrement,
src int foreignKey,
word varchar(255),
freq int,
coherency int,
style int,
UNIQUE(word,foreignKey)
"""
createTable = "CREATE TABLE %s(%s);"
insertInto = "INSERT INTO %s(%s) VALUES(%s)";

def getDB():
	return sqlite3.connect(DATABASE)

def initPairs(name,db):
	db.execute(createTable%(name,SCHEMA_PAIRS))
	return db
def initChoices(name,db):
	db.execute(createTable%(name,SCHEMA_CHOICES))
	return db
def init():
	db = getDB()
	initPairs(TABLE_PAIRS,db)
	initChoices(TABLE_CHOICES,db)
	return db

def increment(val,key):

if __name__ == "__main__":
	print getDB()
