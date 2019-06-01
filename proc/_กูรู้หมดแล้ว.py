import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar
from utils.anyuser import anyuser_safecheck
from utils.discord_image import getLastImage
from utils.text import textimage
#from utils.procimg import ProcImg

name = "_กูรู้หมดแล้ว"

class _กูรู้หมดแล้ว(Proc) :
	desc = {
		"th" : {
			"กูรู้หมดแล้ว" : "มีม กูรู้หมดแล้ว ของกำนันโชติ",
		}
	}
	author = "gongpha"
	usag = {
		"th" : {
			"กูรู้หมดแล้ว" : "<ข้อความ>"
		}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	def m_ikwi(self, text) :
		# by gongpha
		bg = Image.open("template/meme/กูรู้หมดแล้ว.png")

		img_text = textimage(text, "font/sukhumvitb.ttf", 50, (160, 28, 51), None, None, 0)

		# draw = ImageDraw.Draw(bg)
		# draw.text((41, 158), text, (140, 28, 51), font=font)
		r = img_text.rotate(1, expand = True)
		bg.paste(r,(41, 158),r)
		return bg


	@commands.command(name="กูรู้หมดแล้ว", aliases=["ikwi"])
	async def ikwi(self, ctx, *, text : str) :
		async with ctx.channel.typing() :
			self.m_ikwi(text).save("cache/ikwi.png", format='png', optimize=True)
			file = discord.File("cache/ikwi.png", filename="ikwi.png")
			await ctx.send("{} : `{}`".format(ctx.bot.stringstack["Model"]["Text"], text),file=file)

def setup(bot) :
	bot.add_cog(loadInformation(_กูรู้หมดแล้ว(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
