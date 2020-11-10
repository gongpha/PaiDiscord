import asyncio, discord
import platform
import yaml
import sys
import traceback
import random
import os
import json
from io import BytesIO
from discord.ext import commands
from utils.template import embed_em, embed_wm
from utils.dict import safeget
#import pymysql.cursors
import aiomysql.cursors
import aiohttp
import datetime
import utils.botdb as botdb
import re

class NoToken(Exception) :
	"""No Token was found or invalid token"""
	pass

class AuthNotFound(Exception) :
	"""Finding Auth with keys was failed"""
	pass

class BotChannelNotFound(Exception) :
	"""Defined channels wasn't found"""
	pass

class BotIsNotReady(Exception) :
	"""API Function was called while the bot isn't ready"""
	pass

class ConfigsNotFound(Exception) :
	"""Config and Base Config files are not found"""
	pass

def eget(dict, key, default) :
	v = dict.get(key, '')
	try :
		return os.environ.get(v[1:], default) if v.startswith('?') else v
	except AttributeError :
		return v

class Pramual(commands.Bot) :
	pbot = None
	def __init__(self, *args, **kwargs) :
		self.info_fname = kwargs.pop('info', {})
		self.channels_fname = kwargs.pop('channels', {})
		self.auths_fname = kwargs.pop('auths', {})
		self.configs_fname = kwargs.pop('configs', {})
		self.resources_fname = kwargs.pop('resources', {
			"StatusIcons" : {
				"online" : '📗',
				"idle" : '📒',
				"dnd" : '📕',
				"offline" : '📓',
				"invisible" : '📓'
			}
		})
		self.loaded_dev = kwargs.pop('dev', False)
		self.load_configs(self.info_fname, self.channels_fname, self.auths_fname, self.configs_fname, self.resources_fname, self.loaded_dev, kwargs.pop('loop', asyncio.get_event_loop()), kwargs.pop('build_number', 0), kwargs.pop('build_date', None))
		self.load_strings()
		self.load_assets()
		if self.token == None :
			raise NoToken("Invalid Token")

		intents = discord.Intents.default()
		intents.members = True


		super().__init__(command_prefix=self.cmd_prefix, intents=intents, *args, **kwargs)
		self.remove_command('help')
		pbot = self

	def load_assets(self) :
		with open("assets/webhook.png", "rb") as image :
			self.webhook_avatar = image.read()

	def load_strings(self) :
		self.stringstack = {}
		for language in self.languages :
			try :
				with open('i18n/{}.yml'.format(language), encoding="utf8") as json_file :
					self.stringstack[language] = yaml.safe_load(json_file)
			except FileNotFoundError :
				print('>> "{}" language not found'.format(language))
				self.stringstack[language] = {}

	# def interface_channel_check(self, channel) :
	# 	if not channel.topic :
	# 		return None
	# 	match = re.match('@@@(.+)__([a-z]*):(.+)*', channel.topic)
	# 	if (match.group(1)).lower() == self.bot_name.lower() :
	# 		return (match.group(2), match.group(3).split(','))
	# 	else :
	# 		return None
	#
	# def scan_interface_channel(self) :
	# 	for channel in self.get_all_channels()
	# 		r = interface_channel_check(channel)
	# 		if r :


	def load_configs(self, info, channels, auths, configs, resources, dev, loop, build_number, build_date) :
		inf = info
		self.bot_channels = channels
		self.auth = auths
		self.configs = configs
		self.resources = resources
		self.build_number = build_number
		self.build_date = build_date
		self.dev_configs = {}
		self.dev = dev
		if self.dev == None :
			self.dev = eget(self.configs, 'Dev', False)

		if self.dev :
			if 'IfDev' in self.configs :
				self.dev_configs = self.configs['IfDev']

		def infget(key, default) :
			return eget(inf, key, default)

		self.bot_name = infget('name', 'Pai')
		self.bot_description = infget('description', '')
		self.bot_description_long = infget('description_long', '')
		self.token = infget('token', None)
		self.cached_prefix = {}
		self.cached_language = {}
		self.hd_avatar_url = infget('hd_avatar_url', None)
		self.cmdprefix = infget('default_command_prefix', '_')
		def prefix(bot, message) :
			r = []
			r = commands.when_mentioned(bot, message) + r
			r.append(self.cached_prefix.get((message.guild or message.author).id, self.cmdprefix))
			return r
		self.cmd_prefix = prefix

		self.default_timezone = infget('default_timezone', 'Asia/Bangkok')
		self.languages = infget('languages', ['en', 'th'])
		self.theme = infget('theme', (0xFF7F00, 0x007FFF))
		self.owners = infget('owners', [])
		self.db = infget('db', None)
		self.db_host = infget('db_hostname', None)
		self.db_username = infget('db_username', None)
		self.db_password = infget('db_password', None)
		self.db_database = infget('db_database', None)

		#self.cache_interface = {}

		g = infget('game_static', None)
		gd = infget('game_default', None)
		if not g :
			g = gd
		self.game = [g] if not isinstance(g, (list, tuple)) else g
		self.cog_list = infget('cogs', ['cogs.Info', 'cogs.Experimental'])
		self.interface = infget('interface', False)
		self.guild_invite_code = infget('my_guild_invite_code', 'KK6R9BJ')

		self.loop = loop
		self.waitForMessage = {}
		self.start_time = datetime.datetime.now()
		self.session = aiohttp.ClientSession(loop=self.loop)

	def getAuth(self, *keylist) :
		dct = self.auth.copy()
		for key in keylist :
			try:
				dct = dct[key]
			except KeyError :
				raise AuthNotFound
				return None

	# def add_channel_by_dict(self, dictch) :
	# 	for n, id in dictch.items() :
	# 		self.add_my_channel(n, id)
	#
	# def add_my_channel(self, name, id) :
	# 	print(f">> Added Channel {name} : {id}")
	# 	self.channels_id[name] = id
	#
	def get_mutual_guilds(self, user) :
		mt = []
		for g in self.guilds :
			if g.get_member(user.id) :
				mt.append(g)
		return mt
	def get_bot_channel(self, *keylist) :
		c = safeget(self.bot_channels, *keylist)
		if c == None :
			raise BotChannelNotFound
		else :
			if self.is_ready() :
				return self.get_channel(int(c))
			else :
				raise BotIsNotReady

	#async def use_query(self, sql, result, time, rowcount) :
	#	e = discord.Embed(title=f"Query Report")
	#	e.description = "```\n" + sql[:2041] + "```"
	#	j = json.dumps(result, indent=4)
	#	e.add_field(name="Result ({})".format(rowcount), value='```\n' + j[:1017] + '```')
	#	e.color = 0xFFFF00
	#	e.set_footer(text=time)
	#	await self.get_bot_channel("system", "query_report").send(embed=e)

	def ss(self, *keylist) :
		#lang = self.cached_language.get(id, None)
		lang = None
		dct = self.stringstack[lang or self.languages[0]].copy()
		for key in keylist :
			try:
				dct = dct[key]
			except KeyError :
				return "@@@[string_not_found/ไม่-พบ-ข้อความ]"
		return dct

	def get_dev_configs(self, key, default=None) :
		if self.dev :
			return None
		return self.dev_configs.get(key, default)

	def get_resource(self, default, *keylist) :
		lang = None
		dct = self.resources.copy()
		for key in keylist :
			try:
				dct = dct[key]
			except KeyError :
				return default
		return dct

	# async def fetch_language(self, id) :
	# 	if id in self.cached_language :
	# 		return self.cached_language[id]
	# 	else :
	# 		lang = await fetchone(self, "SELECT lang FROM pai_discord_profile WHERE snowflake = %s", id)
	# 		if lang :


	async def on_ready(self) :
		print(f'>> Login As "{self.user.name}" ({self.user.id})')
		print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
		if self.dev :
			print('>> Developer Mode Enabled')
		for c in self.cog_list :
			try :
				self.load_extension(c)
			except commands.errors.ExtensionFailed as error :
				print("""Load Extension "{}" Failed.""".format(c))
				error = getattr(error, 'original', error)

				traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		if self.game :
			game = discord.Game(name=self.game[0].format(self), type=discord.ActivityType.listening)
		await self.change_presence(status=discord.Status.online, activity=game)
		self.static_invite = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=470019184&scope=bot'.format(self.user.id)
		try :
			self.guild_invite = await self.fetch_invite(url=self.guild_invite_code)
		except discord.NotFound :
			print('>> WARNING : GUILD INVITE NOT FOUND')
			self.guild_invite = None

		self.db = botdb.BotDB(self, self.db, self.db_host, self.db_username, self.db_password, self.db_database)
		try :
			await self.db.init()
			print("(!) Connected to Database")
		except botdb.CannotConnect :
			print("<X> Cannot connect database")
		except botdb.NotAllowConnect :
			print("(!) No Connecting for database")

	def run_bot(self) :
		try :
			super().run(self.token)
		except discord.errors.HTTPException as e :
			print("(X) HTTP ERROR")
			print("    ({}) {}".format(e.status, e.text))

	async def kill_bot(self) :
		for vc in self.voice_clients :
			await vc.disconnect()
		await self.session.close()
		await self.close()
		self.bot.loop.stop()
		if self.db :
			self.db.close()

	# @after_invoke
	# async def after_command(self, ctx):
	# 	await ctx.send("Hello from after_invoke")

	async def on_command_completion(self, ctx) :
		#if self.get_dev_configs("update_command_used_count", False) :
		try :
			await ctx.bot.db.update_and_increase_cmd_count(ctx.author)
		except botdb.CannotConnect :
			pass

	async def on_command(self, ctx) :
		# if ctx.author.id not in self.cached_language :
		# 	await self.fetch_language(ctx.author.id)
		e = discord.Embed(title=f"Command : `{self.cmdprefix}{ctx.command.name}`")
		e.description = f"Called to `{self.bot_name}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel) if ctx.message.guild else 'DM with `{0.recipient}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n" + ctx.message.jump_url + "\n```" + ctx.message.clean_content + "```", inline=False)
		if isinstance(self.theme, (list, tuple)) :
			e.color = self.theme[1] if len(self.theme) > 1 else self.theme[0]
		else :
			e.color = self.theme
		e.timestamp = ctx.message.created_at
		await self.get_bot_channel("system", "log").send(embed=e)

	async def on_command_error(self, ctx, error) :
		cmdn = ctx.message.content.split(' ')[0]
		if isinstance(error, commands.CommandNotFound) :
			return
		elif isinstance(error, commands.MissingRequiredArgument) :
			await ctx.send(embed=embed_em(ctx, self.ss('InCorrectArgument'), "```{} {}```".format(cmdn, ctx.command.usage) if ctx.command.usage != None else ''))
			return
		elif isinstance(error, commands.NoPrivateMessage) :
			await ctx.send(embed=embed_wm(ctx, ctx.bot.ss("CommandInDMNotAvailable")))
			return
		elif isinstance(error, commands.MissingPermissions) :
			l = ('\n'.join(ctx.bot.ss("NoPermissionWith").format(ctx.bot.ss("Permission", string)) for string in error.missing_perms)) if error.missing_perms else ctx.bot.ss("None")
			await ctx.send(embed=embed_em(ctx, l))
			return
		elif isinstance(error, commands.NotOwner) :
			await ctx.send(embed=embed_em(ctx, ctx.bot.ss("YouAreNotBotOwner")))
			return
		elif isinstance(error, commands.CheckFailure) :
			await ctx.send(embed=embed_em(ctx, error)) # ctx.bot.ss("AnErrorOccurred")
			return

		e = discord.Embed(title="Command Error : `{}{}`".format(self.cmdprefix if ctx.command.name != None else "",ctx.command.name if ctx.command.name != None else "UNKNOWN"))
		e.description = f"Called to `{self.bot_name}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel) if ctx.message.guild else 'DM with `{0.recipient}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n" + ctx.message.jump_url + "\n```" + ctx.message.content + "```", inline=False)
		e.color = 0xff0000
		e.timestamp = ctx.message.created_at

		error = getattr(error, 'original', error)

		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

		tb = error.__traceback__
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename

		e.add_field(name='Expection', value="("+str(ctx.message.id) + ")\n```" + str(getattr(error, 'original', error)) + "```", inline=False)
		e.add_field(name='Filename', value=filename, inline=True)
		e.add_field(name='Line No.', value=lineno, inline=True)
		await self.get_bot_channel("system", "error").send(embed=e)

	async def on_member_join(self, member) :
		if self.get_dev_configs("member_join_message", True) :
			e = discord.Embed(title=self.ss("WelcomeUserToGuild").format(member=member, guild=member.guild))
			ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
			e.description = "*{}*".format(self.ss("UserWasJoinedGuildNo").format(mention=member.mention, count=len(member.guild.members), ordinal=ordinal(len(member.guild.members))))
			e.color = 0x00AA80
			e.set_thumbnail(url=member.avatar_url)
			e.set_footer(text=member.id)
			await member.guild.system_channel.send(embed=e)

	async def on_member_remove(self, member) :
		if self.get_dev_configs("member_leave_message", True) :
			if self.user.id == member.id :
				return
			e = discord.Embed(title=self.ss("UserWasLeftTheGuild").format(member=member, guild=member.guild))
			e.description = "*{}*".format(self.ss("NowGuildHadNoMembersLeft").format(count=len(member.guild.members)))
			e.color = 0xCE3232
			e.set_thumbnail(url=member.avatar_url)
			e.set_footer(text=member.id)
			await member.guild.system_channel.send(embed=e)

	async def on_guild_join(self, guild) :
		t = await qinsert_guild(self, guild)
		if t != None :
			e = discord.Embed(title="New Guild : {}".format(guild.name))
			#e.description = "*{}*".format(self.stringstack["UserWasJoinedGuildNo"].format(member.mention,len(member.guild.members)))
			e.color = 0x00AA80
			e.set_thumbnail(url=str(guild.icon_url))
			e.set_footer(text="{} : {}".format(guild.id, t))
			await self.get_bot_channel("system", "guild_update").send(embed=e)

	async def on_guild_remove(self, guild) :
		t = await commit(self, "DELETE FROM `pai_discord_guild` WHERE `snowflake` = %s", guild.id)
		if t != None :
			e = discord.Embed(title="Removed Guild : {}".format(guild.name))
			#e.description = "*{}*".format(self.stringstack["UserWasJoinedGuildNo"].format(member.mention,len(member.guild.members)))
			e.color = 0xCE3232
			e.set_thumbnail(url=str(guild.icon_url))
			e.set_footer(text="{} : {}".format(guild.id, t))
			await self.get_bot_channel("system", "guild_update").send(embed=e)

	async def on_message(self, message) :
		#print(self.waitForMessage)
		if self.interface :
			if message.author.id in self.owners :
				cc = message.channel
				if isinstance(cc, discord.TextChannel) :
					r = cc.topic
					if r != None :
						match = re.match('@@@(.+)__([a-z]*):(.+)*', r)
						if match :
							if (match.group(1)).lower() != self.bot_name.lower() :
								return
							if match.group(2) != 'channel' :
								return
							p = match.group(3).split(',')
							if not p[0].isdigit() :
								await message.add_reaction('\N{NEGATIVE SQUARED CROSS MARK}')
								await message.add_reaction('\N{INPUT SYMBOL FOR NUMBERS}')
								return
							else :
								c = self.get_channel(int(p[0]))
								if c == None :
									await message.add_reaction('\N{NEGATIVE SQUARED CROSS MARK}')
									return
								else :
									await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
									f = []
									for a in message.attachments :
										f.append(discord.File(fp=BytesIO(await a.read()), filename=a.filename, spoiler=a.is_spoiler()))
									await c.send(content=message.content, tts=message.tts, embed=message.embeds[0] if message.embeds else None, files=f)
									return
		await self.process_commands(message)

	#async def on_message_delete(self, message) :
		#print(self.waitForMessage)
		# if self.interface :
		# 	if message.author.id in self.owners :
		# 		r = message.channel.topic.split(':')
		# 		if r[0].startswith('@@@pai__channel') :
		# 			if not r[1].isdigit() :
		# 				await message.add_reaction('\N{NEGATIVE SQUARED CROSS MARK}')
		# 				await message.add_reaction('\N{INPUT SYMBOL FOR NUMBERS}')
		# 			else :
		# 				c = self.get_channel(int(r[1]))
		# 				if c == None :
		# 					await message.add_reaction('\N{NEGATIVE SQUARED CROSS MARK}')
		# 				else :
		# 					await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
		# 					await c.send(message.content)

		# if message.channel.id in self.waitForMessage :
		# 	if message.author.id in self.waitForMessage[message.channel.id] :
		# 		if self.waitForMessage[message.channel.id][message.author.id] == 1 :
		# 			await message.channel.send(":thinking:")
		# 			del self.waitForMessage[message.channel.id][message.author.id]
		# 			await self.process_commands(message)
		# 			return
		# if message.activity :
		# 	if message.activity["type"] == 3 :
		# 		await message.channel.send(self.stringstack["Response"]["UserSentActivitiesSpotify"])
		# #if message.mention_everyone :
		# #	await message.channel.send(stringstack["th"]["_response_everyone"])
		# else :
		# 	for user in message.mentions :
		# 		if user.id == self.user.id :
		# 			if message.author.id != self.user.id :
		# 				if not message.content.startswith(self.cmdprefix) :
		# 					await message.channel.send(self.stringstack["Response"]["UserSentBot"].format(message.author.mention))
		#
		# 					if not message.channel.id in self.waitForMessage :
		# 						self.waitForMessage[message.channel.id] = {}
		# 					self.waitForMessage[message.channel.id][message.author.id] = 1
		# 			else :
		# 				await message.channel.send(self.stringstack["Response"]["BotSentItself"])
		#await self.process_commands(message)
def load_yml(filename, deffilename) :
	try :
		with open(filename, 'r', encoding="utf8") as f:
			return yaml.safe_load(f)
	except FileNotFoundError :
		try :
			with open(deffilename, 'r', encoding="utf8") as f:
				return yaml.safe_load(f)
		except FileNotFoundError :
			raise ConfigsNotFound('Config and Base Config files are not found')
