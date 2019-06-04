import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
from utils.request import *
import json
import random

class Request(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

		self.stack = {
			"randomcat" : r_RandomCat,
			"imgur" : r_Imgur
		}


	@commands.command()
	async def request(self, ctx, *req) :
		#print(self.bot.name)
		#print(self.bot.description)
		req = list(req)
		name = req[0]
		req.pop(0)
		try :
			s = self.stack[name]

		except KeyError :
			err = embed_em(ctx, self.bot.stringstack["ObjectNotFoundFromObject"].format(self.bot.stringstack["Model"]["Source"], req))
			err.description = self.bot.stringstack["TypeCommandForShowAllOject"].format("{}request_list".format(self.bot.command_prefix), self.bot.stringstack["Model"]["Source"])
			await ctx.send(embed=err)
			return


			#rr = await s.get(s[0])
		u = await s(ctx.bot, req)
		e = embed_t(ctx, name, "[{}]({})".format(self.bot.stringstack["OpenOriginal"], u[1]))
		if u :
			e.set_image(url=u[0])
			await ctx.send(embed=e)
		else :
			await ctx.send(embed=embed_wm(ctx, self.bot.stringstack["NoResult"],""))

	@commands.command()
	async def request_list(self, ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
		if end is None:
			end = start + 20
		stri = "```\n"
		stri += "\n".join([n for n, v in self.stack.items()])
		stri += '```'
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		await ctx.send(embed=e)

	@commands.command()
	async def image_search(self, ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
	r = requests.get("https://api.qwant.com/api/search/images",
    params={
        'count': 50,
        'q': query,
        't': 'images',
        'safesearch': 1,
        'locale': 'en_US',
        'uiv': 4
    },
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
)
def setup(bot) :
	bot.add_cog(loadInformation(Request(bot)))
