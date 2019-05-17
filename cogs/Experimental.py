import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
class Experimental(Cog) :
	pbot = None
	def __init__(self, bot) :
		pbot = bot

		super().__init__(bot)
		self.cog_hidden = True

	@commands.command()
	@IsOwnerBot()
	async def _shutdown(self, ctx) :
		await ctx.send("👋")
		u = ctx.author
		g = ctx.message.guild
		e = discord.Embed(title="Client was shutdowned by {0} ({1}) from guild {2} ({3})".format(u, u.id, g, g.id))
		e.color = 0xDD0000
		await self.bot.log_channel.send(embed=e)
		self.bot.loop.stop()
		await self.bot.close()

def setup(bot) :
	bot.add_cog(loadInformation(Experimental(bot)))
