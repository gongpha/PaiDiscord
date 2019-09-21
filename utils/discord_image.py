from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import discord

standalone_image_ext = ("png", "jpeg", "jpg", "webp", "tiff")
animated_image_ext = ("gif", )

async def im_avatar(ctx, u) :
	uu = u or ctx.author
	url = uu.avatar_url_as(format="png")
	r = await ctx.bot.session.get(str(url))
	if r.status != 200:
		return None
	return Image.open(BytesIO(await r.read()))

def avatar_image_circle(user) :
	url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user)
	im = Image.open(BytesIO(requests.get(url).content))
	mask = Image.new("L", im.size, 0)
	d = ImageDraw.Draw(mask)
	d.ellipse((0,0,im.width,im.height), fill=255)
	im.putalpha(mask)
	return im

async def loadImageFromURL(ctx, url) :
	try :
		return Image.open(BytesIO(await (await ctx.bot.session.get(str(url))).read()))
	except OSError :
		return None

async def processing_image_to_file(ctx=None, filename="processed_image.png", function=None, *parameter) :
	async with ctx.channel.typing() :
		re = await ctx.bot.loop.run_in_executor(None, function, *parameter)
		if len(re.getvalue()) >= 8388608 :
			i = Image.open(re)
			i.save(re, format="jpg")
			re.seek(0)
			filename += '.jpg'
		return discord.File(re, filename=filename)

async def _getlastimg(ctx, format) :
	if ctx.message.attachments :
		for a in reversed(ctx.message.attachments) :
			for extname in format :
				if (a.filename.lower().endswith("." + extname)) :
					ii = await loadImageFromURL(ctx, a.url)
					if ii :
						return ii
	else :
		if ctx.message.embeds :
			for e in reversed(ctx.message.embeds) :
				if e.url != discord.Embed.Empty :
					ii = await loadImageFromURL(ctx, e.url)
					if ii :
						return ii
				if e.image != discord.Embed.Empty :
					ii = await loadImageFromURL(ctx, e.image.url)
					if ii :
						return ii
		else :
			messages = await ctx.channel.history(limit=100).flatten()

			for msg in messages :
				if msg.attachments :
					for a in reversed(msg.attachments) :
						for extname in format :
							if (a.filename.lower().endswith("." + extname)) :
								ii = await loadImageFromURL(ctx, a.url)
								if ii :
									return ii
				else :
					if msg.embeds :
						for e in reversed(msg.embeds) :
							if e.url != discord.Embed.Empty :
								ii = await loadImageFromURL(ctx, e.url)
								if ii :
									return ii
							if e.image != discord.Embed.Empty :
								if e.image.url != discord.Embed.Empty :
									ii = await loadImageFromURL(ctx, e.image.url)
									if ii :
										return ii
	return await loadImageFromURL(ctx, ctx.author.avatar_url)

async def getLastAnimatedImage(ctx) :
	return (await _getlastimg(ctx, ))
async def getLastImage(ctx) :
	return (await _getlastimg(ctx, standalone_image_ext))
