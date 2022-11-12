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
	@commands.guild_only()
	@IsOwnerGuild()
	async def nuke__channels(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)
		if not ctx.message.guild.me.guild_permissions.manage_channels :
			await ctx.send(embed=embed_em(ctx, self.bot.ss("NoPermissionWith").format(self.bot.ss("Permission", "ManageChannels"))))
		else :
			e = embed_wm(ctx, self.bot.ss("Warning"), self.bot.ss("ActionCannotUndo"))
			if await waitReactionRequired(ctx, self.bot, ['\N{HEAVY CHECK MARK}','\N{BALLOT BOX WITH CHECK}','\N{WHITE HEAVY CHECK MARK}'], ctx.author.id, e) :
				for ch in ctx.message.guild.channels :
					await ch.delete(reason=self.bot.ss("Reason", "CommandBy").format(ctx.author))

	@commands.command()
	@commands.guild_only()
	@IsOwnerGuild()
	async def nuke__messages(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)
		if not ctx.message.guild.me.guild_permissions.manage_channels :
			await ctx.send(embed=embed_em(ctx, self.bot.ss("NoPermissionWith").format(self.bot.ss("Permission", "ManageChannels"))))
		else :
			e = embed_wm(ctx, self.bot.ss("Warning"), self.bot.ss("ActionCannotUndo"))
			if await waitReactionRequired(ctx, self.bot, ['\N{HEAVY CHECK MARK}','\N{BALLOT BOX WITH CHECK}','\N{WHITE HEAVY CHECK MARK}'], ctx.author.id, e) :
				pos = ctx.channel.position;
				ch = await ctx.channel.clone(reason="CLEANING MESSAGES")
				await ctx.channel.delete(reason="CLEANING MESSAGES")
				await ch.edit(reason="CLEANING MESSAGES", position=pos)

async def setup(bot) :
	await bot.add_cog(await loadInformation(Nuke(bot)))
