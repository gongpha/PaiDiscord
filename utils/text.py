from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
def textimage(text : str = 'null', font : str = '../font/tahoma.ttf', size : int = 10, fill = (255,255,255), outline = None, shadow = None, stroke : int = 2) :

	f = ImageFont.truetype(font, int(size))

	if outline == None :
		outline = tuple((int(0.25 * c)) for c in fill)

	if shadow == "asOutline" :
		shadow = outline

	ascent, descent = f.getmetrics()
	(width, baseline), (offset_x, offset_y) = f.font.getsize(text)
	textX = 2 if outline != None else 0
	textY = (2 - offset_y) if outline != None else -offset_y
	img_text = Image.new('RGBA', (width + (stroke*((2 if outline != None else 0) + (2 if shadow != None else 0))), baseline + (stroke*((2 if outline != None else 0) + (2 if shadow != None else 0))) + 2), (0,0,0,0))
	draw_txt = ImageDraw.Draw(img_text)

	# This will help extending string if the last character's width is zero
	texts = text + " "

	if shadow != None and stroke > 0 :
		draw_txt.text((textX-stroke+(stroke*2), textY-stroke+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX+stroke+(stroke*2), textY-stroke+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX+stroke+(stroke*2), textY+stroke+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX-stroke+(stroke*2), textY+stroke+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX-stroke+(stroke*2), textY+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX+stroke+(stroke*2), textY+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX+(stroke*2), textY+stroke+(stroke*2)), texts,shadow,f)
		draw_txt.text((textX+(stroke*2), textY-stroke+(stroke*2)), texts,shadow,f)

	if outline != None and stroke > 0 :
		draw_txt.text((textX-stroke, textY-stroke), texts,outline,f)
		draw_txt.text((textX+stroke, textY-stroke), texts,outline,f)
		draw_txt.text((textX+stroke, textY+stroke), texts,outline,f)
		draw_txt.text((textX-stroke, textY+stroke), texts,outline,f)
		draw_txt.text((textX-stroke, textY), texts,outline,f)
		draw_txt.text((textX+stroke, textY), texts,outline,f)
		draw_txt.text((textX, textY+stroke), texts,outline,f)
		draw_txt.text((textX, textY-stroke), texts,outline,f)

	draw_txt.text((textX, textY), texts, fill, f)
	return img_text
