import discord
import asyncio
import random
def embed_t(bot, ctx, title, description) :
	e = discord.Embed()
	e.color = int(random.choice(bot.theme))
	e.description = description
	e.title = title
	e.set_footer(text=bot.stringstack["RequestBy"].format(ctx.author.display_name), icon_url=ctx.message.author.avatar_url)

	return e

def embed_em(bot, ctx, reason) :
	e = discord.Embed()
	e.color = 0xFF0000
	e.title = "❌ {}".format(reason)
	e.set_footer(text=bot.stringstack["RequestBy"].format(ctx.author), icon_url=ctx.message.author.avatar_url)
	return e

async def waitReactionRequired(ctx, bot, give, ruser, embed) :
	e = embed.copy()
	e.add_field(name=bot.stringstack["PleaseReactionAllCommander"],value=bot.stringstack["Empty"])
	msg = await ctx.send(embed=e)
	for em in give :
		#await ctx.send(em.encode('unicode-escape').decode('ASCII'))
		await msg.add_reaction(emoji=em)
	added = []
	def check(reaction, user) :
		if user.id == ruser :
			return str(reaction.emoji) in give and str(reaction.emoji) not in added
	yes = False
	while not yes :
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			e.clear_fields()
			e.add_field(name=bot.stringstack["PleaseReactionAllCommander"],value=bot.stringstack["TimeoutWaitingReaction"])
			await msg.edit(embed=e)
			await msg.clear_reactions()
			return False
		else:
			e.clear_fields()
			added.append(str(reaction.emoji))
			e.add_field(name=bot.stringstack["PleaseReactionAllCommander"],value=" ".join(added))
			if set(added) == set(give) :
				return True
			await msg.edit(embed=e)
