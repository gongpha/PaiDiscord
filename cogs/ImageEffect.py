import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import embed_em
from utils.procimg import resize_img_b
from utils.discord_image import getLastImage, getLastImageOrAnimatedImage, processing_image_to_file
from PIL import Image as PILImage
from io import BytesIO
from wand.image import Image as WandImage

class ImageEffect(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	# single image
	# @staticmethod
	# def _anaglyph(im) :
	# 	frames = []
	# 	i = 0
	# 	try :
	# 		while 1 :
	# 			bytes = BytesIO()
	# 			im.convert('RGBA').save(bytes, format='PNG')
	# 			bytes.seek(0)
	# 			with WandImage(blob=bytes) as simg :
	# 				img = WandImage.stereogram(left=simg,right=simg)
	# 				img.save(filename="effect-rotational-blur.jpg")
	# 				frames.append(PILImage.open(BytesIO(img.make_blob("png"))))
	# 			i += 1
	# 			im.seek(im.tell() + 1)
	# 	except EOFError :
	# 		pass
	#
	# 	b = BytesIO()
	# 	if len(frames) > 1 :
	# 		frames[0].save(b, format='gif', save_all=True, append_images=frames[1:])
	# 		fmt = 'gif'
	# 	else :
	# 		frames[0].save(b, format='png')
	# 		fmt = 'png'
	# 	b.seek(0)
	#
	# 	return b, fmt

	@staticmethod
	def _wave(im, amplitude, wave_length) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as img :
					img.wave(amplitude=amplitude,wave_length=wave_length)
					frames.append(PILImage.open(BytesIO(img.make_blob("png"))))
				i += 1
				im.seek(im.tell() + 1)
		except EOFError :
			pass

		b = BytesIO()
		if len(frames) > 1 :
			frames[0].save(b, format='gif', save_all=True, append_images=frames[1:])
			fmt = 'gif'
		else :
			frames[0].save(b, format='png')
			fmt = 'png'
		b.seek(0)

		return b, fmt

	@staticmethod
	def _implode(im, amount) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as img :
					img.implode(amount=amount)
					frames.append(PILImage.open(BytesIO(img.make_blob("png"))))
				i += 1
				im.seek(im.tell() + 1)
		except EOFError :
			pass

		b = BytesIO()
		if len(frames) > 1 :
			frames[0].save(b, format='gif', save_all=True, append_images=frames[1:])
			fmt = 'gif'
		else :
			frames[0].save(b, format='png')
			fmt = 'png'
		b.seek(0)

		return b, fmt

	@staticmethod
	def _swirl(im, degree) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as img :
					img.swirl(degree=degree)
					frames.append(PILImage.open(BytesIO(img.make_blob("png"))))
				i += 1
				im.seek(im.tell() + 1)
		except EOFError :
			pass

		b = BytesIO()
		if len(frames) > 1 :
			frames[0].save(b, format='gif', save_all=True, append_images=frames[1:])
			fmt = 'gif'
		else :
			frames[0].save(b, format='png')
			fmt = 'png'
		b.seek(0)

		return b, fmt

	@staticmethod
	def _fx(im, exp) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as img :
					with img.fx(exp) as filtered_img :
						frames.append(PILImage.open(BytesIO(filtered_img.make_blob("png"))))
				i += 1
				im.seek(im.tell() + 1)
		except EOFError :
			pass

		b = BytesIO()
		if len(frames) > 1 :
			frames[0].save(b, format='gif', save_all=True, append_images=frames[1:])
			fmt = 'gif'
		else :
			frames[0].save(b, format='png')
			fmt = 'png'
		b.seek(0)

		return b, fmt

	# @commands.command()
	# async def anaglyph(self, ctx) :
	# 	im = await getLastImageOrAnimatedImage(ctx)
	# 	file = await processing_image_to_file(ctx, "anaglyph", self._anaglyph, im)
	# 	await ctx.send(file=file)

	@commands.command()
	async def wave(self, ctx, amplitude : typing.Optional[int] = 256, wave_length : typing.Optional[int] = 128) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "wave", self._wave, im, amplitude, wave_length)
		await ctx.send(file=file)

	@commands.command()
	async def wave_wh(self, ctx, amplitude : typing.Optional[int] = 32, wave_length : typing.Optional[int] = 4) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "wave", self._wave, im, int(im.width / amplitude), int(im.height / wave_length))
		await ctx.send(file=file)

	@commands.command()
	async def implode(self, ctx, amount : typing.Optional[float] = 0.4) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "implode", self._implode, im, amount)
		await ctx.send(file=file)

	@commands.command()
	async def swirl(self, ctx, degree : typing.Optional[int] = 90) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "sketch", self._swirl, im, degree)
		await ctx.send(file=file)

	@commands.command()
	async def fx(self, ctx, *, exp) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "sketch", self._fx, im, exp)
		await ctx.send(file=file)
def setup(bot) :
	bot.add_cog(loadInformation(ImageEffect(bot)))
