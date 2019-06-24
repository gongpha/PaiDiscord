from discord.ext import commands
from discord import DMChannel
from utils.template import embed_em, embed_wm

def IsOwnerBot() :
	async def predicate(ctx) :
		if ctx.author.id not in ctx.bot.owners :
			await ctx.send(embed=embed_em(ctx, ctx.bot.ss("YouAreNotBotOwner")))
		return ctx.author.id in ctx.bot.owners
	return commands.check(predicate)

def IsOwnerGuild() :
	async def predicate(ctx) :
		if ctx.author.id != ctx.message.guild.owner_id :
			await ctx.send(embed=embed_em(ctx, ctx.bot.ss("YouAreNotGuildOwner")))
		return ctx.author.id == ctx.message.guild.owner_id
	return commands.check(predicate)

def IsNotDM() :
	async def predicate(ctx) :
		if isinstance(ctx.message.channel, DMChannel) :
			await ctx.send(embed=embed_wm(ctx, ctx.bot.ss("CommandInDMNotAvailable")))
		return not isinstance(ctx.message.channel, DMChannel)
	return commands.check(predicate)

async def CheckPermission(ctx, permission, string) :
	if not permission :
		await ctx.send(embed=embed_em(ctx, ctx.bot.ss("NoPermissionWith").format(ctx.bot.ss("Permission", string))))
	return permission

def CanManageMessages() :
	async def predicate(ctx) :
		return await CheckPermission(ctx, ctx.message.guild.me.guild_permissions.manage_channels, "ManageChannels")
	return commands.check(predicate)

def CanManageNicknames() :
	async def predicate(ctx) :
		return await CheckPermission(ctx, ctx.message.guild.me.guild_permissions.manage_nicknames, "ManageNicknames")
	return commands.check(predicate)

def CanManageRoles() :
	async def predicate(ctx) :
		return await CheckPermission(ctx, ctx.message.guild.me.guild_permissions.manage_roles, "ManageRoles")
	return commands.check(predicate)

def CanManageWebhook() :
	async def predicate(ctx) :
		return await CheckPermission(ctx, ctx.message.guild.me.guild_permissions.manage_webhooks, "ManageWebhooks")
	return commands.check(predicate)
