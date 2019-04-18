import discord
import os
import platform
import math
import asyncio
import datetime
import ncfu
import statistics
import requests
import traceback
import typing
import sys
from bot_string import *
from bot_config import *
from bot_template import template
from bot_group import *
from io import BytesIO
from imageproc import filter
from imageproc import generate
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from random import randint
from difflib import SequenceMatcher
from numpy import argmax

from utils.discord_image import *
from utils.procimg import get_all_proc
from utils.thai_format import th_format_date_diff
from pythainlp.util import thai_strftime
from dateutil.relativedelta import relativedelta

from pytz import timezone

import random

ncfu_c = ["b", "c", "d","f","g","h","l","m","n","p","q","r","s","t","v","w","y","z"]

ncfu_C = ["b", "c", "ch", "d", "f", "g", "gh", "j", "k", "l", "llr", "m", "n", "nn", "p", "ph", "phpr", "q", "qu", "r", "rt", "rtm", "s", "sh", "t", "th", "v", "vm", "w", "wh", "y", "z"]

ncfu_v = ["a", "e", "i", "o", "u", "y"]

ncfu_V = ["a", "e", "i", "o", "u", "y", "ae", "ai", "au", "ay", "ea", "ee", "ei", "eu", "ey", "ia", "ie", "oe", "oi", "oo", "ou", "ui"]

ncfu_s = ["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "x", "y"]

ncfu_vS = ["ch", "ck", "rd", "ge", "ld", "le", "", "ang", "ar", "ard", "as", "ash", "at", "ath", "augh", "aw", "ban", "bel", "bur", "cer",
		"cha", "che", "dan", "dar", "del", "den", "dra", "dyn", "ech", "eld",
		"elm", "em", "en", "end", "eng", "enth", "er", "ess", "est", "et",
		"gar", "gha", "hat", "hin", "hon", "ia", "ight", "ild", "im", "ina",
		"ine", "ing", "ir", "is", "iss", "it", "kal", "kel", "kim", "kin",
		"ler", "lor", "lye", "mor", "mos", "nal", "ny", "nys", "old", "om",
		"on", "or", "orm", "os", "ough", "per", "pol", "qua", "que", "rad",
		"rak", "ran", "ray", "ril", "ris", "rod", "roth", "ryn", "sam",
		"say", "ser", "shy", "skel", "sul", "tai", "tan", "tas", "ther",
		"tia", "tin", "ton", "tor", "tur", "um", "und", "unt", "urn", "usk",
		"ust", "ver", "ves", "vor", "war", "wor", "yer"]

ncfu_S = ["ch", "ck", "rd", "ge", "ld", "le", "ng", "sh", "th", "gh",
		"ne", "ke", "mp", "ft", "mb", "dt", "ph", "rt", "pt", "mn",
		"nth", "dth", "rth", "mph", "rph", "nph", "st", "sh", "sk",
		"yth", "ythm", "yn", "yh", "lt", "ll", "rn"]

#print "Hello, Dcoder!"
#print S

def ncfuDemo_genMonsGeneral() :
	result = random.choice([random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_C),random.choice(ncfu_C)])+ random.choice([random.choice(ncfu_v),random.choice(ncfu_V)]) + random.choice([random.choice(ncfu_s),random.choice(ncfu_s),random.choice(ncfu_S),random.choice(ncfu_s),"",random.choice(ncfu_vS)]) + random.choice([random.choice([random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_C),random.choice(ncfu_C)])+ random.choice([random.choice(ncfu_v),random.choice(ncfu_V)]) + random.choice([random.choice(ncfu_s),random.choice(ncfu_s),random.choice(ncfu_S),random.choice(ncfu_s),"",random.choice(ncfu_vS),""])]) + random.choice([random.choice([random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_C),random.choice(ncfu_C)])+ random.choice([random.choice(ncfu_v),random.choice(ncfu_V)]) + random.choice([random.choice(ncfu_s),random.choice(ncfu_s),random.choice(ncfu_S),random.choice(ncfu_s),"",random.choice(ncfu_vS),""])]) + random.choice(["proc","ator","","","","","","","","","",""])
	print("Generated : "+result)
	return result;

#print(ncfu_genMonsGeneral())
token = "NDU3OTA4NzA3ODE3NDIyODYw.Dx35MA.bLvFuYszuqXhIboNI5Dj1WmsupM"
openprocch = 530055377249894421
botname = "OpenProcess"

