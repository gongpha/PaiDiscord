import discord
from discord.ext import commands
from utils.cog import Cog, loadInformation
from utils.template import get_time_format, local_strftime, embed_t, embed_em
from datetime import datetime

stat_url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"

class CovidThailand(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	async def covid_stat(self, ctx, minimal=False) :
		response = await ctx.bot.session.get(stat_url)
		try :
			data = (await response.json())[0]
		except :
			err = embed_em(ctx, self.bot.ss("CannotReceiveDocument"))
			await ctx.send(embed=err)
			return
		curr_datetime = datetime.strptime(data["update_date"], '%Y-%m-%d %H:%M:%S')
		datestr = local_strftime(ctx, curr_datetime, get_time_format(ctx))

		total_hosp = data["total_case"] - data["total_recovered"] - data["total_death"]
		new_hosp = data["new_case"] - data["new_recovered"] - data["new_death"]

		#	DATA1						DATA2					POSITIVE	EMOJI
		dataformat = [
			[data["total_case"],		data["new_case"],		False,		'mask'],
			[data["total_death"],		data["new_death"],		False,		'skull'],
			[data["total_recovered"],	data["new_recovered"],	True,		'sparkling_heart'],
			[total_hosp,				new_hosp,				False,		'hospital'],
		]



		#	0							1						2			3

		# OLD
		#dataformat = {
		#	"case" : ('mask', False),
		#	"death" : ('skull', False),
		#	"new_recovered" : ('sparkling_heart', True),
		#	"Hospitalized" : ('hospital', False)
		#}

		blank_emoji = ctx.bot.get_resource(':black_small_square:', 'Emojis', 'General', 'blank')
		def digits_gen(number, max_length, symbol=False, positive=True) :
			numstr = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
			if symbol :
				resstr = ctx.bot.get_resource("", 'Emojis', 'General', ((("up_green" if number > 0 else "down_red") if positive else ("up_red" if number > 0 else "down_green"))) if number != 0 else "blank")
			else :
				resstr = ""
			number = str(abs(number))
			if len(number) < max_length :
				resstr += blank_emoji * (max_length - len(number))
			for c in number :
				resstr += ':{}:'.format(numstr[int(c)])
			return resstr

		tempstr = ":{}:{}{}"
		await ctx.send(embed=embed_t(ctx, self.ss("title"), description = datestr + "\n\n" + self.ss("ddc_moph"), casesensitive = False))
		final = [tempstr.format(topic[3], blank_emoji + digits_gen(topic[0], max([len(str(abs(c[0]))) for c in dataformat])) + blank_emoji, digits_gen(topic[1], max([len(str(abs(c[1]))) for c in dataformat]), True, topic[2])) for topic in dataformat]
		if minimal :
			await ctx.send("\n".join(final))
		else :
			for f in final :
				await ctx.send(f)

	@commands.command()
	async def covid(self, ctx) :
		is_on_mobile = getattr(ctx.message.author, "is_on_mobile", None)
		if callable(is_on_mobile) :
			await self.covid_stat(ctx, is_on_mobile())
			return
		else :
			await self.covid_stat(ctx)

async def setup(bot) :
	await bot.add_cog(await loadInformation(CovidThailand(bot)))
