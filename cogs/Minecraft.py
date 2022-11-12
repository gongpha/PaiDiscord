import discord
from discord.ext import commands
from utils.cog import Cog, loadInformation
from utils.template import embed_em, embed_t
import re

class UUIDNotFound(Exception) :
	"""UUID was not found"""
	pass

class UsernameNotFound(Exception) :
	"""Username was not found"""
	pass

class Minecraft(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	async def get_us_or_uu(self, input) :
		_isuuid1 = re.match("[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[34][0-9a-fA-F]{3}-[89ab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}", input)
		_isuuid2 = re.match("[0-9a-fA-F]{8}[0-9a-fA-F]{4}[34][0-9a-fA-F]{3}[89ab][0-9a-fA-F]{3}[0-9a-fA-F]{12}", input)
		isuuid = _isuuid1 != None or _isuuid2 != None
		if isuuid :
			uuid = input.replace('-','')
			r = await self.bot.session.get('https://api.mojang.com/user/profiles/{}/names'.format(uuid))
			if r.status != 200 :
				raise UUIDNotFound
			j = await r.json()
			username = j[-1]["name"]
		else :
			username = input
			r = await self.bot.session.get('https://api.mojang.com/users/profiles/minecraft/{}'.format(username))
			if r.status != 200 :
				raise UsernameNotFound
			j = await r.json()
			uuid = j["id"]
		return uuid, username

	@commands.command()
	async def mcskin(self, ctx, input, hat=True) :
		try :
			uuid, username = await self.get_us_or_uu(input)
		except UUIDNotFound :
			await ctx.send(embed=embed_em(ctx, self.ss('UUIDNotfound')))
			return
		except UsernameNotFound :
			await ctx.send(embed=embed_em(ctx, self.ss('UsernameNotfound')))
			return


		avatar_url = 'https://crafatar.com/avatars/{}{}'.format(uuid, '?overlay' if hat else '')
		body_url = 'https://crafatar.com/renders/body/{}{}'.format(uuid, '?overlay' if hat else '')
		# r = await b.session.get(avatar_url)
		# if r.status != 201 :
		# 	await ctx.send(embed=embed_em(ctx, self.ss('UUIDNotfound')))
		# 	return
		#
		# r = await b.session.get(body_url)
		# if r.status != 201 :
		# 	await ctx.send(embed=embed_em(ctx, self.ss('UUIDNotfound')))
		# 	return

		e = embed_t(ctx)
		e.set_author(name=username, icon_url=avatar_url)
		e.set_image(url=body_url)
		e.set_footer(text=uuid)
		if not hat :
			e.add_field(name=ctx.bot.ss('Configs'), value='- ' + self.ss('NoHat'))
		await ctx.send(embed=e)

	@commands.command()
	async def mcskin_raw(self, ctx, input, hat=True) :
		try :
			uuid, username = await self.get_us_or_uu(input)
		except UUIDNotFound :
			await ctx.send(embed=embed_em(ctx, self.ss('UUIDNotfound')))
			return
		except UsernameNotFound :
			await ctx.send(embed=embed_em(ctx, self.ss('UsernameNotfound')))
			return


		avatar_url = 'https://crafatar.com/avatars/{}{}'.format(uuid, '?overlay' if hat else '')
		skin_url = 'https://crafatar.com/skins/{}'.format(uuid)
		# r = await b.session.get(avatar_url)
		# if r.status != 201 :
		# 	await ctx.send(embed=embed_em(ctx, self.ss('UUIDNotfound')))
		# 	return
		#
		# r = await b.session.get(body_url)
		# if r.status != 201 :
		# 	await ctx.send(embed=embed_em(ctx, self.ss('UUIDNotfound')))
		# 	return

		e = embed_t(ctx)
		e.set_author(name=username, icon_url=avatar_url)
		e.set_image(url=skin_url)
		e.set_footer(text=uuid)
		if not hat :
			e.add_field(name=ctx.bot.ss('Configs'), value='- ' + self.ss('NoHat'))
		await ctx.send(embed=e)
async def setup(bot) :
	await bot.add_cog(await loadInformation(Minecraft(bot)))
