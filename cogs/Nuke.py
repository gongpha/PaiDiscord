import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
class Nuke(Cog) :
	pbot = None
	def __init__(self, bot) :
		pbot = bot
		super().__init__(bot)

	@commands.command()
	@IsOwnerGuild()
	async def nuke__channels(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)
		if not ctx.message.guild.me.guild_permissions.manage_channels :
			await ctx.send(embed=embed_em(self.bot, ctx, self.bot.stringstack["NoPermissionWith"].format(self.bot.stringstack["Permission"]["ManageChannels"])))
		else :
			e = embed_t(self.bot, ctx, self.bot.stringstack["Warning"], self.bot.stringstack["ActionCannotUndo"])
			if await waitReactionRequired(ctx, self.bot, ['\N{HEAVY CHECK MARK}','\N{BALLOT BOX WITH CHECK}','\N{WHITE HEAVY CHECK MARK}'], ctx.author.id, e) :
				for ch in ctx.message.guild.channels :
					await ch.delete(reason=self.bot.stringstack["Reason"]["CommandBy"].format(ctx.author))

	@commands.command()
	@IsOwnerGuild()
	async def nuke__messages(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)
		if not ctx.message.guild.me.guild_permissions.manage_messages :
			await ctx.send(embed=embed_em(self.bot, ctx, self.bot.stringstack["NoPermissionWith"].format(self.bot.stringstack["Permission"]["ManageMessages"])))
		else :
			e = embed_t(self.bot, ctx, self.bot.stringstack["Warning"], self.bot.stringstack["ActionCannotUndo"])
			if await waitReactionRequired(ctx, self.bot, ['\N{HEAVY CHECK MARK}','\N{BALLOT BOX WITH CHECK}','\N{WHITE HEAVY CHECK MARK}'], ctx.author.id, e) :
				msgs = []
				while len(await ctx.message.channel.history(limit=300).flatten()) > 0 :
					async for m in ctx.message.channel.history(limit=300) :
						msgs.append(m)
					await ctx.message.channel.delete_messages(msgs)
def setup(bot) :
	bot.add_cog(loadInformation(Nuke(bot)))
