import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint

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
