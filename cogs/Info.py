import discord
import platform
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import embed_t, embed_em, embed_wm
from pytz import timezone
from utils.thai_format import th_format_date_diff
from pythainlp.util import thai_strftime
from dateutil.relativedelta import relativedelta
from utils.anyuser import AnyUser
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
		h.color = self.bot.theme[1] if isinstance(self.bot.theme,(list,tuple)) else self.bot.theme
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

		e.add_field(name=ctx.bot.stringstack["Model"]["Name"], value=object, inline=True)
		if isinstance(object, discord.Member) :
			e.add_field(name=ctx.bot.stringstack["Model"]["Nickname"], value=object.nick or ctx.bot.stringstack["None"], inline=True)
		e.add_field(name=ctx.bot.stringstack["CreatedAt"],value=thai_strftime(object.created_at, ctx.bot.stringstack["DateTimeText"].format(th_format_date_diff(ctx, object.created_at.astimezone(timezone(ctx.bot.timezone))))), inline=True)
		if isinstance(object, discord.Member) :
			e.add_field(name=ctx.bot.stringstack["JoinedGuildAt"].format(ctx.message.guild),value=thai_strftime(object.joined_at, ctx.bot.stringstack["DateTimeText"].format(th_format_date_diff(ctx, object.joined_at.astimezone(timezone(ctx.bot.timezone))))), inline=True)
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
				return [self.bot.ss("Status", SSS),d_status_icon[SSS]]
			if not object.bot :
				status_all = "\n\n{1} **{2}** : {0}\n{4} **{5}** : {3}\n{7} **{8}** : {6}".format(
					"🖥️ " + ctx.bot.stringstack["Model"]["Desktop"],
					status_indicator[sss(object.desktop_status)][1], status_indicator[sss(object.desktop_status)][0],
					"🌐 " + ctx.bot.stringstack["Model"]["Web"],
					status_indicator[sss(object.web_status)][1], status_indicator[sss(object.web_status)][0],
					"📱 " + ctx.bot.stringstack["Model"]["Mobile"],
					status_indicator[sss(object.mobile_status)][1], status_indicator[sss(object.mobile_status)][0],
				)
			else :
				status_all = ""
			status_one = "{0} **{1}**{2}".format(status_indicator[1], status_indicator[0],status_all)
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
		e.add_field(name=self.bot.stringstack["Model"]["Name"], value=ctx.bot.user, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["BotName"], value=ctx.bot.bot_name, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["ID"], value=ctx.bot.user.id, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["Discriminator"], value=ctx.bot.user.discriminator, inline=True)
		m_t = psutil.virtual_memory()[3]
		m_a = psutil.virtual_memory()[0]
		mm_t = convert_size(m_t)
		mm_a = convert_size(m_a)
		e.add_field(name=self.bot.stringstack["Model"]["Memory"], value=self.bot.stringstack["PercentUsagedFrom"].format(str(psutil.virtual_memory()[2]), "[{} / {}]\n{}".format(mm_t, mm_a, progressbar(m_t, m_a))), inline=True)
		cpu = psutil.cpu_percent()
		e.add_field(name=self.bot.stringstack["Model"]["CPU"], value=self.bot.stringstack["PercentUsagedNewLine"].format(str(cpu), progressbar(cpu, 100)), inline=True)
		#print(self.bot.start_time.astimezone(timezone(self.bot.timezone)))
		e.add_field(name=self.bot.stringstack["SystemUpTime"], value=th_format_date_diff(ctx, self.bot.start_time.astimezone(timezone(self.bot.timezone))), inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["Ping"], value=str(round(ctx.bot.ws.latency * 1000)) + " ms", inline=True)










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
		e.add_field(name=self.bot.stringstack["Model"]["Emoji"], value=len(ctx.bot.emojis), inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["CacheMessage"], value=len(ctx.bot.cached_messages), inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["VoiceClient"], value=len(ctx.bot.voice_clients), inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["User"], value=len(ctx.bot.users), inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["Member"], value=mm, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["Channel"], value=tc + vc, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["TextChannel"], value=tc, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["VoiceChannel"], value=vc, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["CategoryChannel"], value=ca, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["Role"], value=rr, inline=True)
		e.add_field(name=self.bot.stringstack["Model"]["Guild"], value=len(ctx.bot.guilds), inline=True)

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

	@IsNotDM()
	@commands.command()
	async def guild(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)
		guild = ctx.message.guild
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
		member, passed = await AnyUser.convert(ctx,obj)
		if passed < 0 :
			err = embed_em(ctx, self.bot.stringstack["ObjectNotFoundFromObject"].format(self.bot.stringstack["Model"]["User"], str(obj)))
			#err.description = "```{}```".format(result.text)
			err.set_footer(text="{} : {} : {}".format(member.status, member.code, passed))
			await ctx.send(embed=err)
		#async with ctx.typing() :
		await ctx.send("`{}` : {}".format(member, member.avatar_url_as(format="png")))

	@commands.command()
	async def anyuser(self, ctx, *, obj = None) :
		result, passed = await AnyUser.convert(ctx,obj)
		if passed < 0 :
			err = embed_em(ctx, self.bot.stringstack["ObjectNotFoundFromObject"].format(self.bot.stringstack["Model"]["User"], str(obj)))
			#err.description = "```{}```".format(result.text)
			err.set_footer(text="{} : {} : {}".format(result.status, result.code, passed))
			await ctx.send(embed=err)
		else :
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
		result, passed = await AnyUser.convert(ctx,obj)
		if passed < 0 :
			err = embed_em(ctx, self.bot.stringstack["ObjectNotFoundFromObject"].format(self.bot.stringstack["Model"]["User"], str(obj)))
			#err.description = "```{}```".format(result.text)
			err.set_footer(text="{} : {} : {}".format(result.status, result.code, passed))
			await ctx.send(embed=err)
		else :
			async with ctx.message.channel.typing() :
				ee = await self.profile_information(ctx,result)
				await ctx.send(embed=ee)

	@commands.command()
	async def ping(self, ctx) :
		await ctx.send(self.bot.stringstack["PingReturnedSec"].format(ctx.bot.latency))
def setup(bot) :
	bot.add_cog(loadInformation(Info(bot)))
