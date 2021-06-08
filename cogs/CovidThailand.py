import discord
from discord.ext import commands
from utils.cog import Cog, loadInformation
from utils.template import get_time_format, local_strftime, embed_t, embed_em
from datetime import datetime

stat_url = "https://covid19.th-stat.com/json/covid19v2/getTodayCases.json"

class CovidThailand(Cog) :
	def __init__(self, bot) :
		super().__init__(bot)

	async def covid_stat(self, ctx, minimal=False) :
		response = await ctx.bot.session.get(stat_url + "today")
		try :
			data = await response.json()
		except :
			err = embed_em(ctx, self.bot.ss("CannotReceiveDocument"))
			await ctx.send(embed=err)
			return
		curr_datetime = datetime.strptime(data["UpdateDate"], '%d/%m/%Y %H:%M')
		datestr = local_strftime(ctx, curr_datetime, get_time_format(ctx))

		dataformat = {
			"Confirmed" : ('mask', False),
			"Deaths" : ('skull', False),
			"Recovered" : ('sparkling_heart', True),
			"Hospitalized" : ('hospital', False)
		}

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
		await ctx.send(embed=embed_t(ctx, self.ss("Title"), description = datestr, casesensitive = False))
		final = [tempstr.format(dataformat[topic][0], blank_emoji + digits_gen(data[topic], max([len(str(abs(data[c]))) for c in list(dataformat.keys())])) + blank_emoji, digits_gen(data["New"+topic], max([len(str(abs(data["New"+c]))) for c in list(dataformat.keys())]), True, dataformat[topic][1])) for topic in list(dataformat.keys())]
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

def setup(bot) :
	bot.add_cog(loadInformation(CovidThailand(bot)))
