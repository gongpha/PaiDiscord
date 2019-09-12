import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
from utils.request import *
import json
import mimetypes
from io import BytesIO
import random

class Request(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)
		self.cached_search = {}

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
			err = embed_em(ctx, self.bot.ss("ObjectNotFoundFromObject").format(self.bot.ss("Model", "Source"), req))
			err.description = self.bot.ss("TypeCommandForShowAllOject").format("{}request_list".format(self.bot.command_prefix), self.bot.ss("Model", "Source"))
			await ctx.send(embed=err)
			return


			#rr = await s.get(s[0])
		u = await s(ctx.bot, req)
		e = embed_t(ctx, name, "[{}]({})".format(self.bot.ss("OpenOriginal"), u[1]))
		if u :
			e.set_image(url=u[0])
			await ctx.send(embed=e)
		else :
			await ctx.send(embed=embed_wm(ctx, self.bot.ss("NoResult"),""))

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
	@IsOwnerBot()
	async def _request__list(self, ctx) :
		e = embed_t(ctx, len(self.cached_search))
		for key, value in self.cached_search.items() :
			e.add_field(name=key, value=len(value))

		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _request__clear(self, ctx) :
		self.cached_search = {}
		await ctx.send(':ok_hand:')

	@commands.command()
	async def image_search(self, ctx, *, q : str) :
		async with ctx.message.channel.typing() :

			if q in self.cached_search :
				urls = self.cached_search.get(q)
			else :
				r = await self.bot.session.get('https://api.qwant.com/api/search/images',
				params={
					'count': 250,
					'q': q,
					't': 'images',
					'safesearch': 0 if ctx.message.channel.is_nsfw() else 1 ,
					'locale': 'th_TH',
					'uiv': 4
				},headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
				})

				response = await r.json(content_type=None)
				if response.get('status') == 'error' :
					error_code = response.get('error')
					print('Error from QWant :', error_code)
					if error_code == 24 :
						await ctx.send(embed=embed_em(ctx, self.bot.ss('AnErrorOccurred')))
						return
				else :
					o = response.get('data').get('result').get('items')
					if not o :
						await ctx.send(embed=embed_em(ctx, self.bot.ss('ImageNotFound')))
						return
					else :
						urls = [r.get('media') for r in o]
						self.cached_search[q] = urls
			async with self.bot.session.get(random.choice(urls)) as resp :
				if resp.status == 200 :
					buffer = BytesIO(await resp.read())
					typ = mimetypes.guess_extension(resp.content_type)
					print('Exporting', typ)
					if typ == '.jpe' :
						typ = '-jpe.jpeg'
					file = discord.File(fp=buffer, filename="pai__image-search_{}-168d{}_request{}".format(ctx.author.display_name,ctx.author.id,typ))
					await ctx.send(self.ss('NSFWWarning') if ctx.message.channel.is_nsfw() else "", file=file)
def setup(bot) :
	bot.add_cog(loadInformation(Request(bot)))
