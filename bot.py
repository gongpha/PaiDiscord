import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='<<?')
@bot.event
async def on_ready():
	print('>> login as')
	print(bot.user.name)
	print(bot.user.id)
	print('<<')
	
@bot.command()
async def greet(ctx):
	await ctx.send("WORKS!")
@bot.command()
async def add(ctx, a: int, b: int):
	await ctx.send(">> " + a+b)
@bot.command()
async def sub(ctx, a: int, b: int):
	await ctx.send(">> " + a-b)
@bot.command()
async def mul(ctx, a: int, b: int):
	await ctx.send(">> " + a*b)
@bot.command()
async def div(ctx, a: int, b: int):
	await ctx.send(">> " + a/b)
	
bot.run('NDU3OTA4NzA3ODE3NDIyODYw.Dhp6wg.tgMLnRYz-43-1Z5x5X-AKHKPXUs')