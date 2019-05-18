import discord
from discord.ext.commands import *

class AnyUser :
	async def convert(ctx, obj) :
		passed = 0
		result = None
		if not obj :
			return None
		try :
			result = await MemberConverter().convert(ctx, obj)
		except BadArgument :
			passed += 1
			try :
				result = await UserConverter().convert(ctx, obj)
			except BadArgument :
				passed += 1
				result = ctx.bot.get_user(obj)
				if result == None :
					passed += 1
					try :
						result = await ctx.bot.fetch_user(obj)
					except discord.NotFound :
						return None;
		return (result, passed)
