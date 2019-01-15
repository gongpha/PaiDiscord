import discord
import os
import platform
import math
import asyncio
import datetime
import ncfu
import statistics
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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

token = os.environ.get('BOT_TOKEN',None)
openprocch = int(os.environ.get('OPENPROC_CH',None))
botname = "OpenProcess"

cmd_prefix = '::'
bot = commands.Bot(command_prefix=cmd_prefix, description="This is a bot :D")
#bot.remove_command('help')
client = discord.Client()
#bot.remove_command("help")
		
def strWithMonospace(string : str) :
	return '`' + string +'`'
def embed_error(ctxx, strr : str, vall : str) :
	errembed=discord.Embed(title="❌ Oops! There's something error", description="", color=0xff0000)
	errembed.add_field(name=strr,value=vall)
	errembed.set_footer(text='Requested by {0}'.format(ctxx.author), icon_url=ctxx.message.author.avatar_url)
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
async def on_ready():
	print('>> login as')
	print(bot.user.name)
	print(bot.user.id)
	print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
		
class TestCommand:
	@bot.command()
	async def error_embed(ctx, method : str, solution : str) :
		"""Testing Embed with Error"""
		await ctx.send("Here, {}".format(ctx.author), embed=embed_error(ctx, method, solution))
		
class BasicCommand :
	# @bot.command()
	# async def say(ctx):
		# """Just say 'I'm still here.'"""
		# await ctx.send("I'm still here.")
	# @bot.command()
	# async def ncfunamegenmons(ctx):
		# """Use NCFUDemo to generate MONS name (UNSTABLE)"""
		# await ctx.send(">> `"+ ncfuDemo_genMonsGeneral() + "`")
	@bot.command()
	async def ncfunt(ctx, a: str):
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
	@bot.command()
	async def mentionme(ctx):
		"""Ping myself"""
		await ctx.send("<@" + str(ctx.message.author.id) + ">")
	@bot.command()
	async def mention(ctx, idthat : int):
		"""Ping Him!"""
		await ctx.send("<@" + str(idthat) + ">")
	@bot.command()
	async def myavatar(ctx):
		"""Your Avatar URL"""
		await ctx.send("`" + str(ctx.message.author) + "` : " + str(ctx.message.author.avatar_url))
	@bot.command()
	async def avatar(ctx, idthat):
		"""His Avatar URL"""
		if not str.isdigit(idthat) :
			user = await bot.get_user_info(ctx.message.mentions[0].id)
		else :
			user = await bot.get_user_info(idthat)
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

class ImageCommand:
	@bot.command(pass_context=True)
	async def infoimg(ctx, rawuser):
		if not str.isdigit(rawuser) :
			user = await bot.get_user_info(ctx.message.mentions[0].id)
		else :
			user = await bot.get_user_info(rawuser)
		img = Image.open("background.png")
		draw = ImageDraw.Draw(img)
		fontsmall = ImageFont.truetype("plat.ttf", 22)
		font = ImageFont.truetype("plat.ttf", 32)
		fontbig = ImageFont.truetype("plat.ttf", 64)

		response = requests.get(user.avatar_url)
		av = Image.open(BytesIO(response.content))
		av.thumbnail((128,128), Image.ANTIALIAS)
		img.paste(av,(100,64))
		draw.text((260, 64), user.name, (0, 0, 0), font=fontbig)
		# display_name
		draw.text((100, 38), ">> {}".format(ctx.message.author.name), (220, 220, 220), font=fontsmall)
		draw.text((260, 128), str(user.id), (0, 0, 0), font=font)
		#draw.text((5, 140), "User Status : {}".format(user.status), (255, 255, 255), font=font)
		draw.text((260, 164), "Created : {}".format(user.created_at), (50, 50, 50), font=fontsmall)

		# rel = user.relationship
		
		# if rel == None :
			# draw.text((260, 220), "NO RELATIONSHIP", (221, 0, 0), font=fontsmall)
		# else :
			# rel.user = ctx.message.author
			# if rel.type == discord.RelationshipType.friend :
			
		#draw.text((260, 220), "Is friend", (0, 170, 128), font=fontsmall)
			# elif rel.type == discord.RelationshipType.blocked :
				# draw.text((260, 220), "Blocked", (221, 0, 0), font=fontsmall)
			# elif rel.type == discord.RelationshipType.incoming_request :
				# draw.text((260, 220), "Outcomming Request", (255, 201, 15), font=fontsmall)
			# elif rel.type == discord.RelationshipType.outgoing_request :
				# draw.text((260, 220), "Incomming Request", (255, 201, 15), font=fontsmall)

		if user.is_avatar_animated() :
			draw.text((100, 195), "Animated", (131, 6, 255), font=fontsmall)


		#mutual_friends()
		# friend = await user.mutual_friends()
		# for ind,f in enumerate(friend) :
			# draw.text((900-draw.textsize(f, fontsmall)[0], 48+(ind*25)), f, (0, 0, 0), font=fontsmall)
		img.save('datinfo.png')
		file = discord.File("datinfo.png", filename="datinfo.png")
		await ctx.send(file=file)
	@bot.command()
	async def blur(ctx, url, scale):
		"""Blur Image"""
		

@bot.command()
async def helpNew(ctx) :
	commands={}
	commands[strWithMonospace(cmd_prefix+'null')]='null'
	
	msgh=discord.Embed(title='', description="written by gongpha#0394\nPowered by discord.py {} with Python {}".format(discord.__version__, platform.python_version()),color=0x9B59B6)
	for command,description in commands.items():
			msgh.add_field(name=command,value=description, inline=False)
	msgh.set_footer(text='Requested by {0}'.format(ctx.author), icon_url=ctx.message.author.avatar_url)
	msgh.set_author(name="OpenProcess Information", icon_url="https://cdn.discordapp.com/avatars/457908707817422860/8d55af0c7e489818c9a8d3bd3b90eccc.webp?size=1024")
	#msgh.set_thumbnail(url=ctx.author.avatar_url)
	await ctx.send("", embed=msgh)

#bot.add_cog(TestCommand())
#bot.add_cog(BasicCommand())
#bot.add_cog(StatsCommand())
bot.loop.create_task(status_task())
bot.run(token)