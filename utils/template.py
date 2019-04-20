import discord

def embed_t(bot, ctx, title, description) :
	e = discord.Embed()
	e.color = bot.theme
	e.description = description
	e.title = title
	e.set_footer(text=bot.stringstack["request_by"].format(ctx.author), icon_url=ctx.message.author.avatar_url)

	return e
