import discord
from discord.ext.commands import *
import codecs
from utils.template import embed_em
from io import BytesIO

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
					try :
						codes = ["{c:x}".format(c=ord(c)) for c in obj]
						if "200d" not in codes :
							code = "-".join([c for c in codes if c != "fe0f"])
						else :
							code = "-".join(codes)
						url = "https://twemoji.maxcdn.com/v/13.0.1/72x72/{}.png".format(code)
						response = await ctx.bot.session.get(url)
						if response.status != 200 :
							raise Exception()
						b = BytesIO(await response.read())
						return ((b,url), 0)
					except :
						return (None, -1)
	b = BytesIO(await result.read())
	return ((b, result), passed)

async def anyemoji_check(ctx, object) :
	r, passed = await anyemoji_convert(ctx,object)
	if passed < 0 :
		err = embed_em(ctx, ctx.bot.stringstack["ObjectNotFoundFromObject"].format(ctx.bot.stringstack["Model"]["Emoji"], str(object)))
		#err.description = "```{}```".format(result.text)
		err.set_footer(text="{} : {} : {}".format(r.status, r.code, passed))
		await ctx.send(embed=err)
		return None
	return r
