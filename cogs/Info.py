import discord
import platform
from discord.ext import commands
import typing
from io import BytesIO
from utils.cog import Cog, loadInformation
from utils.template import embed_t, embed_em, embed_wm, model_info, convert_size, format_date_timediff_short, format_date_timediff, local_strftime, get_time_format
from pytz import timezone
from dateutil.relativedelta import relativedelta
#from utils.anyuser import anyuser_safecheck, anyuser_convert
from utils.anymodel import AnyModel_FindUserOrMember
from utils.anyemoji import anyemoji_convert
from utils.check import *

import datetime
import math
import psutil

def progressbar(iteration, total, length = 10):
	filledLength = int(length * iteration // total)
	bar = '●' * filledLength + '○' * (length - filledLength)
	return bar

class Info(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	def help_overview_embed(self, ctx) :
		h = embed_t(ctx, "❔ {}".format(self.ss("Help")), casesensitive=True)
		#if isinstance(self.bot.theme, (list, tuple)) :
		#	h.color = self.bot.theme[1] if len(self.bot.theme) > 1 else self.bot.theme[0]
		#else :
		#	h.color = self.bot.theme
		for n, c in self.bot.cogs.items() :
			if not c.cog_hidden :
				h.add_field(name="{} {}".format(" ".join(c.cog_emoji or [":x:"]), c.cog_name or c.cog_class),value=f"`{ctx.bot.cmdprefix}{ctx.command.name} {c.qualified_name}`",inline=True) # +"\n".join([f"`{self.bot.command_prefix}{i} {c.qualified_name}`" for i in ctx.command.aliases])
		return h

	def help_specific_embed(self, ctx, cog) :
		h = embed_t(ctx, "{} {}".format(" ".join(cog.cog_emoji or [":x:"]), cog.cog_name or cog.cog_class), cog.cog_desc, casesensitive=True)
		def a() :
			h.add_field(name="`{}{}`".format(ctx.bot.cmdprefix, c.name),value=(c.description or "").format(ctx.bot) or ctx.bot.ss("NoDescription"),inline=True)
		for c in cog.get_commands() :
			if (c.name.startswith('_')) :
				if (ctx.author.id in ctx.bot.owners) :
					a()
			elif (not c.hidden) or (ctx.author.id not in ctx.bot.owners) :
				a()
			#h.add_field(name="`{}{}` {}".format(self.bot.command_prefix, c.name, "📡" if c.sql else ""),value=c.description.format(ctx.bot) or ctx.bot.ss("Empty"],inline=True)
		if h.fields == None :
			h.add_field(name="﻿",value="*{}*".format(self.bot.ss("NoCommand")))
		return h

	def help_command_embed(self, ctx, command, cog) :
		h = embed_t(ctx, "{}**{}**    ({} {})".format(ctx.bot.cmdprefix, command.name, " ".join(cog.cog_emoji or [":x:"]), cog.cog_name or cog.cog_class), ((command.description) or "") + ("\n\n`{}{} {}`".format(self.bot.cmdprefix, command.name, command.usage or "")))
		#if command.sql :
		#	h.description += "\n📡 **{}**".format(self.bot.ss("CommandNeedQuery"])
		return h

	async def profile_information(self, ctx, object) :
		r = await ctx.bot.db.get_profile(object, ['credits', 'commands', 'username'])
		if r != False :
			await ctx.bot.db.update_profile_record(object)
		if object.bot :
			e = embed_wm(ctx, ctx.bot.ss("CannotUseWithBot"))
		else :
			t = 0
			if r == False :
				try :
					fromid = ctx.message.guild.id
				except AttributeError :
					fromid = ctx.message.channel.id
				t = await ctx.bot.db.insert_profile(object)
				r = {
					"result" : {
						"credits" : 0,
						"commands" : 0,
						"username" : object.display_name
					}
				}
			e = embed_t(ctx)
			e.color = object.color if object.color.value != 0 else discord.Color.default()
			e.add_field(name=":credit_card: " + ctx.bot.ss("Model", "Credit"), value=r["result"]["credits"], inline=True)
			e.add_field(name=":arrow_upper_left: " + ctx.bot.ss("CommandUsedCount"), value=r["result"]["commands"], inline=True)
			e.set_author(name=object.display_name or object.name, icon_url=object.display_avatar.url)
			e.set_footer(text=str(object.id))

		return e

	@commands.command()
	async def help(self, ctx, *sect : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		e = None
		h = None
		ov = False
		if not sect :
			ov = True
			h = self.help_overview_embed(ctx)
			e = embed_t(ctx, description=self.bot.bot_description)
			#e.color = self.bot.theme[0] if isinstance(self.bot.theme,(list,tuple)) else self.bot.theme
			e.set_author(name=self.bot.bot_name, icon_url=self.bot.user.display_avatar.url)
			e.set_footer(text="Build " + str(self.bot.build_number) + " • " + (local_strftime(ctx, self.bot.build_date, get_time_format(ctx)) if self.bot.build_date else ""))
		else :
			for n, c in self.bot.cogs.items() :
				#print(n)
				if n == sect[0] :
					h = self.help_specific_embed(ctx, c)
			if h == None :
				for n, cg in self.bot.cogs.items() :
					for c in cg.get_commands() :
						c_a = c.aliases.copy()
						c_a.insert(0, c.name)
						if sect[0] in c_a :
							h = self.help_command_embed(ctx, c, cg)
							break

		www = discord.Embed()
		www.color = 0xFF0000
		www.description = self.bot.ss('PrivateWarning').format("gongpha#0238")

		if e != None :
			await ctx.send(embed=e)

		if h != None :
			await ctx.send(embed=h)
		if ov :
			await ctx.send(embed=www)


	@commands.command()
	async def stats(self, ctx) :
		e = embed_t(ctx, self.bot.ss("StatsOf").format(ctx.bot.bot_name))
		e.set_author(name=ctx.bot.bot_name, icon_url=self.bot.user.display_avatar.url)
		#e.set_thumbnail(url=(await ctx.bot.application_info()).icon_url)
		s = "**{}** : {}\n"
		e.description += s.format(self.bot.ss("Model", "Name"), ctx.bot.user)
		e.description += s.format(self.bot.ss("Model", "BotName"), ctx.bot.bot_name)
		e.description += s.format(self.bot.ss("Model", "ID"), ctx.bot.user.id)
		e.description += s.format(self.bot.ss("Model", "Discriminator"), ctx.bot.user.discriminator)
		m_t = psutil.virtual_memory()[3]
		m_a = psutil.virtual_memory()[0]
		mm_t = convert_size(m_t)
		mm_a = convert_size(m_a)
		e.description += s.format(self.bot.ss("Model", "Memory"), self.bot.ss("PercentUsagedFrom").format(str(psutil.virtual_memory()[2]), "[{} / {}] | {}".format(mm_t, mm_a, progressbar(m_t, m_a))))
		cpu = psutil.cpu_percent()
		e.description += s.format(self.bot.ss("Model", "CPU"), self.bot.ss("PercentUsagedNewLine").format(str(cpu), progressbar(cpu, 100)))
		e.description += s.format(self.bot.ss("SystemUpTime"), format_date_timediff(ctx, self.bot.start_time))
		e.description += s.format(self.bot.ss("Model", "Ping"), str(round(ctx.bot.ws.latency * 1000)) + " ms")










		# SET YOUR STATE HERE
		#public_now = False

		#if ctx.author.id in ctx.bot.owner_list :
		#	public_now = True
		mm = 0
		tc = 0
		vc = 0
		ca = 0
		rr = 0
		for guild in ctx.bot.guilds :
			mm += len(guild.members)
			tc += len(guild.text_channels)
			vc += len(guild.voice_channels)
			ca += len(guild.categories)
			rr += len(guild.roles)
		#pe = e.copy()
		e.description += "\n"
		e.description += s.format(self.bot.ss("Model", "Emoji"), len(ctx.bot.emojis))
		e.description += s.format(self.bot.ss("Model", "CacheMessage"), len(ctx.bot.cached_messages))
		e.description += s.format(self.bot.ss("Model", "VoiceClient"), len(ctx.bot.voice_clients))
		e.description += s.format(self.bot.ss("Model", "User"), len(ctx.bot.users))
		e.description += s.format(self.bot.ss("Model", "Member"), mm)
		e.description += s.format(self.bot.ss("Model", "Channel"), tc + vc)
		e.description += s.format(self.bot.ss("Model", "TextChannel"), tc)
		e.description += s.format(self.bot.ss("Model", "VoiceChannel"), vc)
		e.description += s.format(self.bot.ss("Model", "Category"), ca)
		e.description += s.format(self.bot.ss("Model", "Role"), rr)
		e.description += s.format(self.bot.ss("Model", "Guild"), len(ctx.bot.guilds))

		e.add_field(name=self.bot.ss("Model", "Invite"), value="[{}]({})".format(self.bot.ss("ClickHere"), ctx.bot.static_invite), inline=True)

		e.set_footer(text="Python {} • discord.py {}".format(platform.python_version(), discord.__version__))
		await ctx.send(embed=e)
		#e.set_footer(text=)
		#th_format_date_diff(guild.created_at.astimezone(timezone(self.bot.timezone)))

	@commands.command()
	async def alias(self, ctx, *, sect : str) :
		#print(self.bot.name)
		#print(self.bot.description)
		h = None
		for c in list(self.bot.commands) :
			c_a = c.aliases.copy()
			c_a.insert(0, c.name)
			if sect in c_a :
				h = embed_t(ctx, "{} {} ({})".format(self.ss("AliasFor"), sect, c.name) if sect != c.name else "{} {}".format(self.ss("AliasFor"), sect), self.ss("YouCanCallAliasesInstead"))
				h.add_field(name=self.bot.ss("Model", "Command"), value=f"`{c.name}`")
				h.add_field(name=self.bot.ss("Model", "Alias"), value="\n".join([f"`{i}`" for i in c.aliases]))
				break
		if h != None :
			await ctx.send(embed=h)

	@commands.command()
	async def guild(self, ctx, guild_id : int = 0) :
		if guild_id != 0 :
			guild = ctx.bot.get_guild(guild_id)
		else :
			guild = ctx.message.guild

		if not guild :
			await ctx.send(embed=
				embed_em(ctx, ctx.bot.ss("BotNotInGuild"))
			)
			return
		
		# check if the sender is joined that guild
		member = guild.get_member(ctx.author.id)
		if not member :
			await ctx.send(embed=
				embed_em(ctx, ctx.bot.ss("ObjectNotFoundFromObject").format(ctx.bot.ss("Model", "Guild"), str(guild.id)))
			)
			return
		
		# check if it's in the same guildd
		if ctx.guild :
			if ctx.guild != guild :
				await ctx.send(ctx.bot.ss("CheckDMDueToPrivacy"))
				await ctx.author.send(embed=model_info(ctx, guild))
				await ctx.author.send(ctx.bot.ss("BackToCommandMessage").format(ctx.message.jump_url))
				return

		await ctx.send(embed=model_info(ctx, guild))

	@commands.command()
	async def avatar(self, ctx, *, obj = None) :
		member = await AnyModel_FindUserOrMember(ctx, obj or ctx.author)
		if member :
			url = member.display_avatar.url
			await ctx.send("`{}`\n{}".format(member, url))

	@commands.command()
	async def avatar_permanent(self, ctx, *, obj = None) :
		member = await AnyModel_FindUserOrMember(ctx, obj or ctx.author)
		if member :
			file = discord.File(fp=BytesIO(await member.display_avatar.read()), filename="pai__avatar_{}-168d{}.{}".format(member.display_name, member.id, "gif" if member.display_avatar.is_animated() else "png"))
			# PAI FEATURE ONLY
			if (member.id == 473457863822409728 or member.id == 457908707817422860) and ctx.bot.hd_avatar_url :
				await ctx.send("{}\n{}".format(ctx.bot.ss('WantToSeeHDBotAvatar').format(ctx.bot.bot_name), ctx.bot.ss('TryTypingCmd').format(f"{ctx.bot.cmdprefix}pai_avatar")), file=file)
			else :
				await ctx.send("`{}`".format(member), file=file)

	@commands.command()
	async def icon(self, ctx) :
		guild = ctx.guild
		if guild :
			url = guild.icon
			await ctx.send("`{}`\n{}".format(guild, url))

	@commands.command()
	async def icon_permanent(self, ctx) :
		guild = ctx.guild
		if guild :
			file = discord.File(fp=BytesIO(await guild.icon.read()), filename="pai__icon_{}-168d{}.{}".format(guild.name, guild.id, "gif" if guild.icon.is_animated() else "png"))
			await ctx.send("`{}`".format(guild), file=file)

	@commands.command()
	async def anyuser(self, ctx, *, obj = None) :
		result = await AnyModel_FindUserOrMember(ctx, obj or ctx.author)
		if result :
			await ctx.send(embed=model_info(ctx, result))

	#@commands.command()
	#async def profile(self, ctx, *, obj = None) :
	#	result = await AnyModel_FindUserOrMember(ctx, obj or ctx.author)
	#	async with ctx.message.channel.typing() :
	#		ee = await self.profile_information(ctx,result or ctx.author)
	#		await ctx.send(embed=ee)

	@commands.command()
	async def ping(self, ctx) :
		await ctx.send(self.bot.ss("PingReturnedSec").format(ctx.bot.latency))

	@commands.command()
	async def emoji(self, ctx, emoji_text) :
		emoji, passed = await anyemoji_convert(ctx, emoji_text)
		if passed == -1 :
			err = embed_em(ctx, ctx.bot.ss("ObjectNotFoundFromObject").format(ctx.bot.ss("Model", "Emoji"), emoji_text))
			#err.description = "```{}```".format(result.text)
			await ctx.send(embed=err)
			return

		b = emoji[0]
		if passed == 0 :
			etext = ""

			f = "{}__emoticon_{}.png".format(ctx.bot.bot_name.lower(), "-".join([format(ord(e), 'x') for e in emoji_text]))
		else :
			emoji = emoji[1]
			if passed == 4 :
				f = "{}__emoticon_{}{}-174d{}.{}".format(ctx.bot.bot_name.lower(), "animated_" if emoji.animated else "", emoji.name, emoji.id, "gif" if emoji.animated else "png")
			elif passed < 4 :
				try :
					u = emoji.user
					uid = emoji.user.id
					f = "{}__emoticon_{}{}-174d{}_{}-168d{}_{}-169d{}.{}".format(ctx.bot.bot_name.lower(), "animated_" if emoji.animated else "", emoji.name, emoji.id, u, uid, emoji.guild_id, emoji.guild.name, "gif" if emoji.animated else "png")
				except :
					f = "{}__emoticon_{}{}-174d{}.{}".format(ctx.bot.bot_name.lower(), "animated_" if emoji.animated else "", emoji.name, emoji.id, "gif" if emoji.animated else "png")
			else :
				f = "{}__emoticon".format(ctx.bot.bot_name.lower())

		file = discord.File(fp=b, filename=f)
		await ctx.send(file=file)

	@commands.command()
	async def invite(self, ctx) :
		await ctx.send(embed=embed_t(ctx, ctx.bot.ss('BotInviteLink'), "[{}]({})".format(ctx.bot.ss("ClickHere"), ctx.bot.static_invite)))

	@discord.app_commands.command(name="global", description="Global command test")
	async def global_command(self, interaction: discord.Interaction) :
		await interaction.response.send_message(f'Hello !', ephemeral=False)

async def setup(bot) :
	await bot.add_cog(await loadInformation(Info(bot)))
