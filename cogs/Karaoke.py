import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import embed_t, extract_str
from utils.discord_image import getLastImage
from utils.text import textimage
from utils.procimg import rgbToTuple
from random import randint
class Karaoke(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	def k_wanbuaban(self, text, image, percent, size = 1) :
		# by gongpha, designed like Topline-Diamond's Wangbuaban (ท็อปไลน์-ไดมอนด์ วังบัวบาน ของ พุ่มพวง ดวงจันทร์)

		size = int(32 * (image.width / 250) * size)

		img_text = textimage(text, "font/angsab.ttf", size, (255,255,255), (0,0,0), (0,0,0), 2)
		img_text_scored = textimage(text, "font/angsab.ttf", size, (0,50,255), (255,255,255), (0,0,0), 2)

		#print((0, 0, int(img_text_scored.width * percent / 100), img_text_scored.height))
		img_text_crop = img_text.crop((int(img_text_scored.width * (percent / 100)), 0, img_text_scored.width, img_text_scored.height))
		score_crop = img_text_scored.crop((0, 0, int(img_text_scored.width * (percent / 100)), img_text_scored.height))
		# draw = ImageDraw.Draw(image)
		# image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2),int((y / 100)*(image.height))),img_text_crop)
		# image.paste(score_crop,(int(image.width / 2 - width/2),int((y / 100)*(image.height))),score_crop)
		image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - img_text.width / 2), image.height - img_text_crop.height - 50),img_text_crop)
		image.paste(score_crop,(int(image.width / 2 - img_text.width / 2), image.height - score_crop.height - 50),score_crop)

		return image

	def k_grammy(self, text, eng, image, percent, _size = 1) :
		# by gongpha, designed by GMM GRAMMY

		size = int(36 * (image.width / 250) * _size)
		esize = int(12 * (image.width / 250) * _size)


		img_text = textimage(text, "font/grammy.ttf", size, (255,255,255), (0,0,0), None, 2)
		img_text_scored = textimage(text, "font/grammy.ttf", size, (0,50,255), (255,255,255), None, 2)

		eimg_text = textimage(eng.upper(), "font/futura.ttf", esize, (230,100,35), (0,0,0), None, 2)
		eimg_text_scored = textimage(eng.upper(), "font/futura.ttf", esize, (0,50,255), (255,255,255), None, 2)

		#print((0, 0, int(img_text_scored.width * percent / 100), img_text_scored.height))
		img_text_crop = img_text.crop((int(img_text_scored.width * (percent / 100)), 0, img_text_scored.width, img_text_scored.height))
		score_crop = img_text_scored.crop((0, 0, int(img_text_scored.width * (percent / 100)), img_text_scored.height))

		eimg_text_crop = eimg_text.crop((int(eimg_text_scored.width * (percent / 100)), 0, eimg_text_scored.width, eimg_text_scored.height))
		escore_crop = eimg_text_scored.crop((0, 0, int(eimg_text_scored.width * (percent / 100)), eimg_text_scored.height))

		# draw = ImageDraw.Draw(image)
		# image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2),int((y / 100)*(image.height))),img_text_crop)
		# image.paste(score_crop,(int(image.width / 2 - width/2),int((y / 100)*(image.height))),score_crop)
		image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - img_text.width / 2), image.height - img_text_crop.height - 75), img_text_crop)
		image.paste(score_crop,(int(image.width / 2 - img_text.width / 2), image.height - score_crop.height - 75),score_crop)

		image.paste(eimg_text_crop,(int(eimg_text_scored.width * (percent / 100)) + int(image.width / 2 - eimg_text.width / 2), image.height - eimg_text_crop.height - 20), eimg_text_crop)
		image.paste(escore_crop,(int(image.width / 2 - eimg_text.width / 2), image.height - escore_crop.height - 20),escore_crop)

		return image

	def k_topline_pp(self, text, image, color, percent, size=1) :
		# by gongpha, designed like Topline-Diamond (ท็อปไลน์-ไดมอนด์)
		rgb = rgbToTuple(color)

		size = int(32 * (image.width / 250) * size)

		img_text = textimage(text, "font/toplinebreak.ttf", size, (255,255,255), (0,0,0), "asOutline", 2)
		img_text_scored = textimage(text, "font/toplinebreak.ttf", size, rgb, None, "asOutline", 2)

		#print((0, 0, int(img_text_scored.width * percent / 100), img_text_scored.height))
		img_text_crop = img_text.crop((int(img_text_scored.width * (percent / 100)), 0, img_text_scored.width, img_text_scored.height))
		score_crop = img_text_scored.crop((0, 0, int(img_text_scored.width * (percent / 100)), img_text_scored.height))
		# draw = ImageDraw.Draw(image)
		# image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2),int((y / 100)*(image.height))),img_text_crop)
		# image.paste(score_crop,(int(image.width / 2 - width/2),int((y / 100)*(image.height))),score_crop)
		image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - img_text.width / 2), image.height - img_text_crop.height - 50),img_text_crop)
		image.paste(score_crop,(int(image.width / 2 - img_text.width / 2), image.height - score_crop.height - 50),score_crop)

		return image

	@commands.command()
	async def wanbuaban(self, ctx, *, text : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		self.k_wanbuaban(text, await getLastImage(ctx), randint(0, 100), 1).save('cache/wanbuaban.png')
		file = discord.File("cache/wanbuaban.png", filename="wanbuaban.png")
		await ctx.send("{} : `{}`".format(self.bot.stringstack["Model"]["Text"], text),file=file)

	@commands.command()
	async def topline(self, ctx, *, text : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		self.k_topline_pp(text, await getLastImage(ctx), None, randint(0, 100), 1).save('cache/topline.png')
		file = discord.File("cache/topline.png", filename="topline-diamond.png")
		await ctx.send("{} : `{}`".format(self.bot.stringstack["Model"]["Text"], text),file=file)

	@commands.command()
	async def grammy(self, ctx, *, text : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		t = await extract_str(ctx, text, 2)
		if not t :
			return
		self.k_grammy(t[0], t[1], await getLastImage(ctx), randint(0, 100), 1).save('cache/grammy-karaoke.png')
		file = discord.File("cache/grammy-karaoke.png", filename="grammy-karaoke.png")
		await ctx.send("{} : `{}` | `{}`".format(self.bot.stringstack["Model"]["Text"], t[0], t[1]),file=file)
def setup(bot) :
	bot.add_cog(loadInformation(Karaoke(bot)))
