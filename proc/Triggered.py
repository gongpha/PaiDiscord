import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar
from utils.anyuser import anyuser_safecheck
#from utils.procimg import ProcImg

name = "&triggered"

class Triggered(Proc) :
	desc = {
		"th" : {
			"triggered" : "มีม Triggered"
		}
	}
	author = "gongpha"
	usag = {
		"th" : {
			"triggered" : "<ผู้ใช้ = ตัวเอง>"
		}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def triggered(self, ctx, u = None) :
		im = await im_avatar(ctx, await anyuser_safecheck(ctx, u))
		img = im.convert('RGBA')
		thmm = int((img.width * img.height) / 750000)
		triggered = Image.open("template/proc/triggered-hd.png")
		thm = int((img.height / triggered.height) * 10)
		triggered = triggered.resize((img.width - 40, triggered.height - thm), Image.LANCZOS)
		tint = Image.open('template/proc/redoverlay.png').convert('RGBA').resize(img.size, Image.NEAREST)
		blank = Image.new('RGBA', (img.width - 64, img.height - 64), color=(231, 19, 29))
		frames = []

		for i in range(8):
			base = blank.copy()
			if i == 0:
				base.paste(img, (-16 * thmm, -16 * thmm), img)
			else:
				base.paste(img, (-32 + randint(-16 * thmm, 16 * thmm), -32 + randint(-16 * thmm, 16 * thmm)), img)


			if i == 0:
				base.paste(triggered, (-10 * thmm, img.height - triggered.height - thm))
			else:
				base.paste(triggered, (-12 + randint(-4 * thmm, 4 * thmm), (img.height - triggered.height) + randint(0, 12 * thmm) - thm))

			base.paste(tint, (0, 0), tint)
			frames.append(base)

		frames[0].save('cache/triggered.gif', append_images=frames[1:], save_all=True, loop=0, duration=50)
		file = discord.File("cache/triggered.gif", filename="triggered.gif")
		await ctx.send(file=file)

def setup(bot) :
	bot.add_cog(loadInformation(Triggered(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
