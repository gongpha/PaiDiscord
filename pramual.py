import asyncio, discord
import platform
import yaml
import sys
import traceback
import random
from discord.ext import commands
from utils.template import embed_em
#import pymysql.cursors
import aiomysql.cursors
import aiohttp
import datetime
from utils.query import *

class NoToken(Exception):
	"""No Token was found or invalid token"""
	pass

class Pramual(commands.Bot) :
	pbot = None
	def __init__(self, *args, **kwargs) :
		command_prefix = kwargs.pop('command_prefix', commands.when_mentioned_or('::'))
		self.bot_name = kwargs.pop('name', "null")
		self.bot_description = kwargs.pop('description', "null")
		self.loop = kwargs.pop('loop', asyncio.get_event_loop())
		self.std = kwargs.pop('std', None)
		self.token = kwargs.pop('token', None)
		#self.log_channel_id = kwargs.pop('log_ch', None)
		#self.error_channel_id = kwargs.pop('err_ch', None)
		#self.query_channel_id = kwargs.pop('qur_ch', None)
		self.timezone = kwargs.pop('timezone', None)
		self.theme = kwargs.pop('theme', [0x9B59B6])
		self.lang = kwargs.pop('lang', None)
		self.cog_list = kwargs.pop('cog_list', None)
		self.owner_list = kwargs.pop('owner', None)
		self.waitForMessage = {}
		self.channels_id = {}
		# self.connection = None
		self.where = kwargs.pop('where', None)
		self.session = aiohttp.ClientSession(loop=self.loop)
		self.database_host = kwargs.pop('databaseHost', None)
		self.database_username = kwargs.pop('databaseUsername', None)
		self.database_password = kwargs.pop('databasePassword', None)
		self.database_database = kwargs.pop('databaseDatabase', None)
		self.mysql = kwargs.pop('mysql', False)
		g = kwargs.pop('game_static', None)
		gd = kwargs.pop('game_default', None)
		if not g :
			g = gd
		self.game = [g] if not isinstance(g, (list, tuple)) else g
		self.auth = kwargs.pop('auth', None)
		self.start_time = datetime.datetime.now()
		with open('i18n/{}.yml'.format(self.lang), encoding="utf8") as json_file :
			self.stringstack = yaml.safe_load(json_file)
		if self.token == None :
			raise NoToken("Invalid Token")
		super().__init__(command_prefix=command_prefix, *args, **kwargs)
		self.remove_command('help')
		pbot = self

	async def connect_db(self) :
		# all([self.database_host, self.database_username, self.database_password, self.database_database])
		if self.mysql :
			return await aiomysql.connect(host=self.database_host,
				user=self.database_username,
				password=self.database_password,
				db=self.database_database,
				charset='utf8mb4',
				cursorclass=aiomysql.cursors.DictCursor,
				loop=self.loop)
		else :
			return None

	def add_channel_by_dict(self, dictch) :
		for n, id in dictch.items() :
			self.add_my_channel(n, id)

	def add_my_channel(self, name, id) :
		print(f">> Added Channel {name} : {id}")
		self.channels_id[name] = id

	def get_my_channel(self, name) :
		return self._channels.get(name, None)

	async def use_query(self, sql, time) :
		e = discord.Embed(title=f"Query Report")
		e.description = "```\n" + sql + "```"
		e.color = 0xFFFF00
		e.set_footer(text=time)
		await self.get_my_channel("query").send(embed=e)

	def ss(self, *keylist) :
		dct = self.stringstack.copy()
		for key in keylist:
			try:
				dct = dct[key]
			except KeyError:
				return "@@@[string_not_found/ไม่-พบ-ข้อความ]"
		return dct

	async def on_ready(self) :
		print(f'>> Login As "{self.user.name}" ({self.user.id})')
		print(f'>> Mode   : "{self.std}"')
		print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

		# self.log_channel = super().get_channel(self.log_channel_id)
		# self.error_channel = super().get_channel(self.error_channel_id)
		# self.query_channel = super().get_channel(self.query_channel_id)

		self._channels = {}
		for n, id in self.channels_id.items() :
			c = super().get_channel(id)
			self._channels[n] = c

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

	def run_bot(self) :
		super().run(self.token)

	# @after_invoke
	# async def after_command(self, ctx):
	# 	await ctx.send("Hello from after_invoke")

	async def on_command_completion(self, ctx) :
		await commit(self, "UPDATE `pai_discord_profile` SET commands=commands + 1, user_name=%s WHERE snowflake=%s", (ctx.author.name, ctx.author.id))

	async def on_command(self, ctx) :
		e = discord.Embed(title=f"Command : `{self.command_prefix}{ctx.command.name}`")
		e.description = f"Called to `{self.std}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel) if ctx.message.guild else 'DM with `{0.recipient}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n```" + ctx.message.clean_content + "```", inline=False)
		e.color = int(random.choice(self.theme))
		e.timestamp = ctx.message.created_at
		await self.get_my_channel("log").send(embed=e)

	async def on_command_error(self, ctx, error) :
		e = discord.Embed(title="Command Error : `{}{}`".format(self.command_prefix if ctx.command.name != None else "",ctx.command.name if ctx.command.name != None else "UNKNOWN"))
		e.description = f"Called to `{self.std}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel) if ctx.message.guild else 'DM with `{0.recipient}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n```" + ctx.message.clean_content + "```", inline=False)
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
		await self.get_my_channel("error").send(embed=e)

	async def on_member_join(self, member) :
		e = discord.Embed(title=self.stringstack["WelcomeUserToGuild"].format(member, member.guild))
		e.description = "*{}*".format(self.stringstack["UserWasJoinedGuildNo"].format(member.mention,len(member.guild.members)))
		e.color = 0x00AA80
		e.set_thumbnail(url=member.avatar_url)
		e.set_footer(text=member.id)
		await member.guild.system_channel.send(embed=e)

	async def on_member_remove(self, member) :
		if self.id == member.id :
			return
		e = discord.Embed(title=self.stringstack["UserWasLeftTheGuild"].format(member, member.guild))
		e.description = "*{}*".format(self.stringstack["NowGuildHadNoMembersLeft"].format(len(member.guild.members)))
		e.color = 0xCE3232
		e.set_thumbnail(url=member.avatar_url)
		e.set_footer(text=member.id)
		await member.guild.system_channel.send(embed=e)

	async def on_guild_join(self, guild) :
		t = qinsert_guild(self, guild)
		if t != None :
			e = discord.Embed(title="New Guild : {}".format(guild.name))
			#e.description = "*{}*".format(self.stringstack["UserWasJoinedGuildNo"].format(member.mention,len(member.guild.members)))
			e.color = 0x00AA80
			e.set_thumbnail(url=str(guild.icon_url))
			e.set_footer(text="{} : {}".format(guild.id, t))
			await self.get_my_channel("guild").send(embed=e)

	async def on_guild_remove(self, guild) :
		t = commit(self, "DELETE FROM `pai_discord_guild` WHERE `snowflake` = %s", guild.id)
		if t != None :
			e = discord.Embed(title="Removed Guild : {}".format(guild.name))
			#e.description = "*{}*".format(self.stringstack["UserWasJoinedGuildNo"].format(member.mention,len(member.guild.members)))
			e.color = 0xCE3232
			e.set_thumbnail(url=str(guild.icon_url))
			e.set_footer(text="{} : {}".format(guild.id, t))
			await self.get_my_channel("guild").send(embed=e)

	async def on_message(self, message) :
		#print(self.waitForMessage)
		if message.channel.id in self.waitForMessage :
			if message.author.id in self.waitForMessage[message.channel.id] :
				if self.waitForMessage[message.channel.id][message.author.id] == 1 :
					await message.channel.send(":thinking:")
					del self.waitForMessage[message.channel.id][message.author.id]
					await self.process_commands(message)
					return
		if message.activity :
			if message.activity["type"] == 3 :
				await message.channel.send(self.stringstack["Response"]["UserSentActivitiesSpotify"])
		#if message.mention_everyone :
		#	await message.channel.send(stringstack["th"]["_response_everyone"])
		else :
			for user in message.mentions :
				if user.id == self.user.id :
					if message.author.id != self.user.id :
						if not message.content.startswith(self.command_prefix) :
							await message.channel.send(self.stringstack["Response"]["UserSentBot"].format(message.author.mention))

							if not message.channel.id in self.waitForMessage :
								self.waitForMessage[message.channel.id] = {}
							self.waitForMessage[message.channel.id][message.author.id] = 1
					else :
						await message.channel.send(self.stringstack["Response"]["BotSentItself"])
		await self.process_commands(message)
