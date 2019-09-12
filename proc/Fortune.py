import discord
from io import BytesIO
from random import randrange
from PIL import Image
from discord.ext import commands
from utils.proc import Proc
from utils.proc import loadInformation
from utils.discord_image import im_avatar, processing_image_to_file
from utils.anymodel import AnyModel_FindUserOrMember
from utils.discord_image import getLastImage
from utils.text import textimage
#from utils.procimg import ProcImg

name = "Fortune"

class Fortune(Proc) :
	desc = {
		"th" : {
			"lovematch" : "เอ๊ะ ! ความรักนี่มัน !?",
			"lovematch_random" : "เอ๊ะ ! ความรักนี่มัน !? (แบบสุ่ม)"
		}
	}
	author = "gongpha"
	usag = {
		"th" : {
			"lovematch" : "<ผู้ใช้ที่จะตรวจสอบ>",
			"lovematch_random" : "<ผู้ใช้ที่จะตรวจสอบ>"
		}
	}
	def __init__(self, bot) :
		super().__init__(bot)

	def m_match(self, image_a, image_b, percent) :
		img_a = image_a.convert('RGBA').resize((450,450), Image.LANCZOS)
		img_b = image_b.convert('RGBA').resize((468,468), Image.LANCZOS)
		love = Image.open("template/proc/match.png")
		result = Image.new('RGBA', love.size)

		result.paste(img_a, (23, 110), img_a)
		result.paste(img_b, (584, 76), img_b)
		result.paste(love, (0, 0), love)

		# 350, 475

		img_text = textimage(str(int(percent)) + '%', "font/plat.ttf", 100, (255, 255, 255), None, None, 0)
		result.paste(img_text, (350, 475), img_text)

		b = BytesIO()
		result.save(b, format="png")
		b.seek(0)
		return b

	@commands.command()
	async def lovematch(self, ctx, user) :
		async with ctx.channel.typing() :
			datuser = await AnyModel_FindUserOrMember(ctx, user)
			img = await im_avatar(ctx, datuser)
			percent = (((datuser.id % 100) + (ctx.author.id % 100)) / 200) * 100
			file = await processing_image_to_file(ctx, "match.png", self.m_match, await im_avatar(ctx, ctx.author), img, percent)
			await ctx.send(file=file)

	@commands.command()
	async def lovematch_random(self, ctx, user) :
		async with ctx.channel.typing() :
			datuser = await AnyModel_FindUserOrMember(ctx, user)
			img = await im_avatar(ctx, datuser)
			percent = randrange(0, 100)
			file = await processing_image_to_file(ctx, "match.png", self.m_match, await im_avatar(ctx, ctx.author), img, percent)
			await ctx.send(file=file)

def setup(bot) :
	bot.add_cog(loadInformation(Fortune(bot)))
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
