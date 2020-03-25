from PIL import Image
from PIL import ImageDraw
from io import BytesIO
from utils.procimg import resize_img_b
import discord

standalone_image_ext = ("png", "jpeg", "jpg", "webp", "tiff")
animated_image_ext = ("gif", )

# 1 = Static
# 2 = Animated
def format_type(format) :
	for extname in standalone_image_ext :
		if format.lower() == extname :
			return 1
	for extname in animated_image_ext :
		if format.lower() == extname :
			return 2
	return None

async def im_avatar(ctx, u) :
	uu = u or ctx.author
	url = uu.avatar_url_as(format="png")
	r = await ctx.bot.session.get(str(url))
	if r.status != 200:
		return None
	return Image.open(BytesIO(await r.read()))

async def loadImageFromURL(ctx, url) :
	try :
		return Image.open(BytesIO(await (await ctx.bot.session.get(str(url))).read()))
	except OSError :
		return None

def compress_img(filename, re, fmt) :
	cmp = 75
	while len(re.getvalue()) >= 8388608 :
		i = Image.open(re)
		if format_type(fmt) == 1 :
			i.save(re, format="jpeg", quality=1 if cmp < 1 else cmp)
		else :
			re, fmtt = resize_img_b(i, int(i.width * (cmp / 100)) if cmp > 1 else 1, int(i.height * (cmp / 100)) if cmp > 1 else 1, 'bilinear')

		re.seek(0)
		cmp -= 25

	if len(re.getvalue()) >= 8388608 :
		filename += '.overEightMb{}.{}'.format(str(cmp), 'jpeg' if format_type(fmt) == 1 else fmtt)
	else :
		filename += '.' + fmt
	return discord.File(re, filename=filename)

async def processing_image_to_file(ctx=None, filename="unknown_image_name", function=None, *parameter) :
	if not ctx :
		return
	async with ctx.channel.typing() :
		re, fmt = await ctx.bot.loop.run_in_executor(None, function, *parameter)
		print('Done : ', filename)
		return await ctx.bot.loop.run_in_executor(None, compress_img, filename, re, fmt)

async def _getlastimg_c(ctx, format, count = 1, urlmode = 0) :
	images = []
	async def add(obj) :
		url = obj
		obj = await loadImageFromURL(ctx, obj)
		if obj :
			for extname in format :
				if obj.format.lower() == extname :
					if urlmode :
						images.append(url)
						break
					else :
						images.append(obj)
						break
		else :
			return

		if len(images) == count :
			if count < 2 :
				return obj
			else :
				return images
		else :
			return None

	# check attachments
	async def lm(msg) :
		if msg.attachments :
			for a in reversed(msg.attachments) :
				r = await add(a.url)
				if r :
					return r

		elif msg.embeds :
			for e in reversed(msg.embeds) :
				#print(e.url)
				if e.url != discord.Embed.Empty :
					r = await add(e.url)
					if r :
						return r
				if e.image.url != discord.Embed.Empty :
					r = await add(e.image.url)
					if r :
						return r
		else :
			return False;


	#######################################
	rr = await lm(ctx.message)
	if not rr :
		rm = None
		async for msg in ctx.channel.history(limit=500) :
			rm = await lm(msg)
			if rm :
				break

		if not rm :
			r = await add(ctx.author.avatar_url)
			if r :
				return r
			else :
				return None
		else :
			return rm
	else :
		return rr










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

async def getLastAnimatedImage(ctx, count = 1, urlmode = 0) :
	return (await _getlastimg_c(ctx, animated_image_ext, count, urlmode))
async def getLastImage(ctx, count = 1, urlmode = 0) :
	return (await _getlastimg_c(ctx, standalone_image_ext, count, urlmode))
async def getLastImageOrAnimatedImage(ctx, count = 1, urlmode = 0) :
	return (await _getlastimg_c(ctx, standalone_image_ext + animated_image_ext, count, urlmode))
