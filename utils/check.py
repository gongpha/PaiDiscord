from discord.ext import commands
from discord import DMChannel

def IsOwnerBot() :
	async def predicate(ctx) :
		if ctx.author.id not in ctx.bot.owners :
			raise commands.CheckFailure(ctx.bot.ss("YouAreNotGuildOwner"))
		return True
	return commands.check(predicate)

def IsOwnerGuild() :
	async def predicate(ctx) :
		if ctx.author.id == ctx.message.guild.owner_id :
			raise commands.CheckFailure(ctx.bot.ss("YouAreNotBotOwner"))
		return True
	return commands.check(predicate)

def IsNotDM() :
	async def predicate(ctx) :
		if ctx.guild is False :
			raise commands.NoPrivateMessage()
		return True
	return commands.check(predicate)

def CheckBotGuildPermission(pmstrlist) :
	async def predicate(ctx) :
		if all([getattr(ctx.message.guild.me.guild_permissions, pmstr) for pmstr in pmstrlist]) :
			raise commands.MissingPermissions(pmstrlist)
		return True
	return commands.check(predicate)
