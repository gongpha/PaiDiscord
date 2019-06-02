import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.discord_image import getLastImage
from PIL import Image as PILImage

class Image(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def resize(self, ctx, width : str, height : typing.Optional[str] = "asWidth", resample : typing.Optional[str] = "bilinear", url : typing.Optional[str] = None) :

		im = await getLastImage(ctx)

		if width.endswith("%") :
			w = int((int(width.replace('%', '')) / 100) * im.width)
		else :
			w = width

		if height == "asWidth" :
			h = w
		else :
			if height.endswith("%") :
				h = int((int(height.replace('%', '')) / 100) * im.height)
			else :
				h = height

		resamp = {
			"nearest" : PILImage.NEAREST,
			"bilinear" : PILImage.BILINEAR,
			"bicubic" : PILImage.BICUBIC,
			"lanczos" : PILImage.LANCZOS
		}
		if int(w) <= 0 :
			w = 1
		if int(h) <= 0 :
			h = 1
		try :
			im.resize((int(w), int(h)), resamp.get(resample, lambda: Image.BILINEAR)).save('cache/resize.png')
		except ValueError :
			im.save('cache/resize.png')
			file = discord.File("cache/resize.png", filename="resize.png")
			await ctx.send("`{} x {}`".format(int(w), int(h)), file=file)
			return
		file = discord.File("cache/resize.png", filename="resize.png")
		await ctx.send("`{} x {}`".format(int(w), int(h)), file=file)
def setup(bot) :
	bot.add_cog(loadInformation(Image(bot)))