import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar
from utils.anymodel import AnyModel_FindUserOrMember
from utils.discord_image import getLastImage
#from utils.procimg import ProcImg

name = "Triggered"

class Triggered(Proc) :
	desc = {
		"th" : {
			"triggered" : "มีม Triggered",
			"triggered_l" : "มีม Triggered\nจับภาพล่าสุดในช่อง"
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

	def m_triggered(self, image) :
		img = image.convert('RGBA')
		triggered = Image.open("template/proc/triggered-hd.png")
		tint = Image.open('template/proc/redoverlay.png').convert('RGBA').resize(img.size, Image.NEAREST)
		mmmw = int(16 * ((img.width) / 1000))
		mmmh = int(16 * ((img.height) / 1000))
		triggered = triggered.resize((img.width - (mmmw*2), int(img.height * (20/100))), Image.LANCZOS)
		blank = Image.new('RGBA', (img.width - (mmmw*4), img.height - (mmmh*4)), color=(231, 19, 29))
		frames = []

		for i in range(8) :
			base = blank.copy()

			if i == 0 :
				base.paste(img, (-(mmmw*2), -(mmmh*2)), img)
			else :
				base.paste(img, (-(mmmw*2) + randint(-(mmmw), (mmmw)), -(mmmh*2) + randint(-(mmmh), (mmmh))), img)

			if i == 0:
				base.paste(triggered, (-(mmmw), base.height - triggered.height))
			else:
				base.paste(triggered, (-(mmmw) + randint(-(mmmw), (mmmw)), (base.height - triggered.height) + mmmh + randint(-int(mmmh), int(mmmh))))

			base.paste(tint, (0, 0), tint)
			frames.append(base)

		b = BytesIO()
		frames[0].save(b, format='gif', save_all=True, append_images=frames[1:], loop=0, duration=20, optimize=True)
		b.seek(0)
		return frames


	@commands.command()
	async def triggered(self, ctx, u = None) :
		async with ctx.channel.typing() :
			img = await im_avatar(ctx, await AnyModel_FindUserOrMember(ctx, u or ctx.author))
			frames = await ctx.bot.loop.run_in_executor(None, self.m_triggered, img)
			b = BytesIO()

			file = discord.File(b, filename="triggered.gif")
			await ctx.send(file=file)

	@commands.command()
	async def triggered_l(self, ctx) :
		async with ctx.channel.typing() :
			img = await getLastImage(ctx)
			frames = await ctx.bot.loop.run_in_executor(None, self.m_triggered, img)
			b = BytesIO()
			frames[0].save(b, format='gif', save_all=True, append_images=frames[1:], loop=0, duration=20, optimize=True)
			file = discord.File(b, filename="triggered.gif")
			await ctx.send(file=file)

def setup(bot) :
	bot.add_cog(loadInformation(Triggered(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
