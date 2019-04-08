from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from io import BytesIO
import requests
from random import randint
import platform

def text_outline_topline(size, stroke, text, outline=None, shadow=None, fill=None, fontp=None) :

	if fontp == None :
		fontp = "font/toplinebreak.ttf"
	font = ImageFont.truetype(fontp, int(size))

	if fill == None :
		fill = (randint(0,255),randint(0,255),randint(0,255))
	if outline == None :
		outline = tuple((int(0.25 * c)) for c in fill)
	if shadow == None :
		shadow = (0,0,0)
	else :
		if shadow == "asOutline" :
			shadow = outline

	ascent, descent = font.getmetrics()
	(width, baseline), (offset_x, offset_y) = font.font.getsize(text)
	textX = 2
	textY = 2 - offset_y
	img_text = Image.new('RGBA', (width + (stroke*4), baseline + (stroke*4)), (0,0,0,0))
	draw_txt = ImageDraw.Draw(img_text)
	# platform.system() != "Windows"

	draw_txt.text((textX-stroke+(stroke*2), textY-stroke+(stroke*2)), text,shadow,font)
	draw_txt.text((textX+stroke+(stroke*2), textY-stroke+(stroke*2)), text,shadow,font)
	draw_txt.text((textX+stroke+(stroke*2), textY+stroke+(stroke*2)), text,shadow,font)
	draw_txt.text((textX-stroke+(stroke*2), textY+stroke+(stroke*2)), text,shadow,font)
	draw_txt.text((textX-stroke+(stroke*2), textY+(stroke*2)), text,shadow,font)
	draw_txt.text((textX+stroke+(stroke*2), textY+(stroke*2)), text,shadow,font)
	draw_txt.text((textX+(stroke*2), textY+stroke+(stroke*2)), text,shadow,font)
	draw_txt.text((textX+(stroke*2), textY-stroke+(stroke*2)), text,shadow,font)

	draw_txt.text((textX-stroke, textY-stroke), text,outline,font)
	draw_txt.text((textX+stroke, textY-stroke), text,outline,font)
	draw_txt.text((textX+stroke, textY+stroke), text,outline,font)
	draw_txt.text((textX-stroke, textY+stroke), text,outline,font)
	draw_txt.text((textX-stroke, textY), text,outline,font)
	draw_txt.text((textX+stroke, textY), text,outline,font)
	draw_txt.text((textX, textY+stroke), text,outline,font)
	draw_txt.text((textX, textY-stroke), text,outline,font)

	draw_txt.text((textX, textY), text, fill, font)
	return [img_text, width, baseline, ascent, descent, offset_x, offset_y]

def rgbToTuple(color : str) :
	if color == 'random' :
		return (randint(0,255),randint(0,255),randint(0,255))
	else :
		return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

class filter :
	def median(im) :
		members = [(0,0)] * 9
		newimg = Image.new("RGB",(im.width,im.height), "white")
		for i in range(1,im.width-1):
			for j in range(1,im.height-1):
				members[0] = im.getpixel((i-1,j-1))
				members[1] = im.getpixel((i-1,j))
				members[2] = im.getpixel((i-1,j+1))
				members[3] = im.getpixel((i,j-1))
				members[4] = im.getpixel((i,j))
				members[5] = im.getpixel((i,j+1))
				members[6] = im.getpixel((i+1,j-1))
				members[7] = im.getpixel((i+1,j))
				members[8] = im.getpixel((i+1,j+1))
				members.sort()
				newimg.putpixel((i,j),(members[4]))
		return newimg
	# for i in range(1,im.width-1):
	# 	for j in range(1,im.height-1):
	#         # members[0] = img.getpixel((i-1,j-1))
	#         # members[1] = img.getpixel((i-1,j))
	#         # members[2] = img.getpixel((i-1,j+1))
	#         # members[3] = img.getpixel((i,j-1))
	#         # members[4] = img.getpixel((i,j))
	#         # members[5] = img.getpixel((i,j+1))
	#         # members[6] = img.getpixel((i+1,j-1))
	#         # members[7] = img.getpixel((i+1,j))
	# 		# members[8] = img.getpixel((i+1,j+1))
	# 		x = -(radius)
	# 		y = -(radius)
	# 		for m in range(((radius * 2) + 1) * ((radius * 2) + 1)) :
	# 			members[m] = im.getpixel((i+x,j+y))
	# 			if y >= radius :
	# 				y = -(radius)
	# 			if x >= radius :
	# 				x = -(radius)
	# 				y += 1
	# 			else :
	# 				x += 1
	# 		members.sort()
	# 		newimg.putpixel((i,j),(members[round((((radius * 2) + 1) * ((radius * 2) + 1)) / 2)]))