bot_theme = 0x9B59B6
timezone_def = "Asia/Bangkok"
cmd_prefix = '::'
bot = commands.Bot(command_prefix=cmd_prefix, description="This is a bot :D")
bot.remove_command('help')
client = discord.Client()
#bot.remove_command("help")

def strWithMonospace(string : str) :
	return '`' + string +'`'

def embed_error(ctxx, strr : str, vall : str) :
	errembed=discord.Embed(title=stringstack["th"]["_error_title"], description="", color=0xff0000)
	errembed.add_field(name=strr, value=vall)
	errembed.set_footer(text=stringstack["th"]["_request_by"].format(ctxx.author), icon_url=ctxx.message.author.avatar_url)
	return errembed

def embed_error_not_found_meaning(ctx, main : str, orthis : str) :
	return embed_error(ctx, stringstack["th"]["_not_found_with"].format(main), stringstack["th"]["_help_you_mean_this"].format(orthis))

def embed_error_incorrect_meaning(ctx, main : str, orthis : str, what : str) :
	return embed_error(ctx, stringstack["th"]["_incorrect_with"].format(main), stringstack["th"]["_help_you_mean_this_because"].format(orthis, what))

def embed_error_special(ctxx, theerror) :
	errembed=discord.Embed(title=stringstack["th"]["_error_title"], description="", color=0xff0000)
	errorfixstr = ""
	error = getattr(theerror, 'original', theerror)
	print('COMMAND GOT EXPECTION {}:'.format(ctxx.command), file=sys.stderr)
	traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

	if isinstance(theerror, commands.BadArgument) :
		errorstr = "_error_bad_argument"
	elif isinstance(theerror, commands.MissingRequiredArgument) :
		errorstr = "_error_missing_required_argument"
	elif isinstance(theerror, commands.DisabledCommand) :
		errorstr = "_error_disabled_command"
	elif isinstance(theerror, commands.NoPrivateMessage) :
		errorstr = "_error_no_private_message"
	elif isinstance(error, requests.exceptions.MissingSchema) :
		errorstr = "_request_missing_schema"
	elif isinstance(error, discord.NotFound) :
		errorstr = "_error_not_found_user"
	elif isinstance(theerror, commands.CommandInvokeError) :
		errorstr = "_error_command_invoke_error"
		errorfixstr = error
	else :
		errorstr = "_error_unknown"
	errembed.add_field(name=stringstack["th"][errorstr],value=stringstack["th"][errorstr + "_fix"].format(errorfixstr))
	errembed.set_footer(text=stringstack["th"]["_request_by"].format(ctxx.author), icon_url=ctxx.message.author.avatar_url)
	return errembed

def userref(ctx,idthat) :
	if not str.isdigit(idthat) :
		return ctx.message.mentions[0].id
	else :
		return idthat

def userrefs(ctx, idthose) :
	ele = []
	ind = 0
	for e in idthose :
		if not str.isdigit(e) :
			if len(ctx.message.mentions) > ind :
				ele.append(ctx.message.mentions[ind].id)
				ind += 1
		else :
			ele.append(int(e))
	return ele;

def listToIdList(thelist) :
	ele = []
	for u in thelist :
		ele.append(mentionToId(str(u)))
	return ele;

def userlistToMention(ctx, userlist) :
	ele = []
	for u in userlist :
		if not str.isdigit(u) :
			ele.append(u)
		else :
			ele.append("<@" + str(u) + ">")
	return ele;

def IdListToMention(userlist : list) :
	lists = []
	for a in userlist :
		lists.append("<@" + str(a) + ">")
	return lists;

def IdToMention(user) :
	return "<@" + str(user) + ">"

def cmpStrList(str, list, ratio = 0.8) :
	nearestList = []
	nearestListStr = []
	for a in list :
		try:
			if SequenceMatcher(None, a.upper(), str.upper()).ratio() >= ratio :
				return [True]
			else :
				nearestListStr.append(a)
				nearestList.append(SequenceMatcher(None, a.upper(), str.upper()).ratio())
		except AttributeError:
			if SequenceMatcher(None, a, str).ratio() >= ratio :
				return [True]
			else :
				nearestListStr.append(a)
				nearestList.append(SequenceMatcher(None, a, str).ratio())

	max_value = max(nearestList)
	max_index = argmax(nearestList)
	return [False, nearestListStr[max_index]]

	return false

