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
		failed = 0
		e = embed_wm(ctx, self.bot.ss("Warning"), self.bot.ss("ActionCannotUndo"))
		if await waitReactionRequired(ctx, self.bot, ['\N{HEAVY CHECK MARK}','\N{BALLOT BOX WITH CHECK}','\N{WHITE HEAVY CHECK MARK}'], ctx.author.id, e) :
			pcm = await ctx.send('<a:pai__processing:592209674447618058> {}'.format(ctx.bot.ss('Processing')))
			rs = self.bot.ss("Reason", "CommandBy").format(ctx.author)
			for ch in ctx.message.guild.channels :
				try :
					await ch.edit(name="c{}".format(str(ch.id)), reason=rs)
				except :
					failed += 1
			for e in ctx.message.guild.emojis :
				try :
					await e.edit(name="e{}".format(str(e.id)), reason=rs)
				except :
					failed += 1
			for u in ctx.message.guild.members :
				#if u.id != ctx.message.guild.owner_id or u.top_role < ctx.message.guild.me.top_role :
				try :
					await u.edit(nick="u{}".format(str(u.id)), reason=rs)
				except :
					failed += 1
			for r in ctx.message.guild.roles :
				if ctx.message.guild.me.top_role > r :
					try :
						await r.edit(nick="r{}".format(str(r.id)), reason=rs)
					except :
						failed += 1
			await pcm.edit(content='\N{WHITE HEAVY CHECK MARK} {}\n{} : {}'.format(ctx.bot.ss('Success'), ctx.bot.ss('Failed'), failed))
def setup(bot) :
	bot.add_cog(loadInformation(MagickBomb(bot)))
