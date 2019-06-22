import random
# from aioauth_client import OAuth2Client
# from aiohttp import ClientSession

async def r_RandomCat(b, l) :
	r = await b.session.get('https://aws.random.cat/meow')
	if r.status != 200 :
		return None
	j = await r.json()
	return (j["file"], j["file"])

async def r_Imgur(b, l) :
	data = {
		'refresh_token': b.getAuth("imgur", "refresh_token"),
		'client_id': b.auth("imgur", "client_id"),
		'client_secret': b.auth("imgur", "client_secret"),
		'grant_type': 'refresh_token'
	}


	t = await b.session.post("https://api.imgur.com/oauth2/token", data=data)
	if t.status != 200 :
		return None

	jt = await t.json()









	headers = {}
	headers['Authorization'] = 'Bearer {}'.format(jt["access_token"])
	p = {}
	if not l :
		lto = "https://api.imgur.com/3/gallery/random/random/"
	else :
		p['q'] = " ".join(l)
		lto = "https://api.imgur.com/3/gallery/search/"

	r = await b.session.get(lto, headers=headers, params=p)





# 	client = OAuth2Client(session=b.session,client_id=b.auth["imgur"]["client_id"],client_secret=b.auth["imgur"]["client_secret"],)
#
# (self, client_id, client_secret, base_url=None,
#                  authorize_url=None,
#                  access_token=None, access_token_url=None,
#                  access_token_key=None, session=None, logger=None,
# **params)

	if r.status != 200 :
		return None
	j = await r.json()
	try :
		i = random.choice(j["data"])
		l = i["link"]
		try :
			ii = random.choice(i["images"])
		except KeyError :
			ii = i
	except IndexError :
		return None
	return (ii["link"], l)
