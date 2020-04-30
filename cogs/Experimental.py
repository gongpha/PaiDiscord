import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
from utils.discord_image import *
import json
from io import BytesIO
from utils.query import fetchone, commit, qupdate_all_profile_record, qupdate_all_guild_record

#from discord.ext.commands import MessageConverter, TextChannelConverter
import inspect
import utils.anymodel as anymodel

async def check_m(ctx, chid, id) :
	if not id :
		try :
			message = await commands.MessageConverter().convert(ctx, chid);
		except discord.ext.commands.CommandError :
			message = None
			async with ctx.channel.typing() :
				for guild in ctx.bot.guilds:
					for channel in guild.channels:
						try :
							message = await channel.fetch_message(id)
						except :
							pass
				if not message :
					return None
	else :
		try :
			channel = await ctx.bot.fetch_user(int(chid))
		except discord.NotFound :
			channel = ctx.bot.get_channel(int(chid))
			if not channel :
				return None
		try :
			message = await channel.fetch_message(id)
		except discord.NotFound:
			return None
	return message

class Experimental(Cog) :
	pbot = None
	def __init__(self, bot) :
		pbot = bot

		super().__init__(bot)
		self.cog_hidden = True

	@commands.command()
	@IsOwnerBot()
	async def _shutdown(self, ctx) :
		await ctx.send("👋")
		u = ctx.author
		if isinstance(ctx.message.channel, DMChannel) :
			g = ctx.message.channel
		else :
			g = ctx.message.guild
		e = discord.Embed(title="Client was shutdowned by {0} ({1}) from{4} {2} ({3})".format(u, u.id, g, g.id, "" if isinstance(ctx.message.channel, DMChannel) else " guild"))
		e.color = 0xDD0000
		await self.bot.get_bot_channel("system", "log").send(embed=e)
		await self.bot.session.close()
		await self.bot.close()
		self.bot.loop.stop()

	@commands.command()
	@IsOwnerBot()
	async def _send(self, ctx, id, *, text : str) :
		try :
			user = await ctx.bot.fetch_user(id)
			channel = user.dm_channel
			if not channel :
				await user.create_dm()
				channel = user.dm_channel
		except discord.NotFound :
			channel = ctx.bot.get_channel(int(id))
		if not channel :
			await ctx.send(text)
			return
		try :
			sm = await channel.send(text)
			await ctx.send(sm.jump_url)
		except discord.Forbidden as e:
			await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotSend').format(id), self.bot.ss('Forbidden'), error=e))
			return
		except discord.HTTPException as e :
			await ctx.send(content=e.text, embed=embed_em(ctx, self.bot.ss('CannotSend').format(id), error=e))
			return

	@commands.command()
	@IsOwnerBot()
	async def _edit(self, ctx, chid, id, *, text : str) :
		#u = await self.bot.fetch_user(self.bot.user.id)
		message = await check_m(ctx, chid, id)
		if not message :
			await ctx.send(embed=embed_em(ctx, ctx.bot.ss('CannotEdit').format(id or chid), ctx.bot.ss('MessageNotFound')))
			return

		try :
			await message.edit(content=text)
			await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
		except discord.HTTPException as e:
			await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotEdit').format(id), error=e))

	@commands.command()
	@IsOwnerBot()
	async def _delete(self, ctx, chid, id = None) :
		#u = await self.bot.fetch_user(self.bot.user.id)
		message = await check_m(ctx, chid, id)
		if not message :
			await ctx.send(embed=embed_em(ctx, ctx.bot.ss('CannotDelete').format(id or chid), ctx.bot.ss('MessageNotFound')))
			return
		# except anymodel.NotFound as e:
		# 	await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotEdit').format(id), self.bot.ss('MessageNotFound'), error=e))
		# 	return
		# except anymodel.Forbidden as e:
		# 	#await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotEdit').format(id), self.bot.ss('Forbidden') + "\n" + self.bot.ss('UserIDOwnedThisObjectNotMe').format(message.author.name, message.author.id)))
		# 	await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotEdit').format(id), self.bot.ss('Forbidden'), error=e))
		# 	return

		# except discord.HTTPException as e:
		# 	await ctx.send(content=e.text, embed=embed_em(ctx, self.bot.ss('CannotEdit').format(id), error=e))
		# 	return

		try :
			await message.delete()
			await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
		except discord.Forbidden as e:
			await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotDelete').format(id), self.bot.ss('Forbidden'), error=e))
			return
		except discord.HTTPException as e:
			await ctx.send(embed=embed_em(ctx, self.bot.ss('CannotDelete').format(id), error=e))

	@commands.command()
	@IsOwnerBot()
	async def _history(self, ctx, chid, limit=10) :
		try :
			channel = await ctx.bot.fetch_user(int(chid))
		except discord.NotFound :
			channel = ctx.bot.get_channel(int(chid))
		if ctx.channel.guild.me.guild_permissions.manage_webhooks :
			wh = await ctx.channel.create_webhook(name="Pai's User Representer", avatar=ctx.bot.webhook_avatar)
			async for message in channel.history(limit=10) :

				f = []
				for a in message.attachments :
					f.append(discord.File(fp=BytesIO(await a.read()), filename=a.filename, spoiler=a.is_spoiler()))
				await wh.send(content=message.content or "*empty message*", tts=message.tts, embed=message.embeds[0] if message.embeds else None, files=f, username=message.author.name, avatar_url=message.author.avatar_url)
			await wh.delete()

		else :
			async for message in channel.history(limit=10) :
				f = []
				for a in message.attachments :
					f.append(discord.File(fp=BytesIO(await a.read()), filename=a.filename, spoiler=a.is_spoiler()))
				await ctx.send(content=">>>==================================================\n**{0.author}** [{0.author.mention}] user({0.author.id}) message({0.id}) : \n{0.content}\n<<<==================================================".format(message), tts=message.tts, embed=message.embeds[0] if message.embeds else None, files=f)

	@commands.command()
	@IsOwnerBot()
	async def _send_embed(self, ctx, id, *, jsonembed : str) :
		try :
			channel = self.bot.get_channel(int(id)) or ctx.message.channel
		except :
			await channel.send(embed=embed_em(ctx, "a"))
		else :
			await channel.send(embed=discord.Embed.from_dict(json.loads(jsonembed)))

	@commands.command()
	@IsOwnerBot()
	async def _set_status(self, ctx, st) :
		# reverse_status_indicator_int = [discord.Status.online,
		# 	discord.Status.idle,
		# 	discord.Status.dnd,
		# 	discord.Status.offline,
		# 	discord.Status.invisible,
		# ]
		# reverse_status_indicator_str = {
		# 	"online" : discord.Status.online,
		# 	"idle" : discord.Status.idle,
		# 	"dnd" : discord.Status.dnd,
		# 	"offline" : discord.Status.offline,
		# 	"invisible" : discord.Status.invisible,
		# }

		sti = ctx.bot.resources['StatusIcons'][st]


		# if isinstance(status, int) :
		# 	st = reverse_status_indicator_int[status]
		# if isinstance(status, str) :
		# 	st = reverse_status_indicator_str.get(status, discord.Status.online)

		await self.bot.change_presence(status=st)
		await ctx.send(":ok_hand: " + self.bot.ss("SetItTo").format("{} {}".format(sti, self.bot.ss("Status", "dnd"))))

	# @commands.command()
	# @IsOwnerBot()
	# async def _set_credits(self, ctx, id, credits) :
	# 	await commit(self.bot, "UPDATE `pai_discord_profile` SET credits=%s WHERE snowflake=%s", (credits, id))
	# 	await ctx.send(":ok_hand:")

	@commands.command()
	@IsOwnerBot()
	async def _set_game(self, ctx, type, *, name) :
		g = discord.Game(name=name, type=type)
		await self.bot.change_presence(activity=g)
		await ctx.send(":ok_hand: " + self.bot.ss("SetItTo").format("{} {}".format(self.bot.ss("ActivityType", type), name)))

	@commands.command()
	@IsOwnerBot()
	async def _set_game_playing(self, ctx, *, name) :
		g = discord.Game(name=name)
		await self.bot.change_presence(activity=g)
		await ctx.send(":ok_hand: " + self.bot.ss("SetItTo").format("{} {}".format(self.bot.ss("ActivityType", "playing"), name)))

	@commands.command()
	@IsOwnerBot()
	async def _my_info_guild(self, ctx, gid : int = None) :
		guild = ctx.bot.get_guild(int(gid)) if gid else ctx.guild
		if not guild :
			await ctx.send(embed=embed_em(ctx, self.bot.ss('ObjectNotFoundFromObject').format(self.bot.ss('Model', 'Guild'), gid)))

		e = model_info(ctx, guild.me)
		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _refresh_configs(self, ctx) :
		ctx.bot.load_configs(self.info_fname, self.channels_fname, self.auths_fname, self.configs_fname, self.loaded_dev)
		await ctx.send(":ok_hand:")
	# @commands.command()
	# @IsOwnerBot()
	# async def _id(self, ctx, id) :
	# 	IDConverter
	# 	await self.bot.change_presence(activity=g)
	# 	await ctx.send(":ok_hand: " + self.bot.ss("SetItTo").format("{} {}".format(self.bot.ss("ActivityType", "playing"), name)))

	@commands.command()
	@IsOwnerBot()
	async def _process(self, ctx, *, code : str) :
		code = code.strip('` ')
		python = '```py\n{}\n```'
		result = None

		env = {
			'bot': self.bot,
			'ctx': ctx,
			'message': ctx.message,
			'guild': ctx.message.guild,
			'channel': ctx.message.channel,
			'author': ctx.message.author
		}

		env.update(globals())

		try:
			result = eval(code, env)
			if inspect.isawaitable(result):
				result = await result
		except Exception as e:
			await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
			return

		await ctx.send(python.format(result))

	# @commands.command()
	# @IsOwnerBot()
	# async def _send_embed(self, ctx, id, *, embed : str) :
	# 	def _get(object, item) :
	# 		try :
	# 			return y[item]
	# 		except KeyError:
	# 			return ""
	#
	#
	#
	# 	y= json.loads(embed)
	# 	e = discord.Embed()
	# 	e.title = _get(y, "title") or ""
	# 	e.description = _get(y, "description") or ""
	# 	for i in _get(y, "items") :
	# 		e.add_field(name=_get(i, "name"), value=_get(i, "value"), inline=_get(i, ""))
	# 	channel = self.bot.get_channel(int(id)) or ctx.message.channel
	# 	await channel.send(embed=e)

	# @commands.command()
	# @IsOwnerBot()
	# async def _edit(self, ctx, id, *, text : str) :
	# 	channel = self.bot.get_channel(int(id)) or ctx.message.channel
	# 	await channel.send(text)

	@commands.command()
	@IsOwnerBot()
	async def _update_all_users(self, ctx) :
		await qupdate_all_profile_record(self.bot)
		await ctx.send(":ok_hand:")

	@commands.command()
	@IsOwnerBot()
	async def _update_all_guilds(self, ctx) :
		await qupdate_all_guild_record(self.bot)
		await ctx.send(":ok_hand:")

	@commands.command()
	@IsOwnerBot()
	async def _guilds(self, ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None, attr : str = None) :
		if end is None:
			end = start + 20
		stri = "```\n"
		stri += "\n".join([str(x) + (("\n (" + str(getattr(x, attr)) + ")") if attr != None else "") for x in ctx.bot.guilds][:20])
		stri += '```'
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _users(self, ctx, start : typing.Optional[int] = 0, end : typing.Optional[int] = None, attr : str = None) :
		if end is None:
			end = start + 20
		stri = "```\n"
		stri += "\n".join([str(x) + (("\n (" + str(getattr(x, attr)) + ")") if attr != None else "") for x in ctx.bot.users][:20])
		stri += '```'
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		await ctx.send(embed=e)









