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
from utils.anymodel import AnyModel_FindUserOrMember
from utils.procimg import join_vert_image
from utils.text import textimage
#from utils.procimg import ProcImg

name = "Broomaunt"

class Broomaunt(Proc) :
	desc = {
		"th" : {
			"broomaunt" : "ป้าถือไม้กวาด จ้องตีใครสักคน",
		}
	}
	author = "gongpha"
	usag = {
		"th" : {
			"broomaunt" : "<ผู้ใช้แทนคนในรูป=ไม่มี>"
		}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	def m_broomaunt(self, image, loser=None) :
		# by gongpha

		victim = Image.open("template/meme/broomaunt.png")
		ps = image.width / victim.width
		if loser != None :
			loser = loser.resize((90, 90), Image.LANCZOS).convert('RGBA')
			victim.paste(loser, (380, 45), loser)

		img = join_vert_image(image, victim)


		#388,47

		b = BytesIO()
		img.save(b, format="png")
		b.seek(0)
		return b, "png"


	@commands.command(aliases=["ป้าถือไม้กวาด"])
	async def broomaunt(self, ctx, user=None) :
		if user != None :
			av = await im_avatar(ctx, await AnyModel_FindUserOrMember(ctx, user))
		else :
			av = None
		img = await getLastImage(ctx)
		file = await processing_image_to_file(ctx, "broomaunt", self.m_broomaunt, img, av)
		await ctx.send(file=file)

async def setup(bot) :
	await bot.add_cog(await loadInformation(Broomaunt(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
