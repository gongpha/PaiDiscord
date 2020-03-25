from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint
from io import BytesIO

class Image__Failed(Exception) :
	pass

def rgbToTuple(color) :
	if color == None :
		return (randint(0,255),randint(0,255),randint(0,255))
	else :
		return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

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

# orig : keep top image's size
# 1 = top, 2 = bottom
def join_vert_image(image_top, image_bottom, orig = 1, retcenter = 0, scaleby = Image.LANCZOS) :
	if orig == 1 :
		ps = image_top.width / image_bottom.width
		scaled_image = image_bottom.resize((image_top.width, int(ps * image_bottom.height)), scaleby)
		result = Image.new('RGBA', (image_top.width, image_top.height + scaled_image.height), color=(255, 255, 255))
		result.paste(image_top, (0, 0))
		result.paste(scaled_image, (0, image_top.height))
	elif orig == 2 :
		ps = image_bottom.width / image_top.width
		scaled_image = image_top.resize((image_bottom.width, int(ps * image_top.height)), scaleby)
		result = Image.new('RGBA', (image_bottom.width, image_bottom.height + scaled_image.height), color=(255, 255, 255))
		result.paste(scaled_image, (0, 0))
		result.paste(image_bottom, (0, scaled_image.height))
	else :
		return None

	if (retcenter) :
		return (result, scaled_image.height)
	else :
		return result

def resize_img_b(im, w, h, resample) :
	resamp = {
		"nearest" : Image.NEAREST,
		"bilinear" : Image.BILINEAR,
		"bicubic" : Image.BICUBIC,
		"lanczos" : Image.LANCZOS
	}
	frames = []
	try :
		while 1 :
			try :
				img = im.resize((int(w), int(h)), resamp.get(resample, lambda: PILImage.BILINEAR))
				frames.append(img)
				im.seek(im.tell() + 1)
			except ValueError :
				raise Image__Failed("VAL")
			except MemoryError :
				raise Image__Failed("MEM")

	except EOFError :
		pass

	b = BytesIO()
	if len(frames) > 1 :
		frames[0].save(b, format='gif', save_all=True, append_images=frames[1:], loop=0, optimize=True)
		fmt = 'gif'
		print('@gif')
	else :
		frames[0].save(b, format='png')
		fmt = 'png'
		print('@png')
	b.seek(0)

	return b, fmt
