import discord
from discord.ext import commands
from utils.cog import Cog, loadInformation

class Music(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def join(self, ctx, *, channel : discord.VoiceChannel) :
		if ctx.voice_client is not None :
			return await ctx.voice_client.move_to(channel)

		await channel.connect()

def setup(bot) :
	bot.add_cog(loadInformation(Music(bot)))
