import discord
from discord.ext import commands
import typing
from utils.cog import Cog
import aiohttp
from utils.cog import loadInformation
from utils.template import embed_t
from importlib import import_module
import traceback

proc_list = [
	"proc.Triggered",
	"proc.TH_Ikwi",
	"proc.Fortune",
	"proc.Broomaunt",
	"proc.RTX",
	"proc.Karaoke",
	"proc.GarenaAppCover"
]

stack = []

class ImageGenerator(Cog) :
	async def async_init(self):
		for c in proc_list :
			try:
				await self.bot.load_extension(c)
				stack.append(c[5:])
			except Exception as e:
				print(f"Failed to load the {c}")
				traceback.print_exc()
		return await super().async_init()

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
async def setup(bot) :
	await bot.add_cog(await loadInformation(ImageGenerator(bot)))
