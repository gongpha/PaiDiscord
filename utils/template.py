import discord
import asyncio
import random
from discord.utils import escape_mentions
from pythainlp.util import thai_strftime
from pytz import timezone
from sys import platform as _platform
from utils.defined import d_status_icon
from datetime import datetime
from pytz import timezone
import math

def embed_t(ctx, title, description = "") :
	e = discord.Embed()
	#print(e.color)
	if isinstance(ctx.bot.theme, (list, tuple)) :
		e.color = ctx.bot.theme[1] if len(ctx.bot.theme) > 1 else ctx.bot.theme[0]
	else :
		e.color = ctx.bot.theme
	e.description = description
	e.title = title
	if not isinstance(ctx.message.channel, discord.DMChannel) :
		e.set_footer(text=ctx.bot.stringstack["RequestBy"].format(ctx.author.display_name), icon_url=ctx.message.author.avatar_url)

	return e

def embed_em(ctx, reason, description = "", *args, **kwargs) :
	e = discord.Embed()
	e.color = 0xFF0000
	e.description = description
	e.title = "❌ {}".format(reason)
	if 'error' in kwargs and ctx.bot.dev:
		print()
		e.set_footer(text="{}".format(kwargs.get('error', None)))
	else :
		if not isinstance(ctx.message.channel, discord.DMChannel) :
			e.set_footer(text=ctx.bot.stringstack["RequestBy"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
	return e

def embed_wm(ctx, reason, description = "", *args, **kwargs) :
	e = discord.Embed()
	e.color = 0xFFCC4D
	e.description = description
	e.title = "⚠ {}".format(reason)
	if 'error' in kwargs and ctx.bot.dev:
		e.set_footer(text="{}".format(kwargs.get('error', None)))
	else :
		if not isinstance(ctx.message.channel, discord.DMChannel) :
			e.set_footer(text=ctx.bot.stringstack["RequestBy"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
	return e

async def waitReactionRequired(ctx, bot, give, ruser, embed) :
	e = embed.copy()
	e.add_field(name=bot.stringstack["PleaseReactionAllCommander"],value=bot.stringstack["Empty"])
	msg = await ctx.send(embed=e)
	for em in give :
		#await ctx.send(em.encode('unicode-escape').decode('ASCII'))
		await msg.add_reaction(emoji=em)
	added = []
	def check(reaction, user) :
		if user.id == ruser :
			return str(reaction.emoji) in give and str(reaction.emoji) not in added
	yes = False
	while not yes :
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			e.clear_fields()
			e.add_field(name=bot.stringstack["PleaseReactionAllCommander"],value=bot.stringstack["TimeoutWaitingReaction"])
			await msg.edit(embed=e)
			await msg.clear_reactions()
			return False
		else:
			e.clear_fields()
			added.append(str(reaction.emoji))
			e.add_field(name=bot.stringstack["PleaseReactionAllCommander"],value=" ".join(added))
			if set(added) == set(give) :
				return True
			await msg.edit(embed=e)

async def extract_str(ctx, string, count = None, char = '|') :
	t = string.split('|')
	if count == None :
		return t
	if len(t) != count :
		em = embed_em(ctx, ctx.bot.ss('TooManyInput'), ctx.bot.ss('ThereAreInputsButWant').format(count, len(t)))
		await ctx.send(embed=em)
		return None
	return t

def convert_size(size_bytes) :
	if size_bytes == 0:
		return "0 B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

def get_time_format(ctx, complex=False) :
	if _platform == "linux" or _platform == "linux2" or _platform == "darwin" :
		return ctx.bot.ss('DateTimeTextUnixComplex' if complex else 'DateTimeTextUnix')
	elif _platform == "win32" or _platform == "win64" :
		return ctx.bot.ss('DateTimeTextWindowsComplex' if complex else 'DateTimeTextWindows')
	else :
		return ""

def format_date_timediff_short(ctx, time=False, now=None):
	# from https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python/1551394#1551394
	"""
	Get a datetime object or a int() Epoch timestamp and return a
	pretty string like 'an hour ago', 'Yesterday', '3 months ago',
	'just now', etc
	"""
	now = now or datetime.now().astimezone(timezone(ctx.bot.default_timezone))
	time = time.astimezone(timezone(ctx.bot.default_timezone))
	if type(time) is int:
		diff = now - datetime.fromtimestamp(time)
	elif isinstance(time,datetime):
		diff = now - time
	elif not time:
		diff = now - now
	second_diff = diff.seconds
	day_diff = diff.days

	if day_diff < 0:
		return ''

	if day_diff == 0:
		if second_diff < 10:
			return ctx.bot.ss('Time', 'Recently')
		if second_diff < 60:
			return str(int(second_diff)) + ' ' + ctx.bot.ss('Time', 'SecondsAgo')
		if second_diff < 120:
			return ctx.bot.ss('Time', 'MinutesAgo')
		if second_diff < 3600:
			return str(int(second_diff / 60)) + ' ' + ctx.bot.ss('Time', 'MinutesAgo')
		if second_diff < 7200:
			return ctx.bot.ss('Time', 'HoursAgo')
		if second_diff < 86400:
			return str(int(second_diff / 3600))+ ' ' + ctx.bot.ss('Time', 'HoursAgo')
	if day_diff == 1:
		return ctx.bot.ss('Time', 'Yesterday')
	if day_diff < 7:
		return str(int(day_diff)) + ' ' + ctx.bot.ss('Time', 'DaysAgo')
	if day_diff < 31:
		return str(int(day_diff / 7)) + ' ' + ctx.bot.ss('Time', 'WeeksAgo')
	if day_diff < 365:
		return str(int(day_diff / 30)) + ' ' + ctx.bot.ss('Time', 'MonthsAgo')
	return str(int(day_diff / 365)) + ' ' + ctx.bot.ss('Time', 'YearsAgo')

def format_date_timediff(ctx, time=False, now=None) :
	# from https://stackoverflow.com/a/13756038
	now = now or datetime.now().astimezone(timezone(ctx.bot.default_timezone))
	time = time.astimezone(timezone(ctx.bot.default_timezone))
	if type(time) is int:
		diff = now - datetime.fromtimestamp(time)
	elif isinstance(time,datetime):
		diff = now - time
	elif not time:
		diff = now - now
	seconds = int(diff.total_seconds())
	dss = ctx.bot.ss('Time')
	periods = [
		(dss['Year'],		60*60*24*365),
		(dss['Month'],		60*60*24*30),
		(dss['Day'],		60*60*24),
		(dss['Hour'],		60*60),
		(dss['Minute'],		60),
		(dss['Second'],		1)
	]

	strings=[]
	for period_name, period_seconds in periods:
		if seconds > period_seconds:
			period_value , seconds = divmod(seconds, period_seconds)
			has_s = 's' if period_value and ctx.bot.ss('need_s') > 1 else ''
			strings.append("%s %s%s" % (period_value, period_name, has_s))

	return " ".join(strings)

def model_info(ctx, model) :
	#print(type(model))
	nof = []
	e = embed_t(ctx, str(model))
	e.add_field(name=ctx.bot.stringstack["Model"]["Name"], value=escape_mentions(model.name), inline=True)
	if isinstance(model, (discord.Member, discord.User, discord.ClientUser)) :
		nof.append(model.mention)
		e.set_author(name=model.display_name, icon_url=model.avatar_url)
		e.set_thumbnail(url=model.avatar_url)
		if model.id == ctx.bot.user.id :
			nof.append(':regional_indicator_m: :regional_indicator_e:')
		if model.id == ctx.author.id :
			nof.append(':regional_indicator_y: :regional_indicator_o: :regional_indicator_u:')

	elif isinstance(model, discord.Guild) :
		e.set_author(name=model.name, icon_url=model.icon_url)
		e.set_thumbnail(url=model.icon_url)
		if model.unavailable :
			nof.append('❌')
		if model.premium_tier > 0 :
			nof.append('`{}`'.format(ctx.bot.ss('BoostTierNo').format(model.premium_tier)))
		if (model.premium_subscription_count or 0) > 0 :
			nof.append('`{}`'.format(str(model.premium_subscription_count) + " " + ctx.bot.ss('Model', 'Boost')))
		if model.description :
			nof.append('```{}```'.format(model.description))
	else :
		e.set_author(name=model.name)
	nof.append('`{}`'.format(str(model.id)))
	if isinstance(model, (discord.Member, discord.User, discord.ClientUser)) :
		if model.bot :
			nof.append("🤖")
	e.description = " : ".join(nof)
	if isinstance(model, discord.Member) :
		e.color = model.color
	elif isinstance(model, (discord.User, discord.ClientUser)) :
		e.color = discord.Embed.Empty
	elif isinstance(model, discord.Guild) :
		e.add_field(name=ctx.bot.ss("Model", "Region"),value=ctx.bot.ss("VoiceRegion", model.region.name), inline=True)
		e.add_field(name=ctx.bot.ss("Model", "Owner"),value=model.owner.mention, inline=True)
		c = "\n   -{} : {}"
		e.add_field(name="{} : {}".format(ctx.bot.ss("Model", "Channel"), len(model.channels)),value='{}{}{}'.format(
			c.format(ctx.bot.ss("Model", "TextChannel"), len(model.text_channels)),
			c.format(ctx.bot.ss("Model", "VoiceChannel"), len(model.voice_channels)),
			c.format(ctx.bot.ss("Model", "Category"), len(model.categories)),
		), inline=True)
		user_c = 0
		bot_c = 0
		r_m_c = 0
		r_um_c = 0
		for m in model.members :
			if m.bot :
				bot_c += 1
			else :
				user_c += 1
		for r in model.roles :
			if r.managed :
				r_m_c += 1
			else :
				r_um_c += 1
		e.add_field(name="{} : {}".format(ctx.bot.ss("Model", "Member"), model.member_count), value='{}{}'.format(
			c.format(ctx.bot.ss("Model", "User"), user_c),
			c.format(ctx.bot.ss("Model", "Bot"), bot_c)
		), inline=True)
		e.add_field(name="{} : {}".format(ctx.bot.ss("Model", "Role"), len(model.roles)), value='{}{}'.format(
			c.format(ctx.bot.ss("Model", "UnmanagedRole"), r_um_c),
			c.format(ctx.bot.ss("Model", "ManagedRole"), r_m_c)
		), inline=True)
		e.add_field(name=ctx.bot.ss("Model", "SystemChannel"), value=model.system_channel.mention if model.system_channel else ctx.bot.ss('Empty'), inline=True)
		e.add_field(name="{} : {}".format(ctx.bot.ss("Model", "Boost"), model.premium_subscription_count),value=("```\n{}\n```".format("\n".join([m.name for m in model.premium_subscribers]))) if model.premium_subscribers else ctx.bot.ss("Empty"), inline=True)
		e.add_field(name=ctx.bot.ss("Model", "URL"), value='{}{}{}'.format(
			c.format(ctx.bot.ss("Model", "Icon"), "[{}]({})".format(ctx.bot.ss('ClickHere' if model.icon_url_as(format='png') else 'NoObject'), model.icon_url_as(format='png'))),
			c.format(ctx.bot.ss("Model", "Banner"), "[{}]({})".format(ctx.bot.ss('ClickHere' if model.banner_url_as(format='png') else 'NoObject'), model.banner_url_as(format='png'))),
			c.format(ctx.bot.ss("Model", "Splash"), "[{}]({})".format(ctx.bot.ss('ClickHere' if model.splash_url_as(format='png') else 'NoObject'), model.splash_url_as(format='png')))
		), inline=True)
		e.add_field(name=ctx.bot.ss("Model", "Limits"), value='{}{}{}'.format(
			c.format(ctx.bot.ss("Model", "Emoji"), model.emoji_limit),
			c.format(ctx.bot.ss("Model", "Bitrate"), str(round(model.bitrate_limit / 1000)) + 'Kbps'),
			c.format(ctx.bot.ss("Model", "FileSize"), convert_size(model.filesize_limit)),
		), inline=True)

	if isinstance(model, discord.Member) :
		e.description += "\n" + ctx.bot.ss('InformationFromServer').format(str(model.guild))
	e.add_field(name=ctx.bot.ss("CreatedAt"), value=thai_strftime(model.created_at, get_time_format(ctx)) + "\n" + ctx.bot.ss('WhenObject').format(format_date_timediff_short(ctx, model.created_at)), inline=True)
	if isinstance(model, discord.Member) :
		e.add_field(name=ctx.bot.stringstack["Model"]["Nickname"], value=escape_mentions(model.nick) or ctx.bot.stringstack["None"], inline=True)
		e.add_field(name=ctx.bot.stringstack["JoinedGuildAt"].format(model.guild), value=thai_strftime(model.joined_at, get_time_format(ctx)) + "\n" + ctx.bot.ss('WhenObject').format(format_date_timediff_short(ctx, model.joined_at)), inline=True)
		if model.premium_since :
			e.add_field(name=ctx.bot.stringstack["PremiumSince"], value=thai_strftime(model.premium_since, get_time_format(ctx)) + "\n" + ctx.bot.ss('WhenObject').format(format_date_timediff_short(ctx, model.premium_since)), inline=True)

		def sss(SSS) :
			return [ctx.bot.ss("Status", SSS.name), d_status_icon[SSS.name]]
		if not model.bot :
			status_all = "\n\n{1} **{2}** : {0}\n{4} **{5}** : {3}\n{7} **{8}** : {6}".format(
				"🖥️ " + ctx.bot.stringstack["Model"]["Desktop"],
				sss(model.desktop_status)[1], sss(model.desktop_status)[0],
				"🌐 " + ctx.bot.stringstack["Model"]["Web"],
				sss(model.web_status)[1], sss(model.web_status)[0],
				"📱 " + ctx.bot.stringstack["Model"]["Mobile"],
				sss(model.mobile_status)[1], sss(model.mobile_status)[0],
			)
		else :
			status_all = ""
		status_one = "{0} **{1}**{2}".format(sss(model.status)[1], sss(model.status)[0], status_all)
		e.add_field(name=ctx.bot.stringstack["Model"]["Status"], value=status_one, inline=True)
	return e
