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
			width = int((int(width.replace('%', '')) / 100) * im.width)

		if height == "asWidth" :
			height = width
		else :
			if height.endswith("%") :
				height = int((int(height.replace('%', '')) / 100) * im.height)

		resamp = {
			"nearest" : PILImage.NEAREST,
			"bilinear" : PILImage.BILINEAR,
			"bicubic" : PILImage.BICUBIC,
			"lanczos" : PILImage.LANCZOS
		}

		im.resize((int(width), int(height)), resamp.get(resample, lambda: Image.BILINEAR)).save('cache/resize.png')
		file = discord.File("cache/resize.png", filename="resize.png")
		await ctx.send("`{} x {}`".format(int(width), int(height)), file=file)
def setup(bot) :
	bot.add_cog(loadInformation(Image(bot)))
