import discord
from discord.ext import commands
from utils.cog import Cog, loadInformation

class MyCog(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def hello(self, ctx) :
		await ctx.send('Hello !')
async def setup(bot) :
	await bot.add_cog(await loadInformation(MyCog(bot)))
