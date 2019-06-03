from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import discord

standalone_image_ext = ("png", "jpeg", "jpg", "webp", "tiff")

async def im_avatar(ctx, u) :
	uu = u or ctx.author
	url = uu.avatar_url_as(format="png")
	#print(url)
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

async def getLastImage(ctx) :
	if ctx.message.attachments :
		for a in reversed(ctx.message.attachments) :
			for extname in standalone_image_ext :
				if (a.filename.lower().endswith("." + extname)) :
					return Image.open(BytesIO(await (await ctx.bot.session.get(str(a.url))).read()))
	else :
		if ctx.message.embeds :
			for e in reversed(ctx.message.embeds) :
				if e.url != discord.Embed.Empty :
					return Image.open(BytesIO(await (await ctx.bot.session.get(str(e.url))).read()))
				if e.image != discord.Embed.Empty :
					return Image.open(BytesIO(await (await ctx.bot.session.get(str(e.image.url))).read()))
		else :
			messages = await ctx.channel.history(limit=100).flatten()

			for msg in messages :
				if msg.attachments :
					for a in reversed(msg.attachments) :
						for extname in standalone_image_ext :
							if (a.filename.lower().endswith("." + extname)) :
								return Image.open(BytesIO(await (await ctx.bot.session.get(str(a.url))).read()))
				else :
					if msg.embeds :
						for e in reversed(msg.embeds) :
							if e.url != discord.Embed.Empty :
								return Image.open(BytesIO(await (await ctx.bot.session.get(str(e.url))).read()))
							if e.image != discord.Embed.Empty :
								if e.image.url != discord.Embed.Empty :
									return Image.open(BytesIO(await (await ctx.bot.session.get(str(e.image.url))).read()))
	return Image.open(BytesIO(await (await ctx.bot.session.get(str(ctx.author.avatar_url))).read()))
