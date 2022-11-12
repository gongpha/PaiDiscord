import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar, processing_image_to_file, getLastImage
from utils.anymodel import AnyModel_FindUserOrMember
from utils.discord_image import getLastImageOrAnimatedImage
#from utils.procimg import ProcImg

name = "GarenaAppCover"

class GarenaAppCover(Proc) :
	desc = {
		"th" : {
			"garena_app" : "Cover แอปโดย Garena",
		}
	}
	author = "gongpha"
	usag = {
		"th" : {

		}
	}

	cover = Image.open("template/meme/garena_app_cover.png")

	def __init__(self, bot) :
		super().__init__(bot)

	def m_garena_app(self, image) :
		frames = []
		try :
			while 1 :
				img = image.convert('RGBA')

				mmm = img.width / (512)
				_cover = self.cover.resize((int(self.cover.width * (mmm)), int(self.cover.height * (mmm))), Image.LANCZOS)

				img.paste(_cover, (img.width - _cover.width,img.height - _cover.height), _cover)
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


	@commands.command()
	async def garena_app(self, ctx, user = None) :
		if user != None :
			av = await im_avatar(ctx, await AnyModel_FindUserOrMember(ctx, user))
		else :
			av = None
		img = await getLastImage(ctx)
		file = await processing_image_to_file(ctx, "garena", self.m_garena_app, img)
		await ctx.send(file=file)

async def setup(bot) :
	await bot.add_cog(await loadInformation(GarenaAppCover(bot)))
