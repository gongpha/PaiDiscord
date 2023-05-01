# from anyuser import anyuser_convert
import discord
import re
from discord.utils import *
from utils.template import embed_em
# # tob = {
# # 	discord.User = 'user',
# # 	discord.Member = 'member',
# # 	discord.Message = 'message',
# # 	discord.Guild = 'guild',
# # 	discord.TextChannel = 'textchannel'
# # }
#
# async def anymodel_convert(ctx, object) :
# 	result = None
# 	result, passed = await anyuser_convert(ctx, object)
# 	string = tob.get(type(result))
# 	if passed < 0 :
# 		result = await fetch_channel(object)

def _get_from_guilds(bot, getter, argument) :
	result = None
	for guild in bot.guilds :
		result = getattr(guild, getter)(argument)
		if result:
			return result
	return result

class NotFound(Exception) :
	pass

class Forbidden(Exception) :
	pass


class AnyConverter :
	async def convert(self, ctx, object) :
		raise NotImplementedError('Derived classes need to implement this.')

class AnyID(AnyConverter) :
	def __init__(self) :
		self._id_regex = re.compile(r'([0-9]+)$')
		super().__init__()

	def _get_id_match(self, object) :
		return self._id_regex.match(object)

class AnyUser(AnyID) :
	async def convert(self, ctx, object, external = True) :
		match = self._get_id_match(object) or re.match(r'<@!?([0-9]+)>$', object)
		result = None
		state = ctx._state

		if match is not None :
			user_id = int(match.group(1))
			result = ctx.bot.get_user(user_id)
		else:
			arg = object
			# check for discriminator if it exists
			if len(arg) > 5 and arg[-5] == '#' :
				discrim = arg[-4:]
				name = arg[:-5]
				predicate = lambda u: u.name == name and u.discriminator == discrim
				result = discord.utils.find(predicate, state._users.values())
				if result is not None:
					return result

			predicate = lambda u: u.name == arg
			result = discord.utils.find(predicate, state._users.values())
		if result is None :
			if external :
				try :
					result = await ctx.bot.fetch_user(user_id)
				except discord.NotFound :
					raise NotFound('User "{}" not found. While finding on external'.format(object))
				except discord.Forbidden :
					raise Forbidden('Cannot get info of "{}"'.format(object))
			else :
				raise NotFound('User "{}" not found'.format(object))

		return result

class AnyMember(AnyID) :
	async def convert(self, ctx, object, in_ctx_guild = True) :
		bot = ctx.bot
		match = self._get_id_match(object) or re.match(r'<@!?([0-9]+)>$', object)
		result = None
		if in_ctx_guild and isinstance(ctx.message.channel, discord.TextChannel) :
			guild = ctx.guild
			if match is None :
				result = guild.get_member_named(object)
			else :
				result = guild.get_member(int(match.group(1)))
			if not result :
				for m in guild.members :
					if str(object).lower() in (m.nick or "").lower() :
						result = m
					else :
						if str(object).lower() in m.name.lower() :
							result = m
		else :
			if not isinstance(ctx.message.channel, discord.TextChannel) :
				raise NotFound('No Guild in non-TextChannel')
			if match is None :
				for guild in bot.guilds :
					result = guild.get_member_named(object)
			else :
				user_id = int(match.group(1))
				for guild in bot.guilds :
					result = guild.get_member(user_id)

		if result is None :
			raise NotFound('Member "{}" not found'.format(object))


		return result

async def AnyModel__MemberOrUser(ctx, object, external=True, in_ctx_guild=True) :
	if isinstance(object, (discord.Member, discord.User)) :
		return object
	if not object :
		return None
	try :
		return await AnyMember().convert(ctx, object, in_ctx_guild)
	except NotFound :
		try :
			return await AnyUser().convert(ctx, object, external)
		except NotFound :
			raise NotFound('Member or User "{}" not found'.format(object))
		except Forbidden :
			raise Forbidden('Cannot get info of "{}"'.format(object))

async def AnyModel__MemberOrUser_Optional(ctx, object, external=True, in_ctx_guild=True) :
	try :
		return await AnyModel__MemberOrUser(ctx, object, external, in_ctx_guild)
	except :
		return None

async def AnyModel_FindUserOrMember(ctx, object, external=True, in_ctx_guild=True) :
	r = await AnyModel__MemberOrUser_Optional(ctx, object, external, in_ctx_guild)
	if not r :
		err = embed_em(ctx, ctx.bot.ss("ObjectNotFoundFromObject").format(ctx.bot.ss("Model", "User"), str(object)))
		#err.description = "```{}```".format(result.text)
		await ctx.send(embed=err)
		return None
	return r
