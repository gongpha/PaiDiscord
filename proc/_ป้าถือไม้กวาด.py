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
from utils.text import textimage
#from utils.procimg import ProcImg

name = "_ป้าถือไม้กวาด"

class _ป้าถือไม้กวาด(Proc) :
	desc = {
		"th" : {
			"ป้าถือไม้กวาด" : "ป้าถือไม้กวาด จ้องตีใครสักคน",
		}
	}
	author = "gongpha"
	usag = {
		"th" : {
			"ป้าถือไม้กวาด" : "<ผู้ใช้แทนคนในรูป=ไม่มี>"
		}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	def m_broomaunt(self, image, loser=None) :
		# by gongpha

		victim = Image.open("template/meme/ป้าถือไม้กวาด.png")
		ps = image.width / victim.width
		if loser != None :
			loser = loser.resize((90, 90), Image.LANCZOS).convert('RGBA')
			victim.paste(loser, (380, 45), loser)

		victim = victim.resize((image.width, int(ps * victim.height)), Image.LANCZOS)

		result = Image.new('RGBA', (image.width, image.height + victim.height), color=(255, 255, 255))
		result.paste(image, (0, 0))
		result.paste(victim, (0, image.height))


		#388,47

		b = BytesIO()
		result.save(b, format="png")
		b.seek(0)
		return b


	@commands.command(name="ป้าถือไม้กวาด", aliases=["broomaunt"])
	async def broomaunt(self, ctx, user=None) :
		if user != None :
			av = await im_avatar(ctx, await AnyModel_FindUserOrMember(ctx, user))
		else :
			av = None
		img = await getLastImage(ctx)
		file = await processing_image_to_file(ctx, "broomaunt.png", self.m_broomaunt, img, av)
		await ctx.send(file=file)

def setup(bot) :
	bot.add_cog(loadInformation(_ป้าถือไม้กวาด(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
