import discord
import math
from discord.ext import commands
bot = commands.Bot(command_prefix='<<?')

game = 'Processor'
@bot.event
async def on_ready():
	print('>> OpenProcess by gongpha')
	print('>> login as')
	print(bot.user.name)
	print(bot.user.id)
	print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	return await client.change_presence(game=discord.Game(name=game))
	
@bot.command()
async def test(ctx):
	await ctx.send("CURRENTLY WORK!")
@bot.command()
async def add(ctx, a: int, b: int):
	await ctx.send(">> " + str(a+b))
@bot.command()
async def sub(ctx, a: int, b: int):
	await ctx.send(">> " + str(a-b))
@bot.command()
async def mul(ctx, a: int, b: int):
	await ctx.send(">> " + str(a*b))
@bot.command()
async def div(ctx, a: int, b: int):
	await ctx.send(">> " + str(a/b))
@bot.command()
async def sqrt(ctx, a: int):
	await ctx.send(">> " + str(math.sqrt(a)))
@bot.command()
async def mod(ctx, a: int, b: int):
	await ctx.send(">> " + str(a%b))
	
	
	
	
@bot.command()
	async def help(ctx):
		embed = discord.Embed(title="Commands for OpenProcess", description="", color=0x0090FF)
		embed.add_field(name="<<?add A B", value="Gives the addition of **A** and **B**", inline=False) 
		embed.add_field(name="<<?sub A B", value="Gives the subtraction of **A** and **B**", inline=False) 
		embed.add_field(name="<<?mul A B", value="Gives the multiplication of **A** and **B**", inline=False)
		embed.add_field(name="<<?div A B", value="Gives the division of **A** and **B**", inline=False)
		embed.add_field(name="<<?sqrt A", value="Gives the squareRoot of **A**", inline=False)
		embed.add_field(name="<<?mod A B", value="Gives the modulation of **A** and **B**", inline=False)
		embed.add_field(name="<<?test", value="Gives a status of bot", inline=False)
		embed.add_field(name="<<?help", value="Display help message", inline=False)
		await ctx.send(embed=embed)
	
bot.run('NDU3OTA4NzA3ODE3NDIyODYw.Dhp6wg.tgMLnRYz-43-1Z5x5X-AKHKPXUs')