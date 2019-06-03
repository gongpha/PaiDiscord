import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
import json
from utils.query import fetchone, commit

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
		await self.bot.log_channel.send(embed=e)
		await self.bot.session.close()
		await self.bot.close()
		self.bot.loop.stop()

	@commands.command()
	@IsOwnerBot()
	async def _send(self, ctx, id, *, text : str) :
		channel = self.bot.get_channel(int(id)) or ctx.message.channel
		await channel.send(text)

	@commands.command()
	@IsOwnerBot()
	async def _send_dm(self, ctx, id, *, text : str) :
		user = await self.bot.fetch_user(id) or ctx.author.id
		channel = user.dm_channel
		if not channel :
			await user.create_dm()
			channel = user.dm_channel
		try :
			await channel.send(text)
		except discord.Forbidden :
			await ctx.send(embed=embed_em(ctx, self.bot.ss("CannotSendTo").format(self.bot.ss("DMWithUser").format(channel.recipient.name)), self.bot.ss("Forbidden")))

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
	async def _set_status(self, ctx, status) :
		reverse_status_indicator_int = [discord.Status.online,
			discord.Status.idle,
			discord.Status.dnd,
			discord.Status.offline,
			discord.Status.invisible,
		]
		reverse_status_indicator_str = {
			"online" : discord.Status.online,
			"idle" : discord.Status.idle,
			"dnd" : discord.Status.dnd,
			"offline" : discord.Status.offline,
			"invisible" : discord.Status.invisible,
		}

		status_indicator = {
			discord.Status.online : [ctx.bot.stringstack["Status"]["Online"], "📗"],
			discord.Status.idle : [ctx.bot.stringstack["Status"]["Idle"], "📒"],
			discord.Status.dnd : [ctx.bot.stringstack["Status"]["DoNotDisturb"], "📕"],
			discord.Status.offline : [ctx.bot.stringstack["Status"]["Offline"], "📓"],
			discord.Status.invisible : [ctx.bot.stringstack["Status"]["Invisible"], "📓"],
		}

		if isinstance(status, int) :
			st = reverse_status_indicator_int[status]
		if isinstance(status, str) :
			st = reverse_status_indicator_str.get(status, discord.Status.online)

		await self.bot.change_presence(status=st)
		sst = status_indicator[st]
		await ctx.send(":ok_hand: " + self.bot.ss("SetItTo").format("{} {}".format(sst[1], sst[0])))

	@commands.command()
	@IsOwnerBot()
	async def _set_credits(self, ctx, id, credits) :
		commit(self.bot, "UPDATE `pai_discord_profile` SET credits=%s WHERE snowflake=%s", (credits, id))
		await ctx.send(":ok_hand:")

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

def setup(bot) :
	bot.add_cog(loadInformation(Experimental(bot)))
