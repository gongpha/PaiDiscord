import pymysql.cursors
from time import time

def fetchone(bot, sql, list = None) :
	connection = bot.connect_db()
	try :
		with connection.cursor() as cursor :
			f = time()
			cursor.execute(sql, list)
			s = time()
		used = s - f
		print('Query Executed "{}"'.format(sql % (list)))
		return {
			"result" : cursor.fetchone(),
			"time" : used,
			"rows" : cursor.rowcount
		}
	except pymysql.err.Error as e:
		print('Query Failed to execute "{}" :\n{}'.format(sql % (list),e))
		return None
	finally :
		connection.close()

def commit(bot, sql, list = None) :
	connection = bot.connect_db()
	try :
		with connection.cursor() as cursor :
			f = time()
			cursor.execute(sql, list)
			s = time()
		used = s - f
		print('Query Executed "{}"'.format(sql % (list)))
		connection.commit()
		return used
	except pymysql.err.Error as e:
		print('Query Failed to execute "{}" :\n{}'.format(sql % (list),e))
		return None
	finally :
		connection.close()
