import discord
from discord.ext import commands
import json

class Cog(commands.Cog) :
    def __init__(self, bot):
        self.bot = bot
        with open('i18n/cogs/{}/{}.json'.format(self.__class__.__name__, bot.lang), encoding="utf8") as json_file:
            self.stringstack = json.load(json_file)
        self.cog_name = self.stringstack["cog_name"]
        self.cog_desc = self.stringstack["cog_desc"]
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
        c.description = cog.stringstack["command_{}_desc".format(c.name)]
        c.usage = cog.stringstack["command_{}_usge".format(c.name)]
    return cog
