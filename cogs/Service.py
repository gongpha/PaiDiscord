import discord
from discord.ext import commands
from utils.cog import Cog, loadInformation

class Service(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	@commands.command()
	async def my_cmd_count(self, ctx) :
		await ctx.send(ctx.bot.ss("DeprecatedCommand").format(c))
		# result = await AnyModel_FindUserOrMember(ctx, obj or ctx.author)
		# 	async with ctx.message.channel.typing() :
		# 		r = await ctx.bot.db.get_profile(result, ['commands'])
		# 		if r = False :
		# 			await ctx.bot.db.insert_profile(result)
		# 			await ctx.bot.db.increase_cmd_count(result)
		# 			c = 1
		# 		else :
		# 			c = r['commands']
		# 		await ctx.send(self.ss("YouUsedCount").format(c))
async def setup(bot) :
	await bot.add_cog(await loadInformation(Service(bot)))
