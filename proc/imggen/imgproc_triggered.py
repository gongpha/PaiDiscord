from io import BytesIO
from random import randint

from PIL import Image
from utils.procimg import ProcImg

name = {
	"th" : "Triggered"
}
author = "gongpha"
desc = {
	"th" : "ถึงกับ ทริกเกอร์ !"
}
classname = ("Triggered",)
class Triggered(ProcImg) :
	def generate(self, users, members, avatars, date, kwargs) :
		img = Image.open("a.png").convert('RGBA')
		thmm = int((img.width * img.height) / 750000)
		triggered = Image.open("triggered-hd.png")
		thm = int((img.height / triggered.height) * 10)
		triggered = triggered.resize((img.width - 40, triggered.height - thm), Image.LANCZOS)
		tint = Image.open('redoverlay.png').convert('RGBA').resize(img.size, Image.NEAREST)
		blank = Image.new('RGBA', (img.width - 64, img.height - 64), color=(231, 19, 29))
		frames = []

		for i in range(8):
			base = blank.copy()
			if i == 0:
				base.paste(img, (-16 * thmm, -16 * thmm), img)
			else:
				base.paste(img, (-32 + randint(-16 * thmm, 16 * thmm), -32 + randint(-16 * thmm, 16 * thmm)), img)


			if i == 0:
				base.paste(triggered, (-10 * thmm, img.height - triggered.height - thm))
			else:
				base.paste(triggered, (-12 + randint(-4 * thmm, 4 * thmm), (img.height - triggered.height) + randint(0, 12 * thmm) - thm))

			base.paste(tint, (0, 0), tint)
			frames.append(base)

		return frames
	#[0].save("a.gif", save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
