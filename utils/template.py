import discord
import asyncio
import random
from discord.utils import escape_mentions
from pytz import timezone
from sys import platform as _platform
import datetime
from pytz import timezone
import math

defcol = 0x36393F

def embed_t(ctx, title = "", description = "", casesensitive = False) :
	e = discord.Embed()
	#print(e.color)

	if isinstance(ctx.me, discord.Member) :
		e.color = ctx.me.color
	elif isinstance(ctx.me, (discord.User, discord.ClientUser)) :
		e.color = defcol
	#if isinstance(ctx.bot.theme, (list, tuple)) :
	#	e.color = ctx.bot.theme[1] if len(ctx.bot.theme) > 1 else ctx.bot.theme[0]
	#else :
	#	e.color = ctx.bot.theme

	e.description = description
	e.title = title
	if not isinstance(ctx.message.channel, discord.DMChannel) :
		e.set_footer(text=ctx.bot.ss("RequestBy").format(ctx.author.display_name) + (" • " + ctx.bot.ss('DontForgetCaseSensitive')) if casesensitive else "", icon_url=ctx.message.author.display_avatar.url)
	elif casesensitive :
		e.set_footer(text=ctx.bot.ss('DontForgetCaseSensitive'), icon_url=ctx.message.author.display_avatar.url)

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
			e.set_footer(text=ctx.bot.ss("RequestBy").format(ctx.author), icon_url=ctx.message.author.display_avatar.url)
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
			e.set_footer(text=ctx.bot.ss("RequestBy").format(ctx.author), icon_url=ctx.message.author.display_avatar.url)
	return e

_NEED_L10N = "AaBbCcDFGgvXxYy+"  # flags that need localization
_EXTENSIONS = "EO-_0#" # extension flags

# https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/util/date.py#L82
def _local_strftime(datetime: datetime.datetime, fmt_char: str, be, ctx) -> str:

	_abbr_weekdays = [
		ctx.bot.ss('Date', '_Monday'),
		ctx.bot.ss('Date', '_Tuesday'),
		ctx.bot.ss('Date', '_Wednesday'),
		ctx.bot.ss('Date', '_Thursday'),
		ctx.bot.ss('Date', '_Friday'),
		ctx.bot.ss('Date', '_Saturday'),
		ctx.bot.ss('Date', '_Sunday')
	]
	_full_weekdays = [
		ctx.bot.ss('Date', 'Monday'),
		ctx.bot.ss('Date', 'Tuesday'),
		ctx.bot.ss('Date', 'Wednesday'),
		ctx.bot.ss('Date', 'Thursday'),
		ctx.bot.ss('Date', 'Friday'),
		ctx.bot.ss('Date', 'Saturday'),
		ctx.bot.ss('Date', 'Sunday')
	]

	_full_months = [
		ctx.bot.ss('Date', 'January'),
		ctx.bot.ss('Date', 'February'),
		ctx.bot.ss('Date', 'March'),
		ctx.bot.ss('Date', 'April'),
		ctx.bot.ss('Date', 'May'),
		ctx.bot.ss('Date', 'June'),
		ctx.bot.ss('Date', 'July'),
		ctx.bot.ss('Date', 'August'),
		ctx.bot.ss('Date', 'September'),
		ctx.bot.ss('Date', 'October'),
		ctx.bot.ss('Date', 'November'),
		ctx.bot.ss('Date', 'December')
	]
	_abbr_months = [
		ctx.bot.ss('Date', '_January'),
		ctx.bot.ss('Date', '_February'),
		ctx.bot.ss('Date', '_March'),
		ctx.bot.ss('Date', '_April'),
		ctx.bot.ss('Date', '_May'),
		ctx.bot.ss('Date', '_June'),
		ctx.bot.ss('Date', '_July'),
		ctx.bot.ss('Date', '_August'),
		ctx.bot.ss('Date', '_September'),
		ctx.bot.ss('Date', '_October'),
		ctx.bot.ss('Date', '_November'),
		ctx.bot.ss('Date', '_December')
	]

	str_ = ""
	if fmt_char == "A":
		str_ = _full_weekdays[datetime.weekday()]
	elif fmt_char == "a":
		str_ = _abbr_weekdays[datetime.weekday()]
	elif fmt_char == "B":
		str_ = _full_months[datetime.month - 1]
	elif fmt_char == "b":
		str_ = _abbr_months[datetime.month - 1]
	elif fmt_char == "C":
		str_ = str(int((datetime.year + (543 if be else 0)) / 100) + 1)
	elif fmt_char == "c":
		str_ = "{:<2} {:>2} {} {} {}".format(
			_abbr_weekdays[datetime.weekday()],
			datetime.day,
			_abbr_months[datetime.month - 1],
			datetime.strftime("%H:%M:%S"),
			datetime.year + (543 if be else 0),
		)
	elif fmt_char == "D":
		str_ = "{}/{}".format(datetime.strftime("%m/%d"), str(datetime.year + ((543 if be else 0) if be else 0))[-2:])
	elif fmt_char == "F":
		str_ = "{}-{}".format(str(datetime.year + (543 if be else 0)), datetime.strftime("%m-%d"))
	elif fmt_char == "G":
		str_ = str(int(datetime.strftime("%G")) + (543 if be else 0))
	elif fmt_char == "g":
		str_ = str(int(datetime.strftime("%G")) + (543 if be else 0))[-2:]
	elif fmt_char == "v":
		str_ = "{:>2}-{}-{}".format(
			datetime.day, _abbr_months[datetime.month - 1], datetime.year + (543 if be else 0)
		)
	elif fmt_char == "X":
		str_ = datetime.strftime("%H:%M:%S")
	elif fmt_char == "x":
		str_ = "{}/{}/{}".format(
			_padding(datetime.day), _padding(datetime.month), datetime.year + (543 if be else 0)
		)
	elif fmt_char == "Y":
		str_ = str(datetime.year + (543 if be else 0))
	elif fmt_char == "y":
		str_ = str(datetime.year + (543 if be else 0))[2:4]
	elif fmt_char == "+":
		str_ = "{:<2} {:>2} {} {} {}".format(
			_abbr_weekdays[datetime.weekday()],
			datetime.day,
			_abbr_months[datetime.month - 1],
			datetime.year + (543 if be else 0),
			datetime.strftime("%H:%M:%S"),
		)
	else:
		str_ = datetime.strftime(f"%{fmt_char}")

	return str_


