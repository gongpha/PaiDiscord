from discord.ext import commands
from utils.template import embed_em

def IsOwnerBot() :
	async def predicate(ctx) :
		if ctx.author.id not in ctx.bot.owner_list :
			await ctx.send(embed=embed_em(ctx, ctx.bot.stringstack["YouAreNotBotOwner"]))
		return ctx.author.id in ctx.bot.owner_list
	return commands.check(predicate)

def IsOwnerGuild() :
	async def predicate(ctx) :
		return ctx.author.id == ctx.message.guild.owner_id
	return commands.check(predicate)

async def CheckPermission(ctx, permission, string) :
	if not permission :
		await ctx.send(embed=embed_em(ctx, ctx.bot.stringstack["NoPermissionWith"].format(ctx.bot.stringstack["Permission"][string])))
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
