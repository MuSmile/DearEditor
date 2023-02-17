import os, jsonpickle, sqlite3
from PySide6.QtCore import QByteArray, QDataStream

class _Prefs():
	def connect(self, path):
		self.conn = sqlite3.connect(path)

	def doSql(self, cmd, commit = True):
		c = self.conn.cursor()
		c.execute(cmd)
		if commit: self.conn.commit()
		c.close()

	def createTable(self, table):
		self.doSql(f'''
		CREATE TABLE {table} (
		    name STRING PRIMARY KEY
		                UNIQUE
		                NOT NULL,
		    data STRING
		); ''')

	def hasTable(self, table):
		c = self.conn.cursor()
		c.execute(f'SELECT count(*) FROM sqlite_master WHERE type="table" AND name = "{table}"')
		r = c.fetchone()
		c.close()
		return r[0] > 0
		
	def affirmTable(self, table):
		if not self.hasTable(table):
			self.createTable(table)

	def close(self):
		self.conn.close()
		self.conn = None

	def set(self, name, data, table):
		if isinstance(data, str): data = f'"{data}"'
		self.doSql(f'INSERT OR REPLACE INTO {table} VALUES ("{name}", {data});')

	def setBool(self, name, data, table):
		self.set(name, str(data), table)

	def setQVariant(self, name, var, table):
		data = QByteArray()
		stream = QDataStream(data, QIODevice.WriteOnly)
		stream.writeQVariant(var)
		data = str(data.toBase64(), 'utf-8')
		self.set(name, f'b\'{data}\'', table)

	def setObject(self, name, obj, table):
		data = jsonpickle.encode(obj, indent = None)
		self.set(name, data, table)

	def get(self, name, table):
		c = self.conn.cursor()
		c.execute(f'SELECT data FROM {table} WHERE name == "{name}"')
		r = c.fetchone()
		c.close()
		return r and r[0]

	def getBool(self, name, table):
		return self.get(name, table).lower() == 'true'

	def getQVariant(self, name, table):
		r = self.get(name, table)
		if not r: return None
		data = QByteArray.fromBase64(bytes(r[2:-1], 'utf-8'))
		stream = QDataStream(data, QIODevice.ReadOnly)
		return stream.readQVariant()

	def getObject(self, name, table):
		r = self.get(name, table)
		if r: return jsonpickle.decode(r)
		return None

	def remove(self, name, table):
		self.doSql(f'DELETE FROM {table} WHERE name == "{name}"')

	def clear(self, table):
		self.doSql(f'DELETE FROM {table}')

EditorPrefs = _Prefs()
