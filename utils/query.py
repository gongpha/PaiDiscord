import pymysql.cursors
from time import time

def fetchone(connection, sql, list = None) :
	try :
		with connection.cursor() as cursor :
			f = time()
			cursor.execute(sql, list)
			s = time()
		used = s - f
		print('Query Executed "{}"'.format(sql))
		return {
			"result" : cursor.fetchone(),
			"time" : used,
			"rows" : cursor.rowcount
		}
	except pymysql.err.Error :
		print('Query Failed to execute "{}"'.format(sql))
		return None

def commit(connection, sql, list = None) :
	try :
		with connection.cursor() as cursor :
			f = time()
			cursor.execute(sql, list)
			s = time()
		used = s - f
		print('Query Executed "{}"'.format(sql))
		connection.commit()
		return used
	except pymysql.err.Error as e:
		print('Query Failed to execute "{}" :\n{}'.format(sql,e))
		return None
