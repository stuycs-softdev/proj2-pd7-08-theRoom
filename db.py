import sqlite3
from document import doc

class Author:
	table = None
	sid = None
	db = None
	conn = None	
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
	insertInto = "INSERT INTO %s(%s) VALUES(%s)"
	dTable = "DROP TABLE %s"
	increment = "UPDATE %s SET %s = %s + %s WHERE %s = '%s'"
	def __init__(self):
		self.getDB()
	def getDB(self):
		if self.db is None or self.conn is None:
			self.conn = sqlite3.connect(self.DATABASE)
			self.db = self.conn.cursor()
		return self.db
	#word functions
	def select(self,word,srcid = None):
		if srcid is None:
			srcid = self.sid
		sql = "SELECT * FROM %s WHERE word = ? AND src = ?"%self.TABLE_CHOICES
		i = self.db.execute(sql,(word,srcid))
		data = i.fetchone()
		if data is not None:
			self.sid = data[0]
			self.table = self.TABLE_CHOICES
		return data
	def getWords(self,pid = None):
		if pid is None:
			pid = self.sid
		i = self.db.execute("SELECT * FROM %s WHERE src = %s"%(self.TABLE_CHOICES,pid))
		return i.fetchall()
	def selectWords(self,a,b):
		i = self.db.execute("SELECT * FROM %s WHERE firstWord = ? AND secondWord = ?"%(self.TABLE_PAIRS),(a,b))
		data = i.fetchone()
		if data is not None:
			self.sid = data[0]
			self.table = self.TABLE_PAIRS
		return data
	def getPairs(self,a):
		i = self.db.execute("SELECT firstWord,secondWord FROM %s WHERE firstWord = ? "%(self.TABLE_PAIRS),(a,b))
		data = i.fetchall()
		return data
		
	#resets db
	def reset(self):
		self.dropTable(self.TABLE_PAIRS)
		self.dropTable(self.TABLE_CHOICES)
		return self
	#drops a table
	def dropTable(self,table):
		self.db.execute(self.dTable%table)
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
		if exists is None:
			self.db.execute(self.insertInto%(self.TABLE_PAIRS,"firstWord,secondWord","?,?"),(a,b))
			self.sid = self.db.lastrowid
			self.table = self.TABLE_PAIRS
		exists = self.select(c)
		if exists is not None:
			self.adjust("freq",1)
		else:
			self.selectWords(a,b)
			self.db.execute(self.insertInto%(self.TABLE_CHOICES,"src,word,freq","?,?,?"),(self.sid,c,1))
		return self
	#everything
	def everything(self):
		ans = {}
		sql = "SELECT * FROM %s"%self.TABLE_PAIRS
		pairs = self.db.execute(sql).fetchall()
		for pair in pairs:
			first = pair[1]
			second = pair[2]
			self.selectWords(first,second)
			choices = self.getWords()
			formatted = {}
			for choice in choices:
				formatted[choice[2]] = choice[3]
			ans[(first,second)] = formatted
		return ans
		
	#adjust a value
	def adjust(self,key,val):
		self.db.execute(self.increment%(self.table,key,key,val,"pid",self.sid));
		return self
	#save
	def save(self):
		self.conn.commit()
	def __del__(self):
		self.save()
		self.db = None
		sekf.conn = None
if __name__ == "__main__":
	a = Author()
	a.reset()
	a.init()
	#a.getWords(