def returnhttpstring(code, subfix = "", localize = "th") :
	# http_code_return = {
    #     200: "zero",
    #     201: "one",
    #     204: "two",
	# 	304: "two",
	# 	400: "two",
	# 	401: "two",
	# 	403: "two",
	# 	404: "two",
	# 	405: "two",
	# 	429: "two",
	# 	502: "two",
    # }
	return stringstack[localize]["_http_status_"+str(code)+subfix]

async def isItMentionOrIdAndValid(user) :
	if str.isdigit(user) :
		try :
			await bot.fetch_user(int(user))
		except discord.NotFound :
			return False
		return True
	else :
		if user.startswith("<@") and user.endswith(">") :
			return True
		else :
			return False

def isItMentionOrId(user) :
	if str.isdigit(user) :
		return True
	else :
		if user.startswith("<@") and user.endswith(">") :
			return True
		else :
			return False

def mentionToId(ctx, mention) :
	if mention == None :
		return ctx.author.id
	result = ""
	result = mention.replace('<@', '')
	result = result.replace('>', '')
	return result

class AnyUser(commands.Converter):
    async def convert(self, ctx, argument):
        print(commands.MemberConvert(ctx, argument))
        return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)


async def getLastImage(ctx) :
	if ctx.message.attachments :
		for a in reversed(ctx.message.attachments) :
			for extname in standalone_image_ext :
				if (a.filename.lower().endswith("." + extname)) :
					return Image.open(BytesIO(requests.get(a.url).content))
	else :
		if ctx.message.embeds :
			for e in reversed(ctx.message.embeds) :
				if e.url != discord.Embed.Empty :
					return Image.open(BytesIO(requests.get(e.url).content))
		else :
			messages = await ctx.channel.history(limit=100).flatten()

			for msg in messages :
				if msg.attachments :
					for a in reversed(msg.attachments) :
						for extname in standalone_image_ext :
							if (a.filename.lower().endswith("." + extname)) :
								return Image.open(BytesIO(requests.get(a.url).content))
				else :
					if msg.embeds :
						for e in reversed(msg.embeds) :
							if e.url != discord.Embed.Empty :
								return Image.open(BytesIO(requests.get(e.url).content))
	return Image.open(BytesIO(requests.get(ctx.author.avatar_url).content))

async def loadImageFrom(ctx, source) :
	async with ctx.channel.typing() :
		url = ""
		if isItMentionOrId(source) :
			object = await bot.fetch_user(mentionToId(source))
				# raise Exception("_error_not_found_user")
				# userobj = await bot.fetch_user(int(mentionToId(source)))
				# if userobj == None :
				# 	await ctx.send("เอิ่ม...",embed=embed_error(ctx, stringstack["th"]["_error_not_found_user"], stringstack["th"]["_error_not_found_user_fix"]))
				# else :
				# 	url = userobj.avatar_url
			if object == None :
				raise discord.NotFound
				return
			url = object.avatar_url
		else :
			url = source

		response = requests.get(url)
		# if response.status_code != 200 :
		# 	raise Exception("_error_http|_http_status_"+str(response.status_code))
		# else:
		return Image.open(BytesIO(response.content))

