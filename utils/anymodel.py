# from anyuser import anyuser_convert
import discord
from discord.utils import *
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

def _get_from_guilds(bot, getter, argument):
	result = None
	for guild in bot.guilds:
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
		self._id_regex = re.compile(r'([0-9]{15,21})$')
		super().__init__()

	def _get_id_match(self, object) :
		return self._id_regex.match(object)

class AnyUser(AnyID) :
	async def convert(self, ctx, object, external = True) :
		match = self._get_id_match(object) or re.match(r'<@!?([0-9]+)>$', object)
		result = None
		state = ctx._state

		if match is not None:
			user_id = int(match.group(1))
			result = ctx.bot.get_user(user_id)
		else:
			arg = object
			# check for discriminator if it exists
			if len(arg) > 5 and arg[-5] == '#':
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
					raise NotFound('User "{}" not found'.format(object))
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
		if in_ctx_guild :
			guild = ctx.guild
			if match is None :
				# not a mention...
				if guild :
					result = guild.get_member_named(object)
				else :
					result = _get_from_guilds(bot, 'get_member_named', object)
			else :
				user_id = int(match.group(1))
				if guild :
					result = guild.get_member(user_id)
				else :
					result = _get_from_guilds(bot, 'get_member', user_id)
		else :
			if match is None:
				# not a mention...
				for guild in bot.guilds :
					if guild :
						result = guild.get_member_named(object)
					else :
						result = _get_from_guilds(bot, 'get_member_named', object)
			else :
				user_id = int(match.group(1))
				for guild in bot.guilds :
					if guild :
						result = guild.get_member(user_id)
					else:
						result = _get_from_guilds(bot, 'get_member', user_id)

		if result is None :
			raise NotFound('Member "{}" not found'.format(object))


		return result

# class AnyMessage(AnyConverter) :
# 	async def convert(self, ctx, object, destination) :
#
# 		id_regex = re.compile(r'^(?:(?P<channel_id>[0-9]{15,21})-)?(?P<message_id>[0-9]{15,21})$')
# 		link_regex = re.compile(
# 			r'^https?://(?:(ptb|canary)\.)?discordapp\.com/channels/'
# 			r'(?:([0-9]{15,21})|(@me))'
# 			r'/(?P<channel_id>[0-9]{15,21})/(?P<message_id>[0-9]{15,21})/?$'
# 		)
# 		match = id_regex.match(object) or link_regex.match(object)
# 		if not match:
# 			raise NotFound('Message "{msg}" not found'.format(msg=object))
# 		message_id = int(match.group("message_id"))
# 		channel_id = match.group("channel_id")
# 		message = ctx.bot._connection._get_message(message_id)
# 		if message:
# 			return message
# 		if in_ctx_channel :
# 			channel = ctx.bot.get_channel(int(channel_id)) if channel_id else ctx.channel
# 			if not channel :
# 				raise NotFound('Channel "{channel}" not found'.format(channel=channel_id))
# 		else :
# 			m = None
# 			for guild in ctx.bot.guilds :
# 				for channel_ in guild.text_channels :
# 					try :
# 						m = await channel_.fetch_message(message_id)
# 					except : pass
# 			if not m :
# 				raise NotFound('Message "{msg}" not found from all channels'.format(msg=object))
# 		try :
# 			return await channel.fetch_message(message_id)
# 		except discord.NotFound :
# 			raise NotFound('Message "{msg}" not found'.format(msg=object))
# 		except discord.Forbidden :
# 			raise Forbidden("Can't read messages in {channel}".format(channel=channel.mention))


# async def anyuser_convert(ctx, obj) :
# 	passed = 1
# 	result = None
# 	if not obj :
# 		return (ctx.author, 0)
# 	try :
# 		result = await MemberConverter().convert(ctx, obj)
# 	except BadArgument :
# 		passed += 1
# 		try :
# 			result = await UserConverter().convert(ctx, obj)
# 		except BadArgument :
# 			passed += 1
# 			result = ctx.bot.get_user(obj)
# 			if result == None :
# 				passed += 1
# 				try :
# 					result = await ctx.bot.fetch_user(obj)
# 				except discord.NotFound as e :
# 					return (e, -1)
# 				except discord.HTTPException as e:
# 					return (e, -2)
# 	return (result, passed)
