import discord
from discord.ext.commands import *

async def anyemoji_convert(ctx, obj) :
	passed = 1
	result = None
	if not obj :
		return (None, 0)
	try :
		result = await EmojiConverter().convert(ctx, obj)
	except BadArgument :
		passed += 1
		result = ctx.bot.get_emoji(obj)
		if result == None :
			passed += 1
			try :
				result = await ctx.bot.fetch_emoji(obj)
			except :
				passed += 1
				try :
					result = await PartialEmojiConverter().convert(ctx, obj)
				except BadArgument :
					return (None, -1)
	return (result, passed)

async def anyemoji_check(ctx, object) :
	r, passed = await anyemoji_convert(ctx,object)
	if passed < 0 :
		err = embed_em(ctx, ctx.bot.stringstack["ObjectNotFoundFromObject"].format(ctx.bot.stringstack["Model"]["Emoji"], str(object)))
		#err.description = "```{}```".format(result.text)
		err.set_footer(text="{} : {} : {}".format(r.status, r.code, passed))
		await ctx.send(embed=err)
		return None
	return r