##############################################################





	@commands.command()
	@IsOwnerBot()
	async def _channel_list(self, ctx, guild_id = None, attr : str = None) :
		if guild_id == "this" :
			guild = ctx.guild
		else :
			guild = ctx.bot.get_guild(int(guild_id)) or ctx.guild
		e = embed_t(ctx, len(guild.text_channels) + len(guild.voice_channels), len(guild.categories))
		for c in guild.categories :
			e.add_field(name=c.name, value="\n".join(ch.name + ((" (" + str(getattr(ch, attr)) + ")") if attr != None else "") for ch in c.channels))

		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _attachments(self, ctx, chid, id = None, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
		message = await check_m(ctx, chid, id)
		if not message :
			await ctx.send(embed=embed_em(ctx, ctx.bot.ss('CannotEdit').format(id or chid), ctx.bot.ss('MessageNotFound')))
			return

		stri = ". . ."
		if end is None:
			end = start + 20
		if len(message.attachments) > 0 :
			stri = "\n".join(["[{}]({})".format(x.filename,x.url) for x in message.attachments][:20])
			print(stri)
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		e.set_footer(text=str(len(message.attachments)))
		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _lastimg(self, ctx, count = 1, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
		l = await getLastImageOrAnimatedImage(ctx, count, 1);

		stri = ". . ."
		if end is None:
			end = start + 20
		if not isinstance(l, list) :
			l = [l]
		if len(l) > 0 :
			stri = "\n".join([str(x) for x in l][:20])
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		e.set_footer(text=str(len(l)))
		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _lastimg_animate(self, ctx, count = 1, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
		l = await getLastAnimatedImage(ctx, count, 1);

		stri = ". . ."
		if end is None:
			end = start + 20
		if not isinstance(l, list) :
			l = [l]
		if len(l) > 0 :
			stri = "\n".join([str(x) for x in l][:20])
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		e.set_footer(text=str(len(l)))
		await ctx.send(embed=e)

	@commands.command()
	@IsOwnerBot()
	async def _lastimg_static(self, ctx, count = 1, start : typing.Optional[int] = 0, end : typing.Optional[int] = None) :
		l = await getLastImage(ctx, count, 1);

		stri = ". . ."
		if end is None:
			end = start + 20
		if not isinstance(l, list) :
			l = [l]
		if len(l) > 0 :
			stri = "\n".join([str(x) for x in l][:20])
		e = embed_t(ctx, "", "")
		e.add_field(name=f"{start} - {end}", value=stri)
		e.set_footer(text=str(len(l)))
		await ctx.send(embed=e)

	@commands.command()
	async def pai_avatar(self, ctx) :
		if (ctx.bot.user.id == 473457863822409728 or ctx.bot.user.id == 457908707817422860) and ctx.bot.hd_avatar_url :
			await ctx.send(ctx.bot.hd_avatar_url)

def setup(bot) :
	bot.add_cog(loadInformation(Experimental(bot)))
