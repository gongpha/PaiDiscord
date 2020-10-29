import pymysql
import aiomysql
from time import time
import datetime
from discord import NotFound, Forbidden

#import sqlalchemy
import aiomysql

class NotAllowConnect(Exception) :
	pass
class CannotConnect(Exception) :
	pass

class BotDB :
	def __init__(self, bot, allow, host, username, password, database) :
		self.bot = bot
		self.host = host
		self.username = username
		self.password = password
		self.database = database
		self.pool = None
		self.allow = allow

	async def init(self) :
		if self.allow :
			try :
				self.pool = await aiomysql.create_pool(host=self.host,
				user=self.username,
				password=self.password,
				db=self.database,
				charset='utf8mb4',
				cursorclass=aiomysql.cursors.DictCursor,
				loop=self.bot.loop)
			except pymysql.err.OperationalError :
				raise CannotConnect()
		else :
			raise NotAllowConnect()

	async def close(self) :
		self.pool.close()
		await self.pool.wait_closed()

	async def get_cursor(self) :
		if self.pool :
			return await (await self.pool.acquire()).cursor()
		else :
			raise CannotConnect()

	async def fetchone(self, sql, arglist = None) :
		if self.allow :
			cursor = await self.get_cursor();
			await cursor.execute(sql, arglist)
			return await cursor.fetchone()
		else :
			raise NotAllowConnect();

	async def fetchall(self, sql, arglist = None) :
		if self.allow :
			cursor = await self.get_cursor();
			await cursor.execute(sql, arglist)
			return await cursor.fetchall()
		else :
			raise NotAllowConnect();

	async def commit(self, sql, arglist = None) :
		if self.allow :
			cursor = await self.get_cursor();
			await cursor.execute(sql, arglist)
			await cursor.connection.commit()
		else :
			raise NotAllowConnect();

	async def commit_list(self, sql, arglist = None) :
		if self.allow :
			cursor = await self.get_cursor();
			await cursor.executemany(sql, arglist)
			await cursor.connection.commit()
		else :
			raise NotAllowConnect();




	async def check_guild(self, guild) :
		return await (self.fetchone("SELECT EXISTS(SELECT 1 FROM discord_guild WHERE snowflake={} LIMIT 1) AS ex".format(guild.id)))["ex"]

	async def insert_guild(self, guild) :
		if not (await self.check_guild(guild)) :
			await self.commit("INSERT INTO `discord_guild` (`snowflake`, `name`, `added_at`, `updated_at`, `owner_snowflake`, `supported`) VALUES (%s, %s, %s, %s, %s, 0)", (guild.id, guild.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), guild.owner_id))
			return True
		else :
			return False

	async def insert_guild_list_nocheck(self, guildlist) :
		itemlist = []
		for guild in guildlist :
			itemlist.append((guild.id, guild.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), guild.owner_id))
		await self.commit_list("INSERT INTO `discord_guild` (`snowflake`, `name`, `added_at`, `updated_at`, `owner_snowflake`, `supported`) VALUES (%s, %s, %s, %s, %s, 0)", itemlist)
		return True

	async def get_guild(self, guild, ll) :
		if (await self.check_guild(guild)) :
			return await self.fetchone("SELECT {} FROM discord_user WHERE snowflake = %s".format(','.join(ll)))
		else :
			return False

	async def check_profile(self, user) :
		return (await self.fetchone("SELECT EXISTS(SELECT 1 FROM discord_user WHERE snowflake={} LIMIT 1) AS ex".format(user.id)))["ex"]

	async def insert_profile(self, user) :
		if not (await self.check_profile(user)) :
			await self.commit("INSERT INTO `discord_user` (`snowflake`, `username`, `added_at`, `credits`, `owner`, `commands`) VALUES (%s, %s, %s, 0, 0, 0)", (user.id, user.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			return True
		else :
			return False

	async def get_profile(self, user, ll) :
		if (await self.check_profile(user)) :
			return await self.fetchone("SELECT {} FROM discord_user WHERE snowflake = %s".format(",".join(ll)), user.id)
		else :
			return False

	async def update_profile(self, user, dct) :
		if (await self.check_profile(user)) :
			k = []
			l = []
			for key, value in dct.items() :
				k.append(key)
				l.append(value)
			l.append(guild.id)
			str = ",".join(["{}=%s".format(key) for key in k])
			return await self.commit("UPDATE `discord_guild` SET {} WHERE snowflake = %s".format(str), l)

	async def update_guild(self, guild, dct) :
		if (await self.check_guild(guild)) :
			k = []
			l = []
			for key, value in dct.items() :
				k.append(key)
				l.append(value)
			l.append(guild.id)
			str = ",".join(["{}=%s".format(key) for key in k])
			return await self.commit("UPDATE `discord_guild` SET {} WHERE snowflake = %s".format(str), l)

	async def update_and_increase_cmd_count(self, user) :
		await self.insert_profile(user)
		return await self.commit("UPDATE `discord_user` SET `username`=%s, `commands`=commands + 1 WHERE snowflake = %s", (user.name, user.id))
	async def increase_cmd_count(self, user) :
		await self.insert_profile(user)
		return await self.commit("UPDATE `discord_user` SET `commands`=commands + 1 WHERE snowflake = %s", (user.id))

	async def update_profile_record(self, user) :
		if (await self.check_profile(user)) :
			return await self.update_profile(user, {'username':user.name, 'updated_at':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

	async def update_all_profile_record(self) :
		al = await self.get_user_id_list()
		sql = "UPDATE `discord_user` SET `missing`=%s, `username`=%s, `updated_at`=NOW() WHERE snowflake=%s;"
		ulist = []
		for s in al['result'] :
			try :
				us = await self.bot.fetch_user(s['snowflake'])
			except NotFound :
				ulist.append((1, 'discord_user.username', s['snowflake']))
			else :
				ulist.append((0, us.name, s['snowflake']))
		await self.commit_list(sql, ulist)
		return True









	async def update_guild_record(self, guild) :
		if (await self.check_guild(guild)) :
			return await self.update_guild(guild, {'name':guild.name, 'owner_snowflake':guild.owner_id})

	async def update_all_guild_record(self) :
		al = await self.get_guild_id_list()

		sql = "UPDATE `discord_guild` SET `missing`=%s, `name`=%s, `owner_snowflake`=%s, `updated_at`=NOW() WHERE snowflake=%s;"
		ulist = []
		for s in al :
			try :
				us = await self.bot.fetch_user(s['snowflake'])
			except NotFound :
				ulist.append((1, 'discord_guild.name', 'discord_guild.owner_snowflake', s['snowflake']))
			else :
				ulist.append((0, us.name, us.owner_id, s['snowflake']))
		await self.commit_list(sql, ulist)
		ulist = []
		for gu in self.bot.guilds :
			if gu.id not in [i["snowflake"] for i in al] :
				ulist.append(gu)
		if ulist :
			await self.insert_guild_list_nocheck(ulist)

		return True

	async def get_user_id_list(self, addid = False) :
		return await self.fetchall("SELECT {}snowflake FROM discord_user WHERE missing=0".format("id," if addid else ''))
	async def get_guild_id_list(self, addid = False) :
		return await self.fetchall("SELECT {}snowflake FROM discord_guild WHERE missing=0".format("id," if addid else ''))







	async def look_for_alias(self, user_id, guild_id) :
		return await self.fetchone("SELECT snowflake FROM discord_user_alias WHERE alias=%s AND guild_snowflake=%s")
