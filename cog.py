import discord
from discord.ext import commands
import json

class Cog(commands.Cog) :
    def __init__(self, bot):
        self.bot = bot
        with open('i18n/cogs/{}/{}.json'.format(self.__class__.__name__, bot.lang), encoding="utf8") as json_file:
            self.stringstack = json.load(json_file)
        name = self.stringstack["cog_name"]
        description = self.stringstack["cog_desc"]

    @classmethod
    def setup(c, bot) :
        bot.add_cog(c(bot))
