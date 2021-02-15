import discord
from io import BytesIO
from random import randint
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar, processing_image_to_file
from utils.anymodel import AnyModel_FindUserOrMember
from utils.discord_image import getLastImageOrAnimatedImage
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
		while image.width > 2048 or image.height > 2048 :
			width = image.width // 2
			height = image.height // 2
			image = image.resize((width, height))

		type = None # 1 = Static ; 2 = Animated
		try :
			image.seek(image.tell() + 1)
			type = 2
			image.seek(0)

		except EOFError :
			type = 1

		triggered = Image.open("template/proc/triggered-hd.png")
		tint = Image.open('template/proc/redoverlay.png').convert('RGBA').resize(image.size, Image.NEAREST)
		mmmw = int(16 * ((image.width) / 1000))
		mmmh = int(16 * ((image.height) / 1000))
		triggered = triggered.resize((image.width - (mmmw*2), int(image.height * (20/100))), Image.LANCZOS)
		blank = Image.new('RGBA', (image.width - (mmmw*4), image.height - (mmmh*4)), color=(231, 19, 29))
		frames = []

		if type == 1 :
			img = image.convert('RGBA')
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
				d = 20
				frames.append(base)
		else :
			try :
				i = 0
				d = []
				while 1 :
					d = image.info['duration']
					img = image.convert('RGBA')
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
					i += 1
					image.seek(image.tell() + 1)

			except EOFError :
				pass

		b = BytesIO()
		frames[0].save(b, format='gif', save_all=True, append_images=frames[1:], loop=0, optimize=True, duration=d)
		b.seek(0)
		return b, "gif"


	@commands.command()
	async def triggered(self, ctx, u = None) :
		img = await im_avatar(ctx, await AnyModel_FindUserOrMember(ctx, u or ctx.author))
		file = await processing_image_to_file(ctx, "triggered", self.m_triggered, img)
		await ctx.send(file=file)

	@commands.command()
	async def triggered_l(self, ctx) :
		img = await getLastImageOrAnimatedImage(ctx)
		file = await processing_image_to_file(ctx, "triggered", self.m_triggered, img)
		await ctx.send(file=file)

def setup(bot) :
	bot.add_cog(loadInformation(Triggered(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
