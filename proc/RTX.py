import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar, processing_image_to_file
from utils.anymodel import AnyModel_FindUserOrMember
from utils.discord_image import getLastImage
from utils.procimg import join_vert_image
from utils.template import embed_em

name = "RTX"

class RTX(Proc) :
	desc = {
		"th" : {
			"rtx" : "มีม RTX Off / On\nจับภาพล่าสุด 2 ภาพ",
		}
	}
	author = "gongpha"
	usag = {
		"th" : {}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	def m_rtx(self, im_off, im_on) :
		img, center = join_vert_image(im_off, im_on, 2, True)
		margin = 20
		off = Image.open("template/meme/rtx-off.png")
		mmm = img.width / (2804*2)
		off = off.resize((int(off.width * (mmm)), int(off.height * (mmm))), Image.LANCZOS)
		on = Image.open("template/meme/rtx-on.png")
		on = on.resize((int(on.width * (mmm)), int(on.height * (mmm))), Image.LANCZOS)
		img.paste(off, (0, margin),off)
		img.paste(on, (0, margin + center),on)
		b = BytesIO()
		img.save(b, format="png")
		b.seek(0)
		return b, "png"


	@commands.command()
	async def rtx(self, ctx) :
		img = await getLastImage(ctx, 2)
		if len(img or []) < 2 :
			e = embed_em(ctx, ctx.bot.ss('AnErrorOccurred'), ctx.bot.ss('ImageNotEnoughNeedNum').format(str(2)))
			await ctx.send(embed=e)
			return
		file = await processing_image_to_file(ctx, "rtx", self.m_rtx, img[1], img[0])
		await ctx.send(file=file)

async def setup(bot) :
	await bot.add_cog(await loadInformation(RTX(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
