from discord.ext import commands

def IsOwnerBot(bot) :
	async def predicate(ctx) :
		return ctx.author.id in bot.owner_list
	return commands.check(predicate)

def IsOwnerGuild(bot) :
	async def predicate(ctx) :
		return ctx.author.id == ctx.message.guild.owner_id
	return commands.check(predicate)
