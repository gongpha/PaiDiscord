import discord
from discord.ext import commands
import json
import yaml
import aiohttp
from utils.dict import safeget

class Cog(commands.Cog) :
	def __init__(self, bot):
		self.bot = bot
		#self.session = aiohttp.ClientSession(loop=bot.loop)
		with open('i18n/cogs/{}/{}.yml'.format(self.__class__.__name__, bot.default_language), encoding="utf8") as json_file:
			self.stringstack = yaml.safe_load(json_file)
		try :
			self.cog_name = self.stringstack["cog"]["name"]
			self.cog_desc = self.stringstack["cog"]["description"]
			self.cog_emoji = [str(self.stringstack["cog"]["icon_emoji"])] if not isinstance(self.stringstack["cog"]["icon_emoji"],(list, tuple)) else self.stringstack["cog"]["icon_emoji"] #[item for sublist in self.stringstack["cog"]["icon_emoji"] for item in sublist]
		except KeyError :
			print("Load Cog for {} failed".format(self.__class__.__name__))
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
		try :
			c.description = safeget(cog.stringstack, "command", c.name, "description")
			#c.description = cog.stringstack.get("command", {}).get(c.name, {}).get("description", STRFF)
			c.usage = safeget(cog.stringstack, "command", c.name, "usage")
			d = safeget(cog.stringstack, "command", c.name, "aliases")
			if d :
				if not isinstance(d, (list, tuple)) :
					c.aliases = [d]
				else :
					c.aliases = d
			# try :
			# 	c.sql = cog.stringstack["command"][c.name]["sql"]
			# except KeyError :
			# 	c.sql = False
		except KeyError :
			print("Load Information for {} failed".format(c.name))
	return cog
