import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar, processing_image_to_file
from utils.anyuser import anyuser_safecheck
from utils.discord_image import getLastImage
from utils.text import textimage
#from utils.procimg import ProcImg

name = "TH_Ikwi"

#ikwi : i know who is

class Ikwi(Proc) :
	desc = {
		"th" : {
			"ikwi" : "มีม กูรู้หมดแล้ว ของกำนันโชติ",
		}
	}
	author = "gongpha"
	usag = {
		"th" : {
			"ikwi" : "<ข้อความ>"
		}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	def m_ikwi(self, text) :
		# by gongpha
		bg = Image.open("template/meme/ikwi.png")

		img_text = textimage(text, "font/sukhumvitb.ttf", 50, (160, 28, 51), None, None, 0)

		# draw = ImageDraw.Draw(bg)
		# draw.text((41, 158), text, (140, 28, 51), font=font)
		r = img_text.rotate(1, expand = True)
		bg.paste(r,(41, 158),r)
		b = BytesIO()
		bg.save(b, format="png")
		b.seek(0)
		return b, "png"


	@commands.command(aliases=["กูรู้หมดแล้ว"])
	async def ikwi(self, ctx, *, text : str) :
		file = await processing_image_to_file(ctx, "ikwi", self.m_ikwi, text)
		await ctx.send(file=file)

async def setup(bot) :
	await bot.add_cog(await loadInformation(Ikwi(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
