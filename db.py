import sqlite3
import document

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
	UNIQUE(word,src)
	"""
	createTable = "CREATE TABLE %s(%s);"
	insertInto = "INSERT INTO %s(%s) VALUES(%s)";
	dropTable = "DROP TABLE %s"
	increment = "UPDATE %s SET %s = %s + %s WHERE %s = %s"
	def __init__(self):
		self.getDB()
	def getDB(self):
		if self.db == None:
			self.db = sqlite3.connect(self.DATABASE).cursor()
		return self.db
	#word functions
	def select(self,word,srcid = None):
		if srcid is None:
			srcid = self.sid
		i = self.db.execute("SELECT * FROM %s WHERE word = %s AND src = %s"%(TABLE_CHOICES,word,srcid))
		data = i.fetchone()
		if data[0] is not None:
			self.sid = data[0]
			self.table = TABLE_CHOICES
		return data
	def getWords(self):
		i = self.db.execute("SELECT * FROM %s WHERE src = %s"%(self.TABLE_CHOICES,self.sid))
		return i.fetchall()
	def selectWords(self,a,b):
		i = self.db.execute("SELECT * FROM %s WHERE firstWord = %s AND secondWord = %s"%(self.TABLE_PAIRS,a,b))
		data = i.fetchone()
		self.sid = data[0]
		self.table = self.TABLE_PAIRS
		return data
	
	#resets db
	def reset(self):
		self.dropTable("*")
		return self
	#drops a table
	def dropTable(self,table):
		self.db.execute(self.dropTable%table)
		return self
	
	#initializes tables
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
	#insertion
	def insert(self,a,b,c):
		exists = self.selectWords(a,b)
		if exists[0] is not None:
			self.db.execute(self.insertInto%(TABLE_PAIRS,"firstWord,secondWord","%s,%s"%(a,b)))
			self.sid = self.db.lastrowid
			self.table = TABLE_PAIRS
		exists = self.select(c)
		if exists[0] is not None:
			self.adjust("freq",1)
		else:
			self.selectWords(a,b)
			self.db.execute(self.insertInto%(TABLE_CHOICES,"src,word,freq","%s,%s,%s"%(self.sid,c,0)))
		return self
	#adjust a value
	def adjust(self,key,val):
		self.db.execute(self.increment,(self.table,key,key,val,"pid",self.sid));
		return self
if __name__ == "__main__":
	a = Author()
	a.reset()
	a.init()
	#a.getWords(
