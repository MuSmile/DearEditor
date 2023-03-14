"""This module provide database manipulating toolkit.

Typical usage example:

.. code-block:: python
   :linenos:

   db = Database()
   db.connect('some/path/to/sample.db')
   db.affirmTable('foo')
   db.setBool('bool_test', True, 'foo')
   db.setObject('obj_test', {'hello':'world'}, 'foo')
   obj = db.getObject('obj_test', 'foo')
   print(obj)
   # db.clear('foo')
   db.close()
"""

import os, jsonpickle, sqlite3
from PySide6.QtCore import QByteArray, QDataStream

class Database:
	"""Represent a database object powered by sqlite3.

	Provide basic interface of database manipulating,
	including a set of setters, getters, and other useful utils.
	"""

	def connect(self, path):
		"""Load database of specified path.
		
		Args:
			str path: Source database path.
		"""
		self.conn = sqlite3.connect(path)

	def close(self):
		"""Close a connected database.
		"""
		self.conn.close()
		del self.conn

	####################  OPERATE  ###################
	def doSql(self, cmd, commit = True):
		"""Execute specified sql command.
		
		Args:
			str cmd: Specified command to execute.
			bool commit: Commit database operation.
		"""
		c = self.conn.cursor()
		c.execute(cmd)
		if commit: self.conn.commit()
		c.close()

	def createTable(self, table):
		"""Create a database with specified name.
		
		Args:
			str table: Table name to create.
		"""
		self.doSql(f'''
		CREATE TABLE {table} (
		    name STRING PRIMARY KEY
		                UNIQUE
		                NOT NULL,
		    data STRING
		); ''')

	def hasTable(self, table):
		"""Check if has certain database table.
		
		Args:
			str table: Table name to check.

		Returns:
			bool: Contains certain table or not.
		"""
		c = self.conn.cursor()
		c.execute(f'SELECT count(*) FROM sqlite_master WHERE type="table" AND name = "{table}"')
		r = c.fetchone()
		c.close()
		return r[0] > 0
		
	def affirmTable(self, table):
		"""Affirm a certain database table.

		If table not exist, will create a new one.
		
		Args:
			str table: Table name to affirm.
		"""
		if not self.hasTable(table):
			self.createTable(table)

	def dropTable(self, table):
		"""Drop a certain database table.

		Args:
			str table: Table name to drop.
		"""
		self.doSql(f'DROP TABLE {table}')

	def clearTable(self, table):
		"""Clear a certain database table's content.

		Args:
			str table: Table name to clear.
		"""
		self.doSql(f'DELETE FROM {table}')

	def remove(self, name, table):
		"""Remove an entry in certain database table.

		Args:
			str name: Entry primary key to remove.
			str table: Table name to operate.
		"""
		self.doSql(f'DELETE FROM {table} WHERE name == "{name}"')

	####################  SETTERS  ####################
	def set(self, name, data, table):
		"""Set an entry data in certain database table.

		Args:
			str name: Entry primary key to set.
			any data: Data to set, will be implicit converted str.
			str table: Table name to operate.
		"""
		if isinstance(data, str): data = f'"{data}"'
		self.doSql(f'INSERT OR REPLACE INTO {table} VALUES ("{name}", {data});')

	def setBool(self, name, data, table):
		"""Set an boolean data in certain database table.

		Args:
			str name: Entry primary key to set.
			bool data: Boolean data to set.
			str table: Table name to operate.
		"""
		self.set(name, str(data), table)

	def setQVariant(self, name, data, table):
		"""Set an QVariant variable in certain database table.

		Args:
			str name: Entry primary key to set.
			QVariant Data: QVariant data to set.
			str table: Table name to operate.
		"""
		data = QByteArray()
		stream = QDataStream(data, QIODevice.WriteOnly)
		stream.writeQVariant(var)
		data = str(data.toBase64(), 'utf-8')
		self.set(name, f'b\'{data}\'', table)

	def setObject(self, name, obj, table):
		"""Set an object in certain database table.

		Args:
			str name: Entry primary key to set.
			object obj: Object data to set, will be serialized into json string.
			str table: Table name to operate.
		"""
		data = jsonpickle.encode(obj, indent = None)
		self.set(name, data, table)

	####################  GETTERS  ####################
	def get(self, name, table):
		"""Get an entry data in certain database table.
		
		Args:
			str name: Entry primary key to get.
			str table: Table name to get.

		Returns:
			str: Found entry data.
		"""
		c = self.conn.cursor()
		c.execute(f'SELECT data FROM {table} WHERE name == "{name}"')
		r = c.fetchone()
		c.close()
		return r and r[0]

	def getBool(self, name, table):
		"""Get an boolean data in certain database table.
		
		Args:
			str name: Fntry primary key to get.
			str table: Fable name to get.

		Returns:
			bool: Found entry data.
		"""
		return self.get(name, table).lower() == 'true'

	def getQVariant(self, name, table):
		"""Get an QVariant data in certain database table.
		
		Args:
			str name: Entry primary key to get.
			str table: Table name to get.

		Returns:
			QVariant: Found entry data.
		"""
		r = self.get(name, table)
		if not r: return None
		data = QByteArray.fromBase64(bytes(r[2:-1], 'utf-8'))
		stream = QDataStream(data, QIODevice.ReadOnly)
		return stream.readQVariant()

	def getObject(self, name, table):
		"""Get an object data in certain database table.
		
		Args:
			str name: Entry primary key to get.
			str table: Table name to get.

		Returns:
			object: Found entry data.
		"""
		r = self.get(name, table)
		if r: return jsonpickle.decode(r)
		return None

