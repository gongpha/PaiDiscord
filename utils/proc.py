import discord
from discord.ext import commands
import json
import yaml
import aiohttp

class Proc(commands.Cog) :
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)
		with open('i18n/cogs/{}/{}.yml'.format(self.__class__.__name__, bot.lang), encoding="utf8") as json_file:
			self.stringstack = yaml.safe_load(json_file)
		self.cog_name = self.stringstack["cog"]["name"]
		self.cog_desc = self.stringstack["cog"]["description"]
		self.cog_emoji = self.stringstack["cog"]["icon_emoji"]
		self.cog_hidden = False

		super().__init__()
