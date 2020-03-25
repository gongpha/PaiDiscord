import discord
from discord.ext import commands
import typing
from utils.cog import Cog
import aiohttp
from utils.cog import loadInformation
from utils.template import embed_t
from importlib import import_module

proc_list = [
	"proc.Triggered",
	"proc._กูรู้หมดแล้ว",
	"proc.Fortune",
	"proc._ป้าถือไม้กวาด",
	"proc.RTX"
]

stack = []

class ImageGenerate(Cog) :
	def __init__(self, bot) :
		for c in proc_list :
			#try:
			lib = import_module(c)
			# except ImportError as e:
			# 	raise errors.ExtensionNotFound(c, e) from e
			#else :
			bot._load_from_module_spec(lib, c)
			stack.append(lib.name)


				#traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		super().__init__(bot)

	@commands.command()
	async def imggen_list(self, ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
		if end is None:
			end = start + 20
		stri = "```\n"
		stri += "\n".join(stack)
		stri += '```'
		e = embed_t(ctx, "", ctx.bot.ss("TypeToGetMoreInfoOfEachCmd").format(str(ctx.bot.cmdprefix) + "help <{}>".format(ctx.bot.ss("Model", "Name"))), casesensitive=True)
		e.add_field(name=f"{start} - {end}", value=stri)
		await ctx.send(embed=e)
def setup(bot) :
	bot.add_cog(loadInformation(ImageGenerate(bot)))
