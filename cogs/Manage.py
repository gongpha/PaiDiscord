import discord
from discord.ext import commands
import typing
from utils.cog import Cog
import aiohttp
from utils.cog import loadInformation
from utils.template import embed_t
from pytz import timezone
from utils.thai_format import th_format_date_diff
from pythainlp.util import thai_strftime
from dateutil.relativedelta import relativedelta

class Manage(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

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

	@commands.command()
	async def avatar(self, ctx, member : discord.Member = None) :
		member = member or ctx.author
		async with ctx.typeing() :
			await user__avatar[1]
def setup(bot) :
	bot.add_cog(loadInformation(Info(bot)))