class generate :
	def infoimage(ctx,user,bg) :
		draw = ImageDraw.Draw(bg)
		if platform.system() == "Windows" :
			fontsmall = ImageFont.truetype("font/plat.ttf", 22)
			font = ImageFont.truetype("font/plat.ttf", 32)
			fontbig = ImageFont.truetype("font/plat.ttf", 64)
		else :
			fontsmall = ImageFont.truetype("font/plat.ttf", 22, layout_engine=ImageFont.LAYOUT_RAQM)
			font = ImageFont.truetype("font/plat.ttf", 32, layout_engine=ImageFont.LAYOUT_RAQM)
			fontbig = ImageFont.truetype("font/plat.ttf", 64, layout_engine=ImageFont.LAYOUT_RAQM)

		response = requests.get(user.avatar_url)
		av = Image.open(BytesIO(response.content))
		av.thumbnail((128,128), Image.ANTIALIAS)
		bg.paste(av,(100,64))
		draw.text((260, 64), user.name, (0, 0, 0), font=fontbig)
		# display_name
		draw.text((100, 38), ">> {}".format(ctx.message.author.name), (220, 220, 220), font=fontsmall)
		draw.text((260, 128), str(user.id), (0, 0, 0), font=font)
		#draw.text((5, 140), "User Status : {}".format(user.status), (255, 255, 255), font=font)
		draw.text((260, 164), "Created : {}".format(user.created_at), (50, 50, 50), font=fontsmall)

		# rel = user.relationship

		# if rel == None :
			# draw.text((260, 220), "NO RELATIONSHIP", (221, 0, 0), font=fontsmall)
		# else :
			# rel.user = ctx.message.author
			# if rel.type == discord.RelationshipType.friend :

		#draw.text((260, 220), "Is friend", (0, 170, 128), font=fontsmall)
			# elif rel.type == discord.RelationshipType.blocked :
				# draw.text((260, 220), "Blocked", (221, 0, 0), font=fontsmall)
			# elif rel.type == discord.RelationshipType.incoming_request :
				# draw.text((260, 220), "Outcomming Request", (255, 201, 15), font=fontsmall)
			# elif rel.type == discord.RelationshipType.outgoing_request :
				# draw.text((260, 220), "Incomming Request", (255, 201, 15), font=fontsmall)

		if user.is_avatar_animated() :
			draw.text((100, 195), "Animated", (131, 6, 255), font=fontsmall)
		return bg

	def topline_karaoke(text, image, color, percent, x, y, size=1) :
		# by gongpha, designed to like Topline-Diamond (ท็อปไลน์-ไดมอนด์)
		rgb = rgbToTuple(color)

		size = int(32 * (image.width / 250) * size)

		img_text_list = text_outline_topline(size, 2, text, (0,0,0), "asOutline", (255,255,255))
		img_text_scored_list = text_outline_topline(size, 2, text, None, "asOutline", rgb)

		img_text = img_text_list[0]
		img_text_scored = img_text_scored_list[0]
		width = img_text_list[1]

		# SCORED text

		#print((0, 0, int(img_text_scored.width * percent / 100), img_text_scored.height))
		img_text_crop = img_text.crop((int(img_text_scored.width * (percent / 100)), 0, img_text_scored.width, img_text_scored.height))
		score_crop = img_text_scored.crop((0, 0, int(img_text_scored.width * (percent / 100)), img_text_scored.height))
		# draw = ImageDraw.Draw(image)
		# image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2),int((y / 100)*(image.height))),img_text_crop)
		# image.paste(score_crop,(int(image.width / 2 - width/2),int((y / 100)*(image.height))),score_crop)
		image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2), image.height - img_text_crop.height - 50),img_text_crop)
		image.paste(score_crop,(int(image.width / 2 - width/2), image.height - score_crop.height - 50),score_crop)

		return image

	def topline_karaoke_wanbuaban(text, image, percent, x, y, size=1) :
		# by gongpha, designed to like Topline-Diamond's Wanbuaban (ท็อปไลน์-ไดมอนด์ วังบัวบาน)

		size = int(32 * (image.width / 250) * size)

		img_text_list = text_outline_topline(size, 2, text, (0,0,0), (0,0,0), (255,255,255), "font/angsab.ttf")
		img_text_scored_list = text_outline_topline(size, 2, text, (255,255,255), (0,0,0), (0,50,255), "font/angsab.ttf")

		img_text = img_text_list[0]
		img_text_scored = img_text_scored_list[0]
		width = img_text_list[1]

		# SCORED text

		#print((0, 0, int(img_text_scored.width * percent / 100), img_text_scored.height))
		img_text_crop = img_text.crop((int(img_text_scored.width * (percent / 100)), 0, img_text_scored.width, img_text_scored.height))
		score_crop = img_text_scored.crop((0, 0, int(img_text_scored.width * (percent / 100)), img_text_scored.height))
		# draw = ImageDraw.Draw(image)
		# image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2),int((y / 100)*(image.height))),img_text_crop)
		# image.paste(score_crop,(int(image.width / 2 - width/2),int((y / 100)*(image.height))),score_crop)
		image.paste(img_text_crop,(int(img_text_scored.width * (percent / 100)) + int(image.width / 2 - width / 2), image.height - img_text_crop.height - 50),img_text_crop)
		image.paste(score_crop,(int(image.width / 2 - width/2), image.height - score_crop.height - 50),score_crop)

		return image
