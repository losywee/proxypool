# coding: utf-8
__author__ = 'Moruy'

import sqlite3
import random
# from Util 

class SqliteClient(object):
	"""docstring for SqliteClient"""

	def __init__(self, name, **kwargs):
		self.__table_name = "tb_proxy"
		self.name = self.__table_name + str(name)
		self.__conn = sqlite3.connect(name, check_same_thread = False)
		self.__cursor = self.__conn.cursor()
		self.__cursor.execute("CREATE TABLE IF NOT EXISTS {tb} (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT NOT NULL);".format(tb = self.name))

	def get(self):
		self.__cursor.execute('SELECT item FROM {tb} ORDER BY RANDOM() LIMIT 1'.format(tb = self.name))
		r = self.__cursor.fetchone()
		if len(r) > 0:
			return r[0]
		else:
			return None
	def put(self, proxy, num=1):
		self.__cursor.execute('INSERT INTO {tb} (item) VALUES ("{proxy}")' . format(tb = self.name, proxy = proxy))
		self.__conn.commit()
		return self.__conn.total_changes
		
	def delete(self, key):
		self.__cursor.execute('DELETE FROM {tb} WHERE item == "{key}"' . format(tb = self.name, key = key))
		self.__conn.commit()

	def pop(self):
		self.__cursor.execute('SELECT id,item FROM {tb} ORDER BY RANDOM() LIMIT 1' . format( tb = self.name))
		r = self.__cursor.fetchone()
		if r:
			val = r[1]
			row_id = r[0]
			self.__cursor.execute('DELETE FROM {tb} WHERE id = {row_id}' . format( tb = self.name, row_id = row_id))
			self.__conn.commit()
			return {'proxy': val,
                    'value': row_id}
		else:
			return None
	def update(self, key, value):
		self.__cursor.execute('UPDATE {tb} SET item = {item} WHERE item = "{key}"' . format(tb = self.name, item = value, key = key))
		self.__conn.commit()


	def exists(self, key):
		self.__cursor.execute('SELECT item FROM {tb} WHERE item = "{key}"' . format(tb = self.name, key = key))
		r = self.__cursor.fetchone()
		if r:
			return True
		else:
			return False

	def getAll(self):
		self.__cursor.execute('SELECT * FROM {tb}' . format(tb = self.name))
		r = self.__cursor.fetchall()
		dic_r = {}
		for x in range(0, len(r)):
			res_im = r[x]
			dic_r[res_im[1]] = res_im[0]
		return dic_r

	def getNumber(self):
		self.__cursor.execute('SELECT COUNT(id) as count FROM {tb}' . format(tb = self.name))
		r = self.__cursor.fetchone()
		return r[0]

	def changeTable(self, name):
		print(name)
		self.name = self.__table_name + str(name)
		self.__cursor.execute("CREATE TABLE IF NOT EXISTS {tb} (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT NOT NULL);".format(tb = self.name))

if __name__ == '__main__':
	sqlite = SqliteClient(name='useful_proxy', host='127.0.0.1', port=8899, username = "root", password=None)
	print(sqlite.getAll())
	# print(sqlite.getNumber())
	# print(sqlite.exists("12333333"))
	# print(sqlite.update("12333333", "123434"))
	# print(sqlite.pop())
	# sqlite.delete('1111')
	# print(sqlite.put("123.0.22.31:80"))
	# print(sqlite.get())