async def status_task():
	print("Starting Task...")
	await bot.wait_until_ready()
	activitygame = discord.Game(name="อะไรอยู่ไม่รู้")
	await bot.change_presence(activity=activitygame)
	counter = 0
	lastdd = datetime.datetime.now()
	y_be = lastdd.year + 543
	channel = bot.get_channel(openprocch)
	print("Starting Proc Status Task...")
	while not bot.is_closed():
		#await channel.send( "***ONE HOUR ONE NAME*** (mons)")
		#for i in range(10) :
		#	await channel.send("`" + ncfu_genMonsGeneral() + "`")



		counter += 10

		ncfu_mons_embed=discord.Embed(title="ONE HOUR TEN NAMES `mons_standard`", description="Generate 10 names from `ncfunt` using our arguments", color=0x9B59B6)
		ncfu_mons_embed.add_field(name="1", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="2", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="3", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="4", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="5", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="6", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="7", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="8", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="9", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.add_field(name="10", value="`" + ncfu.n_t_generate(ncfu.mons_std) + "`", inline=True)
		ncfu_mons_embed.set_footer(text=str(counter) + " names generated. Since last deploy ("+ lastdd.strftime('%d, %B %Y') +" : " + str(y_be))
		await channel.send("",embed=ncfu_mons_embed)




		#await channel.send(str(counter) + " names generated. Since last deploy ("+ str(lastdd)+")")
		print("names : " + str(counter))
		await asyncio.sleep(3600)
	print("!!! WARNING : COUNTER MAYBE RESET")

# @bot.event
# async def on_command_error(ctx, error):
	# if isinstance(error, commands.MissingRequiredArgument):
		# await ctx.send("", embed = embed_error(ctx, "Missing Required Arguments", "Make sure, you put correctly arguments"))
	# elif isinstance(error, commands.BadArgument):
		# await ctx.send("", embed = embed_error(ctx, "Bad Arguments or User not found!", "Make sure, you put correctly arguments, user id or user mention"))
	# elif isinstance(error, commands.DisabledCommand):
		# await ctx.send("", embed = embed_error(ctx, "This command is disabled", "You cannot use this command"))
	# elif isinstance(error, commands.CommandOnCooldown):
		# await ctx.send("Hey, {}. Cooldown".format(ctx.author))
	# elif isinstance(error, commands.MissingPermissions):
		# await ctx.send("", embed = embed_error(ctx, "You haven't permission!", "You cannot use this command"))
	# elif isinstance(error, commands.ConversionError):
		# await ctx.send("", embed = embed_error(ctx, "Converting Failed", "Make sure, you put correctly arguments"))
@bot.event
async def on_command_error(ctx, error):
	await ctx.send("มีข้อผิดพลาดจ้า", embed=embed_error_special(ctx, error))

@commands.command()
async def imageproc_run(ctx) :
	await ctx.send("no")

@bot.command()
async def exp__users(ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
	if end is None:
		end = start + 20
	stri = "```"
	for u in range(start, end+1) :
		if u >= len(bot.users) :
			continue
		stri += f"{u}. {bot.users[u]}\n"
	stri += '```'
	e = discord.Embed(title=len(bot.users),color=0x9B59B6)
	e.add_field(name=f"{start} - {end} จาก {len(bot.users)}", value=stri)
	await ctx.send(embed=e)

@bot.command()
async def exp__members(ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
	if end is None:
		end = start + 20
	stri = "```"
	for u in range(start, end+1) :
		if u >= len(bot.users) :
			continue
		stri += f"{u}. {bot.users[u]}\n"
	stri += '```'
	e = discord.Embed(title=len(bot.users),color=0x9B59B6)
	e.add_field(name=f"{start} - {end} จาก {len(bot.users)}", value=stri)
	await ctx.send(embed=e)

@bot.command()
async def exp__member(ctx, *, member : discord.Member) :
	e = discord.Embed(title=f"{str(member)}" + (f" ({member.nick})" if member.nick != None else ""),color=member.top_role.color)
	e.set_thumbnail(url=member.avatar_url)
	e.add_field(name="เข้าร่วม Discord เมื่อ", value=thai_strftime(member.created_at, f"%d %B %Y เวลา %H:%M:%S+(%f)\nเมื่อ {th_format_date_diff(member.created_at.astimezone(timezone(timezone_def)))}"))
	e.add_field(name=f"เข้าร่วม {member.guild.name} เมื่อ", value=thai_strftime(member.joined_at, f"%d %B %Y เวลา %H:%M:%S+(%f)\nเมื่อ {th_format_date_diff(member.joined_at.astimezone(timezone(timezone_def)))}"))
	#e.add_field(name=f"เข้าร่วม {member.gulid.name} เมื่อ", value=thai_strftime(member.joined_at), inline=True)
	await ctx.send(embed=e)

@bot.command()
async def exp__anyuser(ctx, *, that : AnyUser) :

@bot.event
async def on_ready():
	print('>> login as')
	print(bot.user.name)
	print(bot.user.id)
	print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

	procl = get_all_proc('proc/imggen/')
	for p in procl :
		for c in p[0] :
			command_name = c.command_name if c.command_name != None else c
			command_desc = c.local_desc
		proc_name = p[1]
		proc_author = p[2]
		proc_desc = p[3]
		#cmd = commands.command(p.)
		bot.add_command(imageproc_run)

@bot.event
async def on_message(message):
	if message.activity :
		if message.activity["type"] == 3 :
			await message.channel.send(stringstack["th"]["_response_rich_invite_spotify"])
	if message.mention_everyone :
		await message.channel.send(stringstack["th"]["_response_everyone"])
	else :
		for user in message.mentions :
			if user.id == bot.user.id :
				if message.author.id != bot.user.id :
					if not message.content.startswith(cmd_prefix) :
						await message.channel.send(stringstack["th"]["_response_user"].format(message.author.mention))
				else :
					await message.channel.send(stringstack["th"]["_response_self"])
	await bot.process_commands(message)

# @bot.command()
# async def say(ctx):
	# """Just say 'I'm still here.'"""
	# await ctx.send("I'm still here.")
# @bot.command()
# async def ncfunamegenmons(ctx):
	# """Use NCFUDemo to generate MONS name (UNSTABLE)"""
	# await ctx.send(">> `"+ ncfuDemo_genMonsGeneral() + "`")
@bot.command()
async def ncfunt(ctx, *, a: str):
	"""Use NCFU to generate string using own template"""
	await ctx.send(">> `"+ ncfu.n_t_generate(a) + "`")
# @bot.command()
# async def add(ctx, a: int, b: int):
	# """Add 2 Numbers"""
	# await ctx.send(">> `" + str(a+b) + "`")
# @bot.command()
# async def sub(ctx, a: int, b: int):
	# """Subtract 2 Numbers"""
	# await ctx.send(">> `" + str(a-b) + "`")
# @bot.command()
# async def mul(ctx, a: int, b: int):
	# """Multiply 2 Numbers"""
	# await ctx.send(">> `" + str(a*b) + "`")
# @bot.command()
# async def div(ctx, a: int, b: int):
	# """Divide 2 Numbers"""
	# await ctx.send(">> `" + str(a/b) + "`")
# @bot.command()
# async def sqrt(ctx, a: int):
	# """SquareRoot of Number"""
	# await ctx.send(">> `" + str(math.sqrt(a)) + "`")
# @bot.command()
# async def mod(ctx, a: int, b: int):
	# """Modulo 2 Numbers"""
	# await ctx.send(">> `" + str(a%b) + "`")
# @bot.command()
# async def msginfo(ctx):
	# """This Message Information"""
	# await ctx.send("Author : `" + str(ctx.message.author) +
	# "`\nChannel ID : `" + str(ctx.message.channel) + "`\nContent : `" + str(ctx.message.content) + "`")
@bot.command()	  # 1    2      3
async def mention(ctx, idthose : commands.Greedy[discord.Member], count : typing.Optional[int] = 1) :
	# if not count.isdigit() :
	# 	await ctx.send("เดี๋ยว ๆ ๆ",embed=embed_error(ctx, stringstack["th"]["_error_int_is_not_number"].format(stringstack["th"]["_argument_index"].format(2)), stringstack["th"]["_error_int_is_not_number_fix"].format(stringstack["th"]["_argument_index"].format(2))))
	# else :
		# for _ in range(int(count)) :
		# 	for u in IdListToMention(userrefs(ctx, list(idthose))) :
		# 		strout += u
		# await ctx.send(strout)
	if count > 25 :
		count = 25
	async with ctx.channel.typing() :
		for _ in range(int(count)) :
			for u in idthose :
				print(">> Mention to {0} ({1})".format(u,u.id))
				await ctx.send(u.mention)
@bot.command()
async def avatar_png(ctx, rawuser : typing.Optional[str] = None) :
	user = await bot.fetch_user(mentionToId(ctx, rawuser))
	if user.avatar == None :
		url = user.avatar_url
		await ctx.send(stringstack["th"]["_avatar_request"].format(user, url))
	else :
		url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user)
		width, height = Image.open(BytesIO(requests.get(url).content)).size
		await ctx.send(stringstack["th"]["_avatar_request_size"].format(user, "{0} x {1}".format(width, height), url))
@bot.command()
async def avatar(ctx, rawuser : typing.Optional[str] = None):
	user = await bot.fetch_user(mentionToId(ctx, rawuser))
	await ctx.send("`" + str(user) + "` : " + str(user.avatar_url))
@bot.command()
async def mean(ctx, *a):
	await ctx.send(">> `" + str(statistics.mean(list(map(int, a)))) + "`")
@bot.command()
async def h_mean(ctx, *a):
	await ctx.send(">> `" + str(statistics.harmonic_mean(list(map(int, a)))) + "`")
@bot.command()
async def median(ctx, *a):
	await ctx.send(">> `" + str(statistics.median(list(map(int, a)))) + "`")
@bot.command(pass_context=True)
async def infoimg(ctx, *rawuser):
	if not rawuser :
		img = generate.infoimage(ctx, ctx.author, Image.open("template/background.png"))
	else :
		for u in list(rawuser) :
			#user = await bot.fetch_user(mentionToId(u))
			img = generate.infoimage(ctx, await bot.fetch_user(mentionToId(ctx, u)), Image.open("template/background.png"))


		#mutual_friends()
		# friend = await user.mutual_friends()
		# for ind,f in enumerate(friend) :
		# draw.text((900-draw.textsize(f, fontsmall)[0], 48+(ind*25)), f, (0, 0, 0), font=fontsmall)
	img.save('cache/datinfo.png')
	file = discord.File("cache/datinfo.png", filename="datinfo.png")
	await ctx.send(file=file)

@bot.command()
async def gaussianblur(ctx, scale : typing.Optional[int] = 2, url : typing.Optional[str]=None):
	if url == None :
		im = await getLastImage(ctx)
	else :
		im = await loadImageFrom(ctx,url)
	blurim = im.filter(ImageFilter.GaussianBlur(scale))
	blurim.save('cache/gaussianblur.png')
	file = discord.File("cache/gaussianblur.png", filename="gaussianblur.png")
	await ctx.send(file=file)

@bot.command()
async def boxblur(ctx, scale : typing.Optional[int] = 2, url : typing.Optional[str]=None):
	if url == None :
		im = await getLastImage(ctx)
	else :
		im = await loadImageFrom(ctx,url)
	blurim = im.filter(ImageFilter.BoxBlur(scale))
	blurim.save('cache/boxblur.png')
	file = discord.File("cache/boxblur.png", filename="boxblur.png")
	await ctx.send(file=file)

@bot.command()
async def medianimage(ctx, url=None):
	if url == None :
		im = await getLastImage(ctx)
	else :
		im = await loadImageFrom(ctx,url)

	filter.median(im).save('cache/medianimage.png')
	file = discord.File("cache/medianimage.png", filename="medianimage.png")
	await ctx.send(file=file)

@bot.command()
async def ก็มาดิครับ(ctx, *idthose) :
	await ctx.send("ก็มาดิครับ ! " + " กับ ".join(userlistToMention(ctx, list(idthose))))

@bot.command()
async def resize(ctx, width : str, height : typing.Optional[str] = "asWidth", resample : typing.Optional[str] = "bilinear", url : typing.Optional[str] = None):
	if url == None :
		im = await getLastImage(ctx)
	else :
		im = await loadImageFrom(ctx,url)

	if width.endswith("%") :
		width = int((int(width.replace('%', '')) / 100) * im.width)

	if height == "asWidth" :
		height = width
	else :
		if height.endswith("%") :
			height = int((int(height.replace('%', '')) / 100) * im.height)

	resamp = {
		"nearest" : Image.NEAREST,
		"bilinear" : Image.BILINEAR,
		"bicubic" : Image.BICUBIC,
		"lanczos" : Image.LANCZOS
	}

	im.resize((int(width), int(height)), resamp.get(resample, lambda: Image.BILINEAR)).save('cache/resize.png')
	file = discord.File("cache/resize.png", filename="resize.png")
	await ctx.send(file=file)

@bot.command()
async def topline(ctx, *, text : str) :
	im = await getLastImage(ctx)
	generate.topline_karaoke(text,im,None,randint(10,100), 0, 0).save('cache/toplinediamond.png')
	file = discord.File("cache/toplinediamond.png", filename="toplinediamond.png")
	await ctx.send(file=file)

# locatev : typing.Optional[int] = 75
@bot.command()
async def toplinekaraoke(ctx, text : str, color : typing.Optional[str] = None, percent : typing.Optional[int] = None, url : typing.Optional[str] = None) :
	if url == None :
		im = await getLastImage(ctx)
	else :
		im = await loadImageFrom(ctx,url)
	if percent == None :
		percent = randint(10,100)
	generate.topline_karaoke(text,im,color,percent, 0, 0).save('cache/toplinediamond.png')
	file = discord.File("cache/toplinediamond.png", filename="toplinediamond.png")
	await ctx.send(file=file)

@bot.command()
async def wanbuaban(ctx, *, text : str) :
	im = await getLastImage(ctx)
	generate.topline_karaoke_wanbuaban(text,im,randint(0,100), 0, 0).save('cache/wanbuaban.png')
	file = discord.File("cache/wanbuaban.png", filename="wanbuaban.png")
	await ctx.send(file=file)

@bot.command()
async def wanbuabankaraoke(ctx, text : str, percent : typing.Optional[int] = None, url : typing.Optional[str] = None) :
	if url == None :
		im = await getLastImage(ctx)
	else :
		im = await loadImageFrom(ctx,url)
	if percent == None :
		percent = randint(0,100)
	generate.topline_karaoke_wanbuaban(text,im,percent, 0, 0).save('cache/wanbuaban.png')
	file = discord.File("cache/wanbuaban.png", filename="wanbuaban.png")
	await ctx.send(file=file)

@bot.command()
async def กูรู้หมดแล้ว(ctx, *, text : str) :
	generate.i_know_who_is(text).save('cache/i_know_who_is.png')
	file = discord.File("cache/i_know_who_is.png", filename="i_know_who_is.png")
	await ctx.send(file=file)

@bot.command()
async def avatar_circle(ctx, rawuser : typing.Optional[str] = None) :
	user = await bot.fetch_user(mentionToId(ctx, rawuser))
	im = avatar_image_circle(user)
	im.save("cache/circle_avatar.png")
	width, height = im.size

	file = discord.File("cache/circle_avatar.png", filename="circle_avatar.png")
	await ctx.send(stringstack["th"]["_avatar_request_nourl"].format(user, "{0} x {1}".format(width, height)),file=file)


@bot.command()
async def help(ctx, sect : typing.Optional[str] = None) :
	if sect == None :
		msgh=discord.Embed(title="", description = stringstack["th"]["_help_desc"],color=0x9B59B6)#.format(discord.__version__, platform.python_version()),color=0x9B59B6)
		for group in command_group :
			msgh.add_field(name=stringstack["th"]["_section_head_" + group],value="`{0}help {1}`".format(cmd_prefix, group), inline=True)
		#for command in bot.commands :
		#	msgh.add_field(name="{0}{1}\n".format(cmd_prefix, command.name), value=command.help, inline=False)
		msgh.add_field(name=stringstack["th"]["_help_more???"],value=stringstack["th"]["_help_other"], inline=False)
	else :
		for group in command_group :
			if group == sect :
				msgh=discord.Embed(title=stringstack["th"]["_section_head_" + group], description="",color=bot_theme)
				for cmd in command_group[group] :
					for command in bot.commands :
						if command.help == cmd or command.name == cmd :
							try :
								reglist = ""
								if len(commandinfo["th"][cmd]) > 2 :
									for r in commandinfo["th"][cmd][2] :
										reglist += "   *{}*".format(r)
										desc = "`{0}`\n{1}\n{2}".format(commandinfo["th"][cmd][1], commandinfo["th"][cmd][0],reglist)
								else :
									desc = "`{0}`\n{1}".format(commandinfo["th"][cmd][1], commandinfo["th"][cmd][0])
								msgh.add_field(name="{0}{1}\n".format(cmd_prefix, command.name),value=desc, inline=True)
							except KeyError :
								msgh.add_field(name="{0}{1}\n".format(cmd_prefix, command.name),value=stringstack["th"]["_unknown"], inline=True)
	msgh.set_footer(text=stringstack["th"]["_request_by"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
	msgh.set_author(name=stringstack["th"]["_bot_name"], icon_url=bot.user.avatar_url)
	#msgh.set_thumbnail(url=ctx.author.avatar_url)
	await ctx.send(stringstack["th"]["_help_title"], embed=msgh)

#bot.add_cog(TestCommand())
#bot.add_cog(BasicCommand())
#bot.add_cog(StatsCommand())
#bot.loop.create_task(status_task())
bot.run(token)