# https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/util/date.py#L161
def local_strftime(ctx, datetime: datetime.datetime, fmt: str) :
	_parts = []

	i = 0
	fmt_len = len(fmt)
	while i < fmt_len:
		str_ = ""
		if fmt[i] == "%":
			j = i + 1
			if j < fmt_len:
				fmt_char = fmt[j]
				if fmt_char in _NEED_L10N:
					str_ = _local_strftime(datetime, fmt_char, ctx.bot.ss('use_buddhist_era'), ctx)
				elif fmt_char in _EXTENSIONS:

					if fmt_char == "-":
						k = j + 1
						if k < fmt_len:
							fmt_char_nopad = fmt[k]
							if (
								fmt_char_nopad in _NEED_L10N
							):
								str_ = _local_strftime(datetime, fmt_char_nopad, ctx.bot.ss('use_buddhist_era'), ctx)
							else:
								str_ = datetime.strftime(f"%-{fmt_char_nopad}")
							i = i + 1
						else:
							str_ = "-"
					elif fmt_char == "_":
						pass
					elif fmt_char == "0":
						pass
					elif fmt_char == "E":
						pass
					elif fmt_char == "O":
						pass

				elif fmt_char:
					str_ = datetime.strftime(f"%{fmt_char}")

				i = i + 1
			else:
				str_ = "%"
		else:
			str_ = fmt[i]

		_parts.append(str_)
		i = i + 1

	_text = "".join(_parts)

	return _text

async def reaction_message_bool(ctx, bot, msg) :
	await msg.add_reaction(emoji="\N{HEAVY CHECK MARK}")
	await msg.add_reaction(emoji="\N{NEGATIVE SQUARED CROSS MARK}")

	def check(reaction, user) :
		if user.id == msg.author_id :
			return str(reaction.emoji) in give

	while True :
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError :
			await msg.clear_reactions()
			return False
		else :
			if str(reaction.emoji) == "\N{HEAVY CHECK MARK}" :
				return True
			if str(reaction.emoji) == "\N{NEGATIVE SQUARED CROSS MARK}" :
				return False

async def waitReactionRequired(ctx, bot, give, ruser, embed) :
	e = embed.copy()
	e.add_field(name=bot.ss("PleaseReactionAllCommander"),value=bot.ss("Empty"))
	msg = await ctx.send(embed=e)
	for em in give :
		#await ctx.send(em.encode('unicode-escape').decode('ASCII'))
		await msg.add_reaction(emoji=em)
	added = []
	def check(reaction, user) :
		if user.id == ruser :
			return str(reaction.emoji) in give and str(reaction.emoji) not in added
	while True :
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError :
			e.clear_fields()
			e.add_field(name=bot.ss("PleaseReactionAllCommander"),value=bot.ss("TimeoutWaitingReaction"))
			await msg.edit(embed=e)
			await msg.clear_reactions()
			return False
		else :
			e.clear_fields()
			added.append(str(reaction.emoji))
			e.add_field(name=bot.ss("PleaseReactionAllCommander"),value=" ".join(added))
			if set(added) == set(give) :
				return True
			await msg.edit(embed=e)

