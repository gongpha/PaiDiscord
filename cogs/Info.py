import discord
from discord.ext import commands
import typing
from cog import Cog
from cog import loadInformation

class Info(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	def help_overview_embed(self, ctx) :
		h = discord.Embed()
		h.color = self.bot.theme
		h.description = self.bot.stringstack["bot_description"]
		h.set_footer(text=self.bot.stringstack["request_by"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
		h.set_author(name=self.bot.stringstack["bot_name"], icon_url=self.bot.user.avatar_url)
		for n, c in self.bot.cogs.items() :
			h.add_field(name=c.cog_name,value=f"`{self.bot.command_prefix}help {c.qualified_name}`",inline=True)
		return h

	def help_specific_embed(self, ctx, cog) :
		h = discord.Embed()
		h.color = self.bot.theme
		h.description = self.cog_desc
		h.set_footer(text=self.bot.stringstack["request_by"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
		h.title = self.cog_name
		if not cog.get_commands() :
			h.add_field(name="﻿",value="*{}*".format(self.bot.stringstack["no_command"]))
		for c in cog.get_commands() :
			h.add_field(name=f"`{self.bot.command_prefix}{c.name}`",value=c.description,inline=True)
		return h

	@commands.command()
	async def help(self, ctx, *sect : str) :
		h = None
		if not sect :
			h = self.help_overview_embed(ctx)
		else :
			for n, c in self.bot.cogs.items() :
				if n.lower() == sect[0].lower() :
					h = self.help_specific_embed(ctx, c)

		#msgh.set_thumbnail(url=ctx.author.avatar_url)
		if h != None :
			await ctx.send(embed=h)

def setup(bot) :
	bot.add_cog(loadInformation(Info(bot)))
