import discord
import asyncio
import random
from discord.utils import escape_mentions
from utils.thai_format import th_format_date_diff
from pythainlp.util import thai_strftime
from pytz import timezone
from sys import platform as _platform
from utils.defined import d_status_icon

def embed_t(ctx, title, description = "") :
	e = discord.Embed()
	#print(e.color)
	e.color = int(random.choice(ctx.bot.theme))
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
		print()
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

def get_time_format(ctx, complex=False) :
	print( ctx.bot.ss('DateTimeTextWindowsComplex'))
	if _platform == "linux" or _platform == "linux2" or _platform == "darwin" :
		return ctx.bot.ss('DateTimeTextUnixComplex' if complex else 'DateTimeTextUnix')
	elif _platform == "win32" or _platform == "win64" :
		return ctx.bot.ss('DateTimeTextWindowsComplex' if complex else 'DateTimeTextWindows')
	else :
		return ""

def member_info(ctx, member) :
	nof = [member.mention, str(member.id)]
	if member.bot :
		nof.append("🤖")
	e = embed_t(ctx, "", " : ".join(nof))
	e.color = member.color
	e.add_field(name=ctx.bot.stringstack["Model"]["Name"], value=escape_mentions(member.name), inline=True)
	e.description += "\n" + ctx.bot.ss('InformationFromServer').format(str(member.guild))
	e.add_field(name=ctx.bot.stringstack["Model"]["Nickname"], value=escape_mentions(member.nick) or ctx.bot.stringstack["None"], inline=True)
	e.add_field(name=ctx.bot.stringstack["CreatedAt"],value=thai_strftime(member.created_at, get_time_format(ctx).format(th_format_date_diff(ctx, member.created_at))), inline=True)
	e.add_field(name=ctx.bot.stringstack["JoinedGuildAt"].format(member.guild),value=thai_strftime(member.joined_at, get_time_format(ctx).format(th_format_date_diff(ctx, member.joined_at))), inline=True)
	e.set_author(name=member.display_name, icon_url=member.avatar_url)

	def sss(SSS) :
		return [ctx.bot.ss("Status", SSS.name), d_status_icon[SSS.name]]
	if not member.bot :
		status_all = "\n\n{1} **{2}** : {0}\n{4} **{5}** : {3}\n{7} **{8}** : {6}".format(
			"🖥️ " + ctx.bot.stringstack["Model"]["Desktop"],
			sss(member.desktop_status)[1], sss(member.desktop_status)[0],
			"🌐 " + ctx.bot.stringstack["Model"]["Web"],
			sss(member.web_status)[1], sss(member.web_status)[0],
			"📱 " + ctx.bot.stringstack["Model"]["Mobile"],
			sss(member.mobile_status)[1], sss(member.mobile_status)[0],
		)
	else :
		status_all = ""
	status_one = "{0} **{1}**{2}".format(sss(member.status)[1], sss(member.status)[0], status_all)
	e.add_field(name=ctx.bot.stringstack["Model"]["Status"], value=status_one, inline=True)
	e.set_thumbnail(url=member.avatar_url)

	return e
