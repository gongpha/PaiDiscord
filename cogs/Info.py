import discord
import platform
from discord.ext import commands
import typing
from io import BytesIO
from utils.cog import Cog, loadInformation
from utils.template import embed_t, embed_em, embed_wm
from pytz import timezone
from utils.thai_format import th_format_date_diff
from pythainlp.util import thai_strftime
from dateutil.relativedelta import relativedelta
from utils.anyuser import anyuser_safecheck, anyuser_convert
from utils.anyemoji import anyemoji_convert
from utils.query import fetchone, commit
from utils.check import *
import datetime
import math
import psutil
from utils.defined import d_status_icon

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0 B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

def progressbar(iteration, total, length = 10):
	filledLength = int(length * iteration // total)
	bar = '●' * filledLength + '○' * (length - filledLength)
	return bar

class Info(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	def help_overview_embed(self, ctx) :
		h = embed_t(ctx, "❔ {}".format(self.stringstack["Help"]), "")
		h.color = (self.bot.theme[1] if isinstance(self.bot.theme,(list,tuple)) else self.bot.theme) if len(self.bot.theme) > 1 else self.bot.theme[0]
		for n, c in self.bot.cogs.items() :
			if not c.cog_hidden :
				h.add_field(name=":{}: {}".format(": :".join(c.cog_emoji), c.cog_name),value=f"`{self.bot.command_prefix}{ctx.command.name} {c.qualified_name}`",inline=True) # +"\n".join([f"`{self.bot.command_prefix}{i} {c.qualified_name}`" for i in ctx.command.aliases])
		return h

	def help_specific_embed(self, ctx, cog) :
		h = embed_t(ctx, ":{}: {}".format(": :".join(cog.cog_emoji), cog.cog_name), cog.cog_desc)
		if not cog.get_commands() :
			h.add_field(name="﻿",value="*{}*".format(self.bot.stringstack["NoCommand"]))
		for c in cog.get_commands() :
			#h.add_field(name="`{}{}` {}".format(self.bot.command_prefix, c.name, "📡" if c.sql else ""),value=c.description.format(ctx.bot) or ctx.bot.stringstack["Empty"],inline=True)
			h.add_field(name="`{}{}`".format(self.bot.command_prefix, c.name),value=(c.description or "").format(ctx.bot) or ctx.bot.stringstack["Empty"],inline=True)
		return h

	def help_command_embed(self, ctx, command, cog) :
		h = embed_t(ctx, "{}**{}**    (:{}: {})".format(self.bot.command_prefix, command.name, ": :".join(cog.cog_emoji), cog.cog_name), ((command.description) or "") + ("\n\n`{}{} {}`".format(self.bot.command_prefix, command.name, command.usage or "")))
		#if command.sql :
		#	h.description += "\n📡 **{}**".format(self.bot.stringstack["CommandNeedQuery"])
		return h

	async def profile_information(self, ctx, object) :
		r = await fetchone(self.bot, "SELECT profile_name, profile_description, credits, commands FROM pai_discord_profile WHERE snowflake = %s", object.id)

		if object.bot :
			e = embed_wm(ctx, ctx.bot.stringstack["CannotUseWithBot"])
		else :
			new = False
			t = 0
			if not r["result"] and r["rows"] == 0 :
				new = True
				try :
					fromid = ctx.message.guild.id
				except AttributeError :
					fromid = ctx.message.channel.id
				t = await commit(self.bot, "INSERT INTO `pai_discord_profile` (`snowflake`, `profile_name`, `profile_description`, `first_seen`, `first_seen_in_guild`, `credits`, `owner`, `badges`, `level`, `exp`) VALUES (%s, '', '', %s, %s, 0, 0, '{}', 1, 0)", (object.id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), fromid))
				r = {
					"result" : {
						"profile_name" : object.display_name + " *",
						"profile_description" : "",
						"credits" : 0
					}
				}
			e = embed_t(ctx, "", r["result"]["profile_description"])
			e.color = object.color if object.color.value != 0 else discord.Embed.Empty

			e.add_field(name=":credit_card: " + ctx.bot.stringstack["Model"]["Credit"], value=r["result"]["credits"], inline=True)
			e.add_field(name=":arrow_upper_left: " + ctx.bot.stringstack["CommandUsedCount"], value=r["result"]["commands"], inline=True)
			e.set_author(name=r["result"]["profile_name"] or object, icon_url=object.avatar_url)
			e.set_footer(text="🆔 {} : ⏲ {}".format(object.id, ctx.bot.stringstack["QueryExecuteTime"].format(r["time"] if not new else t)))


		return e

	async def user_information(self, ctx, object) :
		nof = [object.mention, str(object.id)]
		if object.bot :
			nof.append("🤖")
		e = embed_t(ctx, "", " : ".join(nof))
		e.color = object.color if object.color.value != 0 else discord.Embed.Empty
		cc = discord.ext.commands.clean_content()
		e.add_field(name=ctx.bot.stringstack["Model"]["Name"], value=await cc.convert(ctx, object.name), inline=True)
		if isinstance(object, discord.Member) :
			e.description += "\n" + ctx.bot.ss('InformationFromServer').format(str(object.guild))
			e.add_field(name=ctx.bot.stringstack["Model"]["Nickname"], value=await cc.convert(ctx, object.nick) or ctx.bot.stringstack["None"], inline=True)
		e.add_field(name=ctx.bot.stringstack["CreatedAt"],value=thai_strftime(object.created_at, get_time_format(ctx).format(th_format_date_diff(ctx, object.created_at))), inline=True)
		if isinstance(object, discord.Member) :
			e.add_field(name=ctx.bot.stringstack["JoinedGuildAt"].format(object.guild),value=thai_strftime(object.joined_at, get_time_format(ctx).format(th_format_date_diff(ctx, object.joined_at))), inline=True)
		e.set_author(name=object.display_name, icon_url=object.avatar_url)

		if isinstance(object, discord.Member) :
			# status_indicator = {
			# 	discord.Status.online : [ctx.bot.stringstack["Status"]["online"], "📗"],
			# 	discord.Status.idle : [ctx.bot.stringstack["Status"]["idle"], "📒"],
			# 	discord.Status.dnd : [ctx.bot.stringstack["Status"]["dnd"], "📕"],
			# 	discord.Status.offline : [ctx.bot.stringstack["Status"]["offline"], "📓"],
			# 	discord.Status.invisible : [ctx.bot.stringstack["Status"]["invisible"], "📓"],
			# }
			def sss(SSS) :
				return [self.bot.ss("Status", SSS.name),d_status_icon[SSS.name]]
			if not object.bot :
				status_all = "\n\n{1} **{2}** : {0}\n{4} **{5}** : {3}\n{7} **{8}** : {6}".format(
					"🖥️ " + ctx.bot.stringstack["Model"]["Desktop"],
					sss(object.desktop_status)[1], sss(object.desktop_status)[0],
					"🌐 " + ctx.bot.stringstack["Model"]["Web"],
					sss(object.web_status)[1], sss(object.web_status)[0],
					"📱 " + ctx.bot.stringstack["Model"]["Mobile"],
					sss(object.mobile_status)[1], sss(object.mobile_status)[0],
				)
			else :
				status_all = ""
			status_one = "{0} **{1}**{2}".format(sss(object.status)[1], sss(object.status)[0], status_all)
			e.add_field(name=ctx.bot.stringstack["Model"]["Status"], value=status_one, inline=True)
		e.set_thumbnail(url=object.avatar_url)
		# if not object.bot :
		# 	ep = embed_t(ctx, ctx.bot.stringstack["Model"]["Profile"], object.mention)
		#
		# 	pro = await object.profile()
		#
		# 	hypesquad_indicator = {
		# 		discord.HypeSquadHouse.bravery : 0x9C81F2,
		# 		discord.HypeSquadHouse.brilliance : 0xF67B63,
		# 		discord.HypeSquadHouse.balance : 0x3ADEC0
		# 	}
		#
		# 	e.color = hypesquad_indicator[hypesquad_houses]

		return e

	# async def user__avatar(self, user : [discord.User, discord.Member]) :
	# 	async with self.session.get(user.avatar_url_as(format="png")) as r :
	# 		avatar = await r.read()
	# 	return (avatar, user.avatar_url_as(format="png"))

	@commands.command()
	async def help(self, ctx, *sect : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		e = None
		h = None
		if not sect :
			h = self.help_overview_embed(ctx)
			e = discord.Embed()
			e.color = self.bot.theme[0] if isinstance(self.bot.theme,(list,tuple)) else self.bot.theme
			e.description = self.bot.bot_description
			e.set_author(name=self.bot.bot_name, icon_url=self.bot.user.avatar_url)
			e.set_footer(text=self.bot.stringstack["Powered"])
		else :
			for n, c in self.bot.cogs.items() :
				#print(n)
				if n == sect[0] :
					h = self.help_specific_embed(ctx, c)
			if h == None :
				for n, cg in self.bot.cogs.items() :
					for c in cg.get_commands() :
						c_a = c.aliases.copy()
						c_a.insert(0, c.name)
						if sect[0] in c_a :
							h = self.help_command_embed(ctx, c, cg)
							break

		#msgh.set_thumbnail(url=ctx.author.avatar_url)
		if e != None :
			await ctx.send(embed=e)
		if h != None :
			await ctx.send(embed=h)

	@commands.command()
	async def stats(self, ctx) :
		e = embed_t(ctx, self.bot.stringstack["StatsOf"].format(ctx.bot.bot_name))
		e.set_author(name=ctx.bot.bot_name, icon_url=self.bot.user.avatar_url)
		e.set_thumbnail(url=(await ctx.bot.application_info()).icon_url)
		s = "**{}** : {}\n"
		e.description += s.format(self.bot.stringstack["Model"]["Name"], ctx.bot.user)
		e.description += s.format(self.bot.stringstack["Model"]["BotName"], ctx.bot.bot_name)
		e.description += s.format(self.bot.stringstack["Model"]["ID"], ctx.bot.user.id)
		e.description += s.format(self.bot.stringstack["Model"]["Discriminator"], ctx.bot.user.discriminator)
		m_t = psutil.virtual_memory()[3]
		m_a = psutil.virtual_memory()[0]
		mm_t = convert_size(m_t)
		mm_a = convert_size(m_a)
		e.description += s.format(self.bot.stringstack["Model"]["Memory"], self.bot.stringstack["PercentUsagedFrom"].format(str(psutil.virtual_memory()[2]), "[{} / {}] | {}".format(mm_t, mm_a, progressbar(m_t, m_a))))
		cpu = psutil.cpu_percent()
		e.description += s.format(self.bot.stringstack["Model"]["CPU"], self.bot.stringstack["PercentUsagedNewLine"].format(str(cpu), progressbar(cpu, 100)))
		e.description += s.format(self.bot.stringstack["SystemUpTime"], th_format_date_diff(ctx, self.bot.start_time.astimezone(timezone(self.bot.timezone))))
		e.description += s.format(self.bot.stringstack["Model"]["Ping"], str(round(ctx.bot.ws.latency * 1000)) + " ms")










		# SET YOUR STATE HERE
		#public_now = False

		#if ctx.author.id in ctx.bot.owner_list :
		#	public_now = True
		mm = 0
		tc = 0
		vc = 0
		ca = 0
		rr = 0
		for guild in ctx.bot.guilds :
			mm += len(guild.members)
			tc += len(guild.text_channels)
			vc += len(guild.voice_channels)
			ca += len(guild.categories)
			rr += len(guild.roles)
		#pe = e.copy()
		e.description += "\n"
		e.description += s.format(self.bot.stringstack["Model"]["Emoji"], len(ctx.bot.emojis))
		e.description += s.format(self.bot.stringstack["Model"]["CacheMessage"], len(ctx.bot.cached_messages))
		e.description += s.format(self.bot.stringstack["Model"]["VoiceClient"], len(ctx.bot.voice_clients))
		e.description += s.format(self.bot.stringstack["Model"]["User"], len(ctx.bot.users))
		e.description += s.format(self.bot.stringstack["Model"]["Member"], mm)
		e.description += s.format(self.bot.stringstack["Model"]["Channel"], tc + vc)
		e.description += s.format(self.bot.stringstack["Model"]["TextChannel"], tc)
		e.description += s.format(self.bot.stringstack["Model"]["VoiceChannel"], vc)
		e.description += s.format(self.bot.stringstack["Model"]["CategoryChannel"], ca)
		e.description += s.format(self.bot.stringstack["Model"]["Role"], rr)
		e.description += s.format(self.bot.stringstack["Model"]["Guild"], len(ctx.bot.guilds))

		e.add_field(name=self.bot.stringstack["Model"]["Invite"], value="[{}](https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=470019184&scope=bot)".format(self.bot.stringstack["ClickHere"], self.bot.user.id), inline=True)

		e.set_footer(text="Python {} • discord.py {}".format(platform.python_version(), discord.__version__))
		await ctx.send(embed=e)
		#e.set_footer(text=)
		#th_format_date_diff(guild.created_at.astimezone(timezone(self.bot.timezone)))

	@commands.command()
	async def alias(self, ctx, *, sect : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		h = None
		for c in list(self.bot.commands) :
			c_a = c.aliases.copy()
			c_a.insert(0, c.name)
			if sect in c_a :
				h = embed_t(ctx, "{} {} ({})".format(self.stringstack["AliasFor"], sect, c.name) if sect != c.name else "{} {}".format(self.stringstack["AliasFor"], sect), "")
				h.add_field(name=self.bot.stringstack["Model"]["Command"], value=f"`{c.name}`")
				h.add_field(name=self.bot.stringstack["Model"]["Alias"], value="\n".join([f"`{i}`" for i in c.aliases]))
				break
		#msgh.set_thumbnail(url=ctx.author.avatar_url)
		if h != None :
			await ctx.send(embed=h)

	@commands.command()
	async def guild(self, ctx, guild_id) :
		#print(self.bot.name)
		#print(self.bot.description)
		guild = self.bot.get_guild(int(guild_id)) or (ctx.message.guild if isinstance(ctx.message.channel, discord.TextChannel) else None)
		if not guild :
			return
		s = embed_t(ctx, guild.name, "")
		s.set_thumbnail(url=guild.icon_url)
		s.add_field(name=self.bot.stringstack["Model"]["ID"],value=guild.id, inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Region"],value=self.bot.stringstack["VoiceRegion"][guild.region.name], inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Owner"],value=guild.owner.mention, inline=True)
		s.add_field(name=self.bot.stringstack["CreatedAt"],value=thai_strftime(guild.created_at, self.bot.stringstack["DateTimeText"].format(th_format_date_diff(ctx, guild.created_at.astimezone(timezone(self.bot.timezone))))), inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Member"],value=len(guild.members), inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Channel"],value=len(guild.channels), inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Role"],value=len(guild.roles), inline=True)

		await ctx.send(embed=s)

	@commands.command()
	async def avatar(self, ctx, *, obj = None) :
		member = await anyuser_safecheck(ctx,obj)
		#async with ctx.typing() :
		if member :
			file = discord.File(fp=BytesIO(await (member.avatar_url_as(static_format="png")).read()), filename="pai__avatar_{}-168d{}".format(member.display_name, member.id))
			await ctx.send("`{}`".format(member), file=file)

	@commands.command()
	async def anyuser(self, ctx, *, obj = None) :
		result, passed = (await anyuser_safecheck(ctx,obj,True))
		if passed >= 0 :
			ee = await self.user_information(ctx,result)
			enum_pass = {
				0 : self.bot.stringstack["Empty"],
				1 : self.bot.stringstack["Model"]["Member"],
				2 : self.bot.stringstack["Model"]["User"],
				3 : self.bot.stringstack["Model"]["User"] + "++", # RARE CASE TO GET THIS VALUE
				4 : self.bot.stringstack["Model"]["ID"],
			}
			ee.add_field(name=self.stringstack["AnyUser__pass"], value="{} : {}".format(passed, enum_pass[passed]))
			await ctx.send(embed=ee)
	@commands.command()
	async def profile(self, ctx, *, obj = None) :
		result = await anyuser_safecheck(ctx,obj)
		async with ctx.message.channel.typing() :
			ee = await self.profile_information(ctx,result)
			await ctx.send(embed=ee)

	@commands.command()
	async def ping(self, ctx) :
		await ctx.send(self.bot.stringstack["PingReturnedSec"].format(ctx.bot.latency))

	@commands.command()
	async def emoji(self, ctx, emoji_text) :
		emoji, passed = await anyemoji_convert(ctx, emoji_text)
		b = BytesIO(await (emoji.url).read())

		if passed == 4 :
			f = "pai__emoticon_{}{}-174d{}.{}".format("animated_" if emoji.animated else "", emoji.name, emoji.id, "gif" if emoji.animated else "png")
		elif passed < 4 :
			try :
				u = emoji.user
				uid = emoji.user.id
				f = "pai__emoticon_{}{}-174d{}_{}-168d{}_{}-169d{}.{}".format("animated_" if emoji.animated else "", emoji.name, emoji.id, u, uid, emoji.guild_id, emoji.guild.name, "gif" if emoji.animated else "png")
			except :
				f = "pai__emoticon_{}{}-174d{}.{}".format("animated_" if emoji.animated else "", emoji.name, emoji.id, "gif" if emoji.animated else "png")
		else :
			f = "pai__emoticon"


		file = discord.File(fp=b, filename=f)
		await ctx.send(file=file)
def setup(bot) :
	bot.add_cog(loadInformation(Info(bot)))
