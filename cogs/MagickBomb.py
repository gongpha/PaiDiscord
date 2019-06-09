import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
class MagickBomb(Cog) :
	pbot = None
	def __init__(self, bot) :
		pbot = bot
		super().__init__(bot)

	@commands.command()
	@IsOwnerGuild()
	@CanManageMessages()
	@CanManageNicknames()
	@CanManageRoles()
	@IsNotDM()
	async def magick__sidname(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)

		e = embed_wm(self.bot, ctx, self.bot.stringstack["Warning"], self.bot.stringstack["ActionCannotUndo"])
		if await waitReactionRequired(ctx, self.bot, ['\N{HEAVY CHECK MARK}','\N{BALLOT BOX WITH CHECK}','\N{WHITE HEAVY CHECK MARK}'], ctx.author.id, e) :
			for ch in ctx.message.guild.channels :
				await ch.edit(name="c{}".format(str(ch.id)), reason=self.bot.stringstack["Reason"]["CommandBy"].format(ctx.author))
			for e in ctx.message.guild.emojis :
				await e.edit(name="e{}".format(str(e.id)), reason=self.bot.stringstack["Reason"]["CommandBy"].format(ctx.author))
			for u in ctx.message.guild.members :
				if u.id != ctx.message.guild.owner_id or u.top_role < ctx.message.guild.me.top_role :
					await u.edit(nick="u{}".format(str(u.id)), reason=self.bot.stringstack["Reason"]["CommandBy"].format(ctx.author))
			for r in ctx.message.guild.roles :
				if ctx.message.guild.me.top_role > r :
					await r.edit(nick="r{}".format(str(r.id)), reason=self.bot.stringstack["Reason"]["CommandBy"].format(ctx.author))

def setup(bot) :
	bot.add_cog(loadInformation(MagickBomb(bot)))
