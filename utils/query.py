#import pymysql.cursors
import aiomysql
from time import time
import datetime
from discord import NotFound

async def fetchall(bot, sql, plist = None) :
	connection = await bot.connect_db()
	fsql = (sql % plist) if plist != None else sql
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, plist)
			s = time()
			used = s - f
			print('[MySQL Query] Query Executed "{}"'.format(fsql))
			r = await cursor.fetchall()
			await bot.use_query(fsql, r, used, cursor.rowcount)
			return {
				"result" : r,
				"time" : used,
				"rows" : cursor.rowcount
			}
	except aiomysql.Error as e:
		print('[MySQL Query] Query Failed to execute "{}" :\n{}'.format(fsql,e))
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')

async def fetchone(bot, sql, plist = None) :
	connection = await bot.connect_db()
	fsql = (sql % plist) if plist != None else sql
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, plist)
			s = time()
			used = s - f
			print('[MySQL Query] Query Executed "{}"'.format(fsql))
			r = await cursor.fetchone()
			await bot.use_query(fsql, r, used, cursor.rowcount)
			return {
				"result" : r,
				"time" : used,
				"rows" : cursor.rowcount
			}
	except aiomysql.Error as e:
		print('[MySQL Query] Query Failed to execute "{}" :\n{}'.format(fsql,e))
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')

async def commit(bot, sql, plist = None) :
	connection = await bot.connect_db()
	fsql = (sql % plist) if plist != None else sql
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, plist)
			s = time()
			used = s - f
		print('[MySQL Query] Query Executed "{}"'.format(fsql))
		await bot.use_query(fsql, {}, used, cursor.rowcount)
		await connection.commit()
		return used
	except aiomysql.Error as e:
		print('[MySQL Query] Query Failed to execute "{}" :\n{}'.format(fsql,e))
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')








async def qcheck_guild(bot, guild) :
	a = await fetchone(bot, "SELECT EXISTS(SELECT 1 FROM discord_guild WHERE snowflake=%s LIMIT 1)", guild.id)
	return a

async def qinsert_guild(bot, guild) :
	if not (await qcheck_guild(bot, guild)) :
		return await commit(bot, "INSERT INTO `discord_guild` (`snowflake`, `name`, `added_at`, `updated_at`, `owner_snowflake`, `supported`) VALUES (%s, %s, %s, %s, %s, 0)", (guild.id, guild.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), guild.owner_id))
	else :
		return False

async def qget_guild(bot, guild, ll) :
	if (await qcheck_guild(bot, guild)) :
		return await fetchone(bot, "SELECT %s FROM discord_user WHERE snowflake = %s", ll)
	else :
		return False

async def qcheck_profile(bot, user) :
	a = await fetchone(bot, "SELECT EXISTS(SELECT 1 FROM discord_user WHERE snowflake=%s LIMIT 1)", user.id)
	return a

async def qinsert_profile(bot, user) :
	if not (await qcheck_profile(bot, user)) :
		return await commit(bot, "INSERT INTO `discord_user` (`snowflake`, `username`, `added_at`, `credits`, `owner`, `commands`) VALUES (%s, %s, 0, 0, 0)", (user.id, user.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	else :
		return False

async def qget_profile(bot, user, ll) :
	if (await qcheck_profile(bot, user)) :
		return await fetchone(bot, "SELECT {} FROM discord_user WHERE snowflake = %s".format(",".join(ll)), user.id)
	else :
		return False

async def qupdate_profile(bot, user, dct) :
	if (await qcheck_profile(bot, user)) :
		str = ",".join(["{}=\"{}\"".format(key, value) for key, value in dct.items()])
		return await commit(bot, "UPDATE `discord_user` SET {} WHERE snowflake = %s".format(str), (user.id))

async def qupdate_profile_record(bot, user) :
	if (await qcheck_profile(bot, user)) :
		return await qupdate_profile(bot, user, {'username':user.name})

async def qupdate_all_profile_record(bot) :
	al = await qget_id_list(bot)
	strall = ""
	for s in al['result'] :
		try :
			us = await bot.fetch_user(s['snowflake'])
		except NotFound :
			strall += "UPDATE `discord_user` SET `username`=\"{}\", `updated_at`=NOW() WHERE snowflake = {};".format('@@@("NOT FOUND")', s['snowflake'])
		else :
			strall += "UPDATE `discord_user` SET `username`=\"{}\", `updated_at`=NOW() WHERE snowflake = {};".format(us.name, s['snowflake'])
	return await commit(bot, strall)

async def qget_id_list(bot, addid = False) :
	return await fetchall(bot, "SELECT {}snowflake FROM discord_user".format("id," if addid else ''))