async def extract_str(ctx, string, count = None, char = '|') :
	t = string.split('|')
	if count == None :
		return t
	if len(t) != count :
		em = embed_em(ctx, ctx.bot.ss('TooManyOrFewInput'), ctx.bot.ss('ThereAreInputsButWant').format(count, len(t)))
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
	now = now or datetime.datetime.now().astimezone(timezone(ctx.bot.default_timezone))
	time = time.astimezone(timezone(ctx.bot.default_timezone))
	if type(time) is int:
		diff = now - datetime.datetime.fromtimestamp(time)
	elif isinstance(time,datetime.datetime):
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
	now = now or datetime.datetime.now().astimezone(timezone(ctx.bot.default_timezone))
	time = time.astimezone(timezone(ctx.bot.default_timezone))
	if type(time) is int:
		diff = now - datetime.datetime.fromtimestamp(time)
	elif isinstance(time,datetime.datetime):
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
	e.add_field(name=ctx.bot.ss("Model", "Name"), value=escape_mentions(model.name), inline=True)
	if isinstance(model, (discord.Member, discord.User, discord.ClientUser)) :
		nof.append(model.mention)
		e.set_author(name=model.display_name, icon_url=model.display_avatar.url)
		e.set_thumbnail(url=model.display_avatar.url)
		if model.id == ctx.bot.user.id :
			nof.append(':regional_indicator_m: :regional_indicator_e:')
		if model.id == ctx.author.id :
			nof.append(':regional_indicator_y: :regional_indicator_o: :regional_indicator_u:')
	if isinstance(model, discord.Member) :
		if model.id == model.guild.owner_id :
			nof.append(':crown:')

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
		e.color = defcol
	elif isinstance(model, discord.Guild) :
		e.add_field(name=ctx.bot.ss("Model", "Region"),value=ctx.bot.ss("VoiceRegion", model.region), inline=True)
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
	e.add_field(name=ctx.bot.ss("CreatedAt"), value=local_strftime(ctx, model.created_at, get_time_format(ctx)) + "\n" + ctx.bot.ss('OnObject').format(format_date_timediff_short(ctx, model.created_at)), inline=True)
	if isinstance(model, discord.Member) :
		if model.nick :
			e.add_field(name=ctx.bot.ss("Model", "Nickname"), value=escape_mentions(model.nick), inline=True)
		e.add_field(name=ctx.bot.ss("JoinedGuildAt").format(model.guild), value=local_strftime(ctx, model.joined_at, get_time_format(ctx)) + "\n" + ctx.bot.ss('OnObject').format(format_date_timediff_short(ctx, model.joined_at)), inline=True)
		if model.premium_since :
			e.add_field(name=ctx.bot.ss("PremiumSince"), value=local_strftime(ctx, model.premium_since, get_time_format(ctx)) + "\n" + ctx.bot.ss('OnObject').format(format_date_timediff_short(ctx, model.premium_since)), inline=True)
		mt = ctx.bot.get_mutual_guilds(model)
		mt_len = len(mt)
		del mt[5:]
		e.add_field(name="{} : {}".format(ctx.bot.ss("MutualGuildWithBot"), mt_len), value=("`{}`".format(", ".join([m.name for m in mt]) + (", ... {}".format(ctx.bot.ss("AndMoreObject").format(mt_len - len(mt), ctx.bot.ss('Model', 'Guild'), s='s' if ctx.bot.ss('need_s') and mt_len - len(mt) > 1 else '')) if mt_len > 5 else ''))) or ctx.bot.ss("Empty"), inline=False)
		def sss(SSS) :
			return [ctx.bot.ss("Status", SSS.name), ctx.bot.get_resource("", 'Emojis', 'StatusIcons', SSS.name)]
		if not model.bot :
			status_all = "\n\n{1} **{2}** : {0}\n{4} **{5}** : {3}\n{7} **{8}** : {6}".format(
				"🖥️ " + ctx.bot.ss("Model", "Desktop"),
				sss(model.desktop_status)[1], sss(model.desktop_status)[0],
				"🌐 " + ctx.bot.ss("Model", "Web"),
				sss(model.web_status)[1], sss(model.web_status)[0],
				"📱 " + ctx.bot.ss("Model", "Mobile"),
				sss(model.mobile_status)[1], sss(model.mobile_status)[0],
			)
		else :
			status_all = ""
		status_one = "{0} **{1}**{2}".format(sss(model.status)[1], sss(model.status)[0], status_all)
		e.add_field(name=ctx.bot.ss("Model", "Status"), value=status_one, inline=True)
	return e

def embed_list(ctx, list, start = 0, end = None) :
	if end is None:
		end = start + 20
	if len(list) > 0 :
		stri = "```\n"
		stri += "\n".join([x.url for x in list][:20])
		stri += '```'
		print(stri)
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
	e.set_footer(text=str(len(list)))
	return e
