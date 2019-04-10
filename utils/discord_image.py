from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import requests

def avatar_image_circle(user) :
    url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user)
    im = Image.open(BytesIO(requests.get(url).content))
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0,0,im.width,im.height), fill=255)
    im.putalpha(mask)
    return im
