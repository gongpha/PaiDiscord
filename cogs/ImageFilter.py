import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import embed_em
from utils.procimg import resize_img_b
from utils.discord_image import getLastImage, getLastImageOrAnimatedImage, processing_image_to_file
from PIL import Image as PILImage
from PIL import ImageFilter as PILImageFilter
from PIL import ImageDraw as PILImageDraw
from io import BytesIO
from wand.image import Image as WandImage

class ImageFilter(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@staticmethod
	def _blur(image, f) :
		frames = []
		try :
			while 1 :
				img = image.convert('RGBA').filter(f)

				frames.append(img)
				image.seek(image.tell() + 1)

		except EOFError :
			pass

		b = BytesIO()
		if len(frames) > 1 :
			frames[0].save(b, format='gif', save_all=True, append_images=frames[1:], loop=0, optimize=True)
			fmt = 'gif'
		else :
			frames[0].save(b, format='png')
			fmt = 'png'
		b.seek(0)

		return b, fmt

	@staticmethod
	def _2polar(im) :
		imn = numpy.asarray(im.convert('RGBA'))
		polarImage, ptSettings = polarTransform.convertToPolarImage(imn, hasColor=True)

		imm = Image.fromarray(polarImage.T.astype('uint8'), 'RGBA')

		return (imm, ptSettings)

	@staticmethod
	def _2cartesian(im, meta) :
		imn = numpy.asarray(im.convert('RGBA'))
		carim = meta.convertToCartesianImage(imn)

		imm = Image.fromarray(carim.astype('uint8'), 'RGBA')

		return imm

	@staticmethod
	def _circular_blur(im, size) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as img :
					img.rotational_blur(angle=size)
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
	def _motion_blur(im, radius, sigma, angle) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as img :
					img.motion_blur(radius=radius, sigma=sigma, angle=angle)
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

	# single image
	@staticmethod
	def _anaglyph(im) :
		frames = []
		i = 0
		try :
			while 1 :
				bytes = BytesIO()
				im.convert('RGBA').save(bytes, format='PNG')
				bytes.seek(0)
				with WandImage(blob=bytes) as simg :
					with Image.stereogram(left=simg,right=simg) as img :
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
	def _image_ellipse(im) :
		frames = []
		mask = PILImage.new("L", im.size, 0)
		d = PILImageDraw.Draw(mask)
		d.ellipse((0,0,im.width,im.height), fill=255)
		i = 0
		try :
			while 1 :
				img = im.convert('RGBA')
				#img.putalpha(mask)
				img.putalpha(mask)
				#img.save("w{}.png".format(i))
				frames.append(img)
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

	@commands.command()
	async def resize(self, ctx, width : str, height : typing.Optional[str] = "asWidth", resample : typing.Optional[str] = "bilinear") :
		im = await getLastImageOrAnimatedImage(ctx)
		try :
			if width.endswith("%") :
				w = int((int(width.replace('%', '')) / 100) * im.width)
			else :
				w = width

			if height == "asWidth" :
				if width.endswith("%") :
					h = int((int(width.replace('%', '')) / 100) * im.height)
				else :
					h = w
			else :
				if height.endswith("%") :
					h = int((int(height.replace('%', '')) / 100) * im.height)
				else :
					h = height
			if int(w) <= 0 :
				w = 1
			if int(h) <= 0 :
				h = 1
		except ValueError:
			e = embed_em(ctx, self.ss('Resize__CannotResizeThisImage'), self.bot.ss('InvalidNumber'))
			await ctx.send(embed=e)
			return
		try :
			file = await processing_image_to_file(ctx, "resize", resize_img_b, im, w, h, resample)
		except Image__Failed :
			e = embed_em(ctx, self.ss('Resize__CannotResizeThisImage'), self.ss('Resize__TryReduceSize'))
			await ctx.send(embed=e)
			return
		await ctx.send("`{} x {}` => `{} x {}`".format(int(im.width), int(im.height), int(w), int(h)), file=file)

	@commands.command()
	async def blur(self, ctx, scale : typing.Optional[int] = 16) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "blur", self._blur, im, PILImageFilter.GaussianBlur(scale))
		await ctx.send(file=file)

	@commands.command()
	async def ellipse(self, ctx) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "ellipse", self._image_ellipse, im)
		await ctx.send(file=file)

	@commands.command()
	async def motion_blur(self, ctx, angle : typing.Optional[int] = 45, radius : typing.Optional[int] = 64) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "motion", self._motion_blur, im, radius, radius / 2, angle)
		await ctx.send(file=file)

	@commands.command()
	async def motion_blur_ext(self, ctx, angle : typing.Optional[int] = 45, radius : typing.Optional[int] = 64, sigma : typing.Optional[int] = 32) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "motion", self._motion_blur, im, radius, sigma, angle)
		await ctx.send(file=file)

	@commands.command()
	async def circular_blur(self, ctx, angle : typing.Optional[int] = 16) :
		im = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "circular", self._circular_blur, im, angle)
		await ctx.send(file=file)
async def setup(bot) :
	await bot.add_cog(await loadInformation(ImageFilter(bot)))
