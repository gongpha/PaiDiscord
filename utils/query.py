#import pymysql.cursors
from time import time

async def fetchone(bot, sql, list = None) :
	connection = await bot.connect_db()
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, list)
			s = time()
			used = s - f
			print('[MySQL Query] Query Executed "{}"'.format(sql % (list)))
			return {
				"result" : await cursor.fetchone(),
				"time" : used,
				"rows" : cursor.rowcount
			}
	except pymysql.err.Error as e:
		print('[MySQL Query] Query Failed to execute "{}" :\n{}'.format(sql % (list),e))
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')

async def commit(bot, sql, list = None) :
	connection = await bot.connect_db()
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, list)
			s = time()
		used = s - f
		print('[MySQL Query] Query Executed "{}"'.format(sql % (list)))
		await connection.commit()
		return used
	except pymysql.err.Error as e:
		print('[MySQL Query] Query Failed to execute "{}" :\n{}'.format(sql % (list),e))
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')
