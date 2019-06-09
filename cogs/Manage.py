import discord
from discord.ext import commands
import typing
from utils.cog import Cog
import aiohttp
from utils.cog import loadInformation
from utils.template import *

class Manage(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def language(self, ctx) :

def setup(bot) :
	bot.add_cog(loadInformation(Info(bot)))
