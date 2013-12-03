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
	coherency int,
	style int,
	UNIQUE(word,foreignKey)
	"""
	createTable = "CREATE TABLE ?(?);"
	insertInto = "INSERT INTO ?(?) VALUES(?)";
	dropTable = "DROP TABLE ?"
	increment = "UPDATE ? SET ? = ? + ? WHERE ? = ?"
	def __init__(self):
		self.getDB()
	def getDB(self):
		if self.db == None:
			self.db = sqlite3.connect(self.DATABASE)
		return self.db
	#word functions
	def select(self,word):
		i = self.db.execute("SELECT * FROM ? WHERE word = ?",(TABLE_PAIRS,word))
		data = i.fetchone()
		
	def getWords(self):
		i = self.db.execute("SELECT * FROM ? WHERE src = ?",(self.TABLE_CHOICES,self.sid))
		return i.fetchall()
	def selectWords(self,a,b):
		i = self.db.execute("SELECT * FROM ? WHERE firstWord = ? &  secondWord = ?",(self.TABLE_PAIRS,a,b))
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
		db.execute(self.createTable,(name,self.SCHEMA_PAIRS))
		return self
	def initChoices(self,name,db):
		db.execute(self.createTable,(name,self.SCHEMA_CHOICES))
		return self
	def init(self):
		db = self.getDB()
		self.initPairs(self.TABLE_PAIRS,db)
		self.initChoices(self.TABLE_CHOICES,db)
		return self
	#insertion
	def insert(self,a,b,c):
		pass
		
	#adjust a value
	def adjust(self,key,val):
		self.db.execute(self.increment,(self.table,key,key,val,"pid",self.sid));
		return self
if __name__ == "__main__":
	a = Author()
	a.selectWords("dog","walk")
	#a.getWords(
