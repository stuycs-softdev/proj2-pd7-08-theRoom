import sqlite3
class Author:

	sid = None
	db = None
	
	DATABASE = "author.db"
	TABLE_PAIRS = "pairs"
	TABLE_CHOICES = "choices"


	SCHEMA_PAIRS = """
	pid integer primary key autoincrement,
	firstWord varchar(255),
	secondWord varchar(255),
	UNIQUE(firstWord, secondWord)
	"""
	SCHEMA_CHOICES = """
	pid integer primary key autoincrement,
	src int foreignKey,
	word varchar(255),
	freq int,
	coherency int,
	style int,
	UNIQUE(word,foreignKey)
	"""
	createTable = "CREATE TABLE %s(%s);"
	insertInto = "INSERT INTO %s(%s) VALUES(%s)";
	dropTable = "DROP TABLE %s"
	increment = "UPDATE %s SET %s = %s + %s WHERE %s = %s"
	def getDB(self):
		if self.db == None:
			return sqlite3.connect(DATABASE)
		else:
			return 
	def reset(self,db):
		self.dropTable("*",db)
	def dropTable(self,table,db):
		db.execute(self.dropTable%table)
	def initPairs(self,name,db):
		db.execute(self.createTable%(name,self.SCHEMA_PAIRS))
		return db
	def initChoices(self,name,db):
		db.execute(self.createTable%(name,self.SCHEMA_CHOICES))
		return db
	def init(self):
		db = self.getDB()
		self.initPairs(TABLE_PAIRS,db)
		self.initChoices(TABLE_CHOICES,db)
		return db
	def increment(self,val,key):
		self.db.execute(self.increment
if __name__ == "__main__":
	a = Author()
	print a.getDB()
