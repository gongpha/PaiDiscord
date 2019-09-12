import discord
from discord.ext import commands
import json
import yaml
import aiohttp

class Proc(commands.Cog) :
	def __init__(self, bot):
		self.bot = bot
		#self.session = aiohttp.ClientSession(loop=bot.loop)
		# [item for sublist in self.stringstack["cog"]["icon_emoji"] for item in sublist]
		self.cog_hidden = True
		super().__init__()
		self.cog_name = self.qualified_name
		self.cog_desc = self.description
		self.cog_emoji = [":gear:"]



    # @classmethod
    # def setup(c, bot) :
    # 	cg = c(bot)
    # 	for c in cg.get_commands():
    # 		c.description = cg.stringstack["command_{}_desc".format(c.name)]
    #
    # 	bot.add_cog(cg)
def loadInformation(cog) :
	for c in cog.get_commands() :
		c.description = cog.desc.get(cog.bot.languages[0], {}).get(c.name, cog.bot.ss("Empty"))
		c.usage = cog.usag.get(cog.bot.languages[0], {}).get(c.name, cog.bot.ss("Empty"))
		c.sql = False
	return cog

#def cfgParse(cfg) :
