import discord
from discord.ext import commands
import typing
from cog import Cog

class Info(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def help(self, ctx, sect : typing.Optional[str] = None) :
		f"""{self.stringstack["help_desc"]}"""
		h = discord.Embed()
		h.color = self.bot.theme
		h.title = self.bot.stringstack["bot_name"]
		h.description = self.bot.stringstack["bot_description"]
		h.set_footer(text = self.bot.stringstack["request_by"].format(ctx.author), icon_url=ctx.message.author.avatar_url)

		for n, c in self.bot.cogs.items() :
			h.add_field(name=c.super().name,value=c.super().description)




		#msgh.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send("", embed=h)

def setup(bot) :
	bot.add_cog(Info(bot))
