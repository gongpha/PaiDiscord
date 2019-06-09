import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import embed_t, embed_em, embed_wm
from urllib.parse import quote_plus
from pythainlp.tokenize import word_tokenize as wt
from pythainlp.transliterate import romanize as rmz
from pythainlp.spell import *

class Thai(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def longdo(self, ctx, *, search : str) :
		e = embed_t(ctx, "Longdo : *{}*".format(search))
		e.description = "[{}]({})".format(self.bot.stringstack["OpenLink"], 'https://dict.longdo.com/mobile.php?search={}'.format(quote_plus(search)))
		await ctx.send(embed=e)

	@commands.command()
	async def word_tokenize(self, ctx, *, text : str) :
		l = list(filter(lambda a: a != " ", wt(text)))
		await ctx.send("```" + ", ".join(l) + "```\n{}".format(self.stringstack["Thai__WordCount"].format(len(l))))

	@commands.command()
	async def word_tokenize_ext(self, ctx, engine, *, text : str) :
		l = list(filter(lambda a: a != " ", wt(text,engine=engine)))
		await ctx.send("```" + ", ".join(l) + "```\n{}".format(self.stringstack["Thai__WordCount"].format(len(l))))

	@commands.command()
	async def romanization(self, ctx, *, text : str) :
		await ctx.send("```\n" + rmz(text) + "```")

	@commands.command()
	async def spell_check(self, ctx, *, text : str) :
		l = list(filter(lambda a: a != " ", spell(text)))
		await ctx.send("```\n" + "\n".join(l) + "```\n{}".format(self.stringstack["Thai__WordCount"].format(len(l))))

	@commands.command()
	async def spell_correct(self, ctx, *, text : str) :
		await ctx.send("```\n" + correct(text) + "```")

def setup(bot) :
	bot.add_cog(loadInformation(Thai(bot)))
