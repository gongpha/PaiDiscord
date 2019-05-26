import discord
from discord.ext import commands
import json
import yaml
import aiohttp

class Cog(commands.Cog) :
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)
		with open('i18n/cogs/{}/{}.yml'.format(self.__class__.__name__, bot.lang), encoding="utf8") as json_file:
			self.stringstack = yaml.safe_load(json_file)
		self.cog_name = self.stringstack["cog"]["name"]
		self.cog_desc = self.stringstack["cog"]["description"]
		self.cog_emoji = [self.stringstack["cog"]["icon_emoji"]] if not isinstance(self.stringstack["cog"]["icon_emoji"],(list, tuple)) else [item for sublist in self.stringstack["cog"]["icon_emoji"] for item in sublist]
		# [item for sublist in self.stringstack["cog"]["icon_emoji"] for item in sublist]
		self.cog_hidden = False

		super().__init__()

    # @classmethod
    # def setup(c, bot) :
    # 	cg = c(bot)
    # 	for c in cg.get_commands():
    # 		c.description = cg.stringstack["command_{}_desc".format(c.name)]
    #
    # 	bot.add_cog(cg)
def loadInformation(cog) :
	for c in cog.get_commands() :
		c.description = cog.stringstack["command"][c.name]["description"]
		c.usage = cog.stringstack["command"][c.name]["usage"]
		if cog.stringstack["command"][c.name]["aliases"] :
			c.aliases = cog.stringstack["command"][c.name]["aliases"]
		try :
			c.sql = cog.stringstack["command"][c.name]["sql"]
		except KeyError :
			c.sql = False
	return cog
