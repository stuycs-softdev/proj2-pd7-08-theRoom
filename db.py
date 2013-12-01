import sqlite3
class Author:
	table = None
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
			self.db = sqlite3.connect(self.DATABASE)
		return self.db
	def select(self,table,id):
		self.sid = id
		self.table = table
		i = self.db.execute("SELECT * FROM %s WHERE pid = %s"%(table,id))
		return i.fetchone()
	def getWords(self):
		i = self.db.execute("SELECT * FROM %s WHERE src = %s"%(self.TABLE_CHOICES,self.sid))
		return i.fetchall()
	def selectWords(a,b):
		i = self.db.execute("SELECT * FROM %s WHERE firstWord = %s &  secondWord = %s"%(self.TABLE_PAIRS,a,b))
		data = i.fetchone()
		self.sid = data[0]
		self.table = self.TABLE_PAIRS
		return data
	def reset(self,db):
		self.dropTable("*",db)
		return self
	def dropTable(self,table,db):
		db.execute(self.dropTable%table)
		return self
	def initPairs(self,name,db):
		db.execute(self.createTable%(name,self.SCHEMA_PAIRS))
		return self
	def initChoices(self,name,db):
		db.execute(self.createTable%(name,self.SCHEMA_CHOICES))
		return self
	def init(self):
		db = self.getDB()
		self.initPairs(self.TABLE_PAIRS,db)
		self.initChoices(self.TABLE_CHOICES,db)
		return self
	def add(self,val,key):
		self.db.execute(self.increment%(table,key,key,val,"pid",sid));
		return self
if __name__ == "__main__":
	a = Author()
	print a.getDB()
