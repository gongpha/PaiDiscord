import discord
import os
import platform
import math
import asyncio
import datetime
import ncfu
import statistics
from discord.ext import commands

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

#token = os.environ.get('BOT_TOKEN',None)
token = 'NDU3OTA4NzA3ODE3NDIyODYw.Dvf7Lw.vlaheg5ndAFcBDi4v4CwvRJBAA0'
#openprocch = int(os.environ.get('OPENPROC_CH',None))
openprocch = 524035018352230410


bot = commands.Bot(command_prefix='::')
client = discord.Client()
# bot.remove_command("help")

def errtype(etype) :
	if etype == 0 : 
		return "Null Error (IDK Too. What is this XD)"
	elif etype == 1 :
		return "Arguments error"
	else :
		return "Wtf is this ?"
		
def embed_error(ctxx, strr : str, vall : str, etype : int) :
	errembed=discord.Embed(title="❌ Oops! There's something error", description=errtype(etype), color=0xff0000)
	errembed.add_field(name=strr,value=vall)
	return errembed

async def status_task():
	print("Starting Task...")
	await bot.wait_until_ready()
	activitygame = discord.Game(name="Processor")
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
		
		ncfu_mons_embed=discord.Embed(title="ONE HOUR TEN NAMES `mons_standard`", description="Generate 10 names from `ncfunt` using our arguments", color=0xff0080)
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

@bot.event
async def on_ready():
	print('>> OpenProcess by gongpha')
	print('>> login as')
	print(bot.user.name)
	print(bot.user.id)
	print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

class TestCommand:
	@bot.command()
	async def error_embed(ctx, method : str, solution : str, errtype : int) :
		"""Testing Embed with Error"""
		await ctx.send("Here, <@" + str(ctx.message.author.id) + ">", embed=embed_error(ctx, method, solution, errtype))
		
class BasicCommand :
	@bot.command()
	async def say(ctx):
		"""Just say 'I'm still here.'"""
		await ctx.send("I'm still here.")
	@bot.command()
	async def ncfunamegenmons(ctx):
		"""Use NCFUDemo to generate MONS name (UNSTABLE)"""
		await ctx.send(">> `"+ ncfuDemo_genMonsGeneral() + "`")
	@bot.command()
	async def ncfunt(ctx, a: str):
		"""Use NCFU to generate string using own template"""
		await ctx.send(">> `"+ ncfu.n_t_generate(a) + "`")
	@bot.command()
	async def add(ctx, a: int, b: int):
		"""Add 2 Numbers"""
		await ctx.send(">> `" + str(a+b) + "`")
	@bot.command()
	async def sub(ctx, a: int, b: int):
		"""Subtract 2 Numbers"""
		await ctx.send(">> `" + str(a-b) + "`")
	@bot.command()
	async def mul(ctx, a: int, b: int):
		"""Multiply 2 Numbers"""
		await ctx.send(">> `" + str(a*b) + "`")
	@bot.command()
	async def div(ctx, a: int, b: int):
		"""Divide 2 Numbers"""
		await ctx.send(">> `" + str(a/b) + "`")
	@bot.command()
	async def sqrt(ctx, a: int):
		"""SquareRoot of Number"""
		await ctx.send(">> `" + str(math.sqrt(a)) + "`")
	@bot.command()
	async def mod(ctx, a: int, b: int):
		"""Modulo 2 Numbers"""
		await ctx.send(">> `" + str(a%b) + "`")
	@bot.command()
	async def msginfo(ctx):
		"""This Message Information"""
		await ctx.send("Author : `" + str(ctx.message.author) + 
		"`\nChannel ID : `" + str(ctx.message.channel) + "`\nContent : `" + str(ctx.message.content) + "`")
	@bot.command()
	async def mentionme(ctx):
		"""Ping myself"""
		await ctx.send("<@" + str(ctx.message.author.id) + ">")
	@bot.command()
	async def mention(ctx, idthat = None):
		"""Ping Him!"""
		if not str.isdigit(idthat) :
			user = await bot.get_user_info(ctx.message.mentions[0].id)
		else :
			user = await bot.get_user_info(idthat)

		if not idthat:
			await ctx.send("Uh oh, <@" + str(ctx.message.author.id) + ">", embed = embed_error(ctx, "You missed argument!", "Put an argument then try again", 1))
		else : 
			if not user  :
				await ctx.send("Uh oh, <@" + str(ctx.message.author.id) + ">", embed = embed_error(ctx, "User wasn't found in the channel!", "Make sure, you put a correct User ID or that user has been in the channel", 1))
			else :
				await ctx.send("<@" + str(user.id) + ">")

	@bot.command()
	async def myavatar(ctx):
		"""Your Avatar URL"""
		await ctx.send("`" + str(ctx.message.author) + "` : " + str(ctx.message.author.avatar_url))
	@bot.command()
	async def avatar(ctx, idthat = None):
		"""His Avatar URL"""
		if not str.isdigit(idthat) :
			user = await bot.get_user_info(ctx.message.mentions[0].id)
		else :
			user = await bot.get_user_info(idthat)

		if not idthat:
			await ctx.send("Uh oh, <@" + str(ctx.message.author.id) + ">", embed = embed_error(ctx, "You missed argument!", "Put an argument then try again", 1))
		else : 
			if not user  :
				await ctx.send("Uh oh, <@" + str(ctx.message.author.id) + ">", embed = embed_error(ctx, "User wasn't found!", "Make sure, you put a correct User ID or that", 1))
			else :
				await ctx.send("`" + str(user) + "` : " + str(user.avatar_url))

class StatsCommand :
	@bot.command()
	async def mean(ctx, *a):
		"""Finding Arithmetic mean"""
		await ctx.send(">> `" + str(statistics.mean(list(map(int, a)))) + "`")
	@bot.command()
	async def h_mean(ctx, *a):
		"""Finding Harmonic mean"""
		await ctx.send(">> `" + str(statistics.harmonic_mean(list(map(int, a)))) + "`")
	@bot.command()
	async def median(ctx, *a):
		"""Finding Median (Middle)"""
		await ctx.send(">> `" + str(statistics.median(list(map(int, a)))) + "`")

#bot.add_cog(TestCommand())
#bot.add_cog(BasicCommand())
#bot.add_cog(StatsCommand())
bot.loop.create_task(status_task())
bot.run(token)