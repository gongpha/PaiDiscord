#import pymysql.cursors
from time import time
import datetime
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
			await bot.use_query(sql % (list), used)
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
		await bot.use_query(sql % (list), used)
		await connection.commit()
		return used
	except pymysql.err.Error as e:
		print('[MySQL Query] Query Failed to execute "{}" :\n{}'.format(sql % (list),e))
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')








async def qcheck_guild(bot, guild) :
	a = await fetchone(bot, "SELECT EXISTS(SELECT 1 FROM pai_discord_guild WHERE snowflake=%s LIMIT 1)", guild.id)
	return a

async def qinsert_guild(bot, guild) :
	if not (await qcheck_guild(bot, guild)) :
		return await commit(bot, "INSERT INTO `pai_discord_guild` (`snowflake`, `prefix`, `c_member_join`, `c_join_message`, `c_member_leave`, `c_leave_message`, `support`, `c_levelup_notice`, `first_seen`) VALUES (%s, '', '1', '', '1', '', '0', '1', %s)", (guild.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	else :
		return False

async def qget_guild(bot, guild, ll) :
	if (await qcheck_guild(bot, guild)) :
		return await fetchone(bot, "SELECT %s FROM pai_discord_profile WHERE snowflake = %s", ", ".join(ll))
	else :
		return False

async def qcheck_profile(bot, user) :
	a = await fetchone(bot, "SELECT EXISTS(SELECT 1 FROM pai_discord_profile WHERE snowflake=%s LIMIT 1)", user.id)
	return a

async def qinsert_profile(bot, user) :
	if not (await qcheck_profile(bot, user)) :
		print('a')
		return await commit(bot, "INSERT INTO `pai_discord_profile` (`snowflake`, `profile_name`, `profile_description`, `first_seen`, `credits`, `owner`, `badges`, `level`, `exp`, `commands`, `info`) VALUES (%s, '', '', %s, 0, 0, '{}', 1, 0, 0, '{}')", (user.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	else :
		return False

async def qget_profile(bot, user, ll) :
	if (await qcheck_profile(bot, user)) :
		return await fetchone(bot, "SELECT %s FROM pai_discord_profile WHERE snowflake = %s", ", ".join(ll))
	else :
		return False
