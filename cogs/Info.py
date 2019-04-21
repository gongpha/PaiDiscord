import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import embed_t
from pytz import timezone
from utils.thai_format import th_format_date_diff
from pythainlp.util import thai_strftime
from dateutil.relativedelta import relativedelta

class Info(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	def help_overview_embed(self, ctx) :
		h = embed_t(self.bot, ctx, "", self.bot.bot_description)
		h.set_author(name=self.bot.bot_name, icon_url=self.bot.user.avatar_url)
		for n, c in self.bot.cogs.items() :
			h.add_field(name=":{}: {}".format(c.cog_emoji, c.cog_name),value=f"`{self.bot.command_prefix}{ctx.command.name} {c.qualified_name}`",inline=True) # +"\n".join([f"`{self.bot.command_prefix}{i} {c.qualified_name}`" for i in ctx.command.aliases])
		return h

	def help_specific_embed(self, ctx, cog) :
		h = embed_t(self.bot, ctx, ":{}: {}".format(cog.cog_emoji, cog.cog_name), cog.cog_desc)
		if not cog.get_commands() :
			h.add_field(name="﻿",value="*{}*".format(self.bot.stringstack["NoCommand"]))
		for c in cog.get_commands() :
			h.add_field(name=f"`{self.bot.command_prefix}{c.name}`",value=c.description,inline=True)
		return h

	@commands.command()
	async def help(self, ctx, *sect : str) :
		#print(self.bot.name)
		#print(self.bot.description)
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

	@commands.command()
	async def alias(self, ctx, sect : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		h = None
		for c in list(self.bot.commands) :
			c_a = c.aliases.copy()
			c_a.insert(0, c.name)
			if sect in c_a :
				h = embed_t(self.bot, ctx, "{} {} ({})".format(self.bot.stringstack["Model"]["Command"], sect, c.name) if sect != c.name else "{} {}".format(self.bot.stringstack["Model"]["Command"], sect), "")
				h.add_field(name=self.bot.stringstack["Model"]["Command"], value=f"`{c.name}`")
				h.add_field(name=self.bot.stringstack["Model"]["Alias"], value="\n".join([f"`{i}`" for i in c.aliases]))
				break
		#msgh.set_thumbnail(url=ctx.author.avatar_url)
		if h != None :
			await ctx.send(embed=h)

	@commands.command()
	async def guild(self, ctx) :
		#print(self.bot.name)
		#print(self.bot.description)
		guild = ctx.message.guild
		s = discord.Embed()
		s.color = self.bot.theme
		s.set_thumbnail(url=guild.icon_url)
		s.set_footer(text=self.bot.stringstack["RequestBy"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
		s.title = guild.name
		s.add_field(name=self.bot.stringstack["Model"]["ID"],value=guild.id, inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Region"],value=self.bot.stringstack["VoiceRegion"][guild.region.name], inline=True)
		s.add_field(name=self.bot.stringstack["Model"]["Owner"],value=guild.owner.mention, inline=True)
		s.add_field(name=self.bot.stringstack["CreatedAt"],value=thai_strftime(guild.created_at, self.bot.stringstack["DateTimeText"].format(th_format_date_diff(guild.created_at.astimezone(timezone(self.bot.timezone))))), inline=True)

		await ctx.send(embed=s)
def setup(bot) :
	bot.add_cog(loadInformation(Info(bot)))
