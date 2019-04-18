import os
import asyncio, discord
import platform
from discord.ext import commands

class Pramual(commands.Bot) :
	def __init__(self, *args, **kwargs) :
		command_prefix = kwargs.pop('command_prefix', commands.when_mentioned_or('::'))
		self.loop = kwargs.pop('loop', asyncio.get_event_loop())
		self.std = kwargs.pop('std', None)
		self.token = os.environ.get(self.std,None) if self.std != None else None
		self.log_channel_id = kwargs.pop('log_ch', None)
		self.theme = kwargs.pop('theme', 0x9B59B6)
		if self.token == None :
			raise NoToken("Invalid Token")
		super().__init__(command_prefix=command_prefix, *args, **kwargs)

	async def on_ready(self) :
		print(f'>> Login As "{self.user.name}" ({self.user.id})')
		print(f'>> Mode   : "{self.std}"')
		print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

		self.log_channel = super().get_channel(self.log_channel_id)

	def run_bot(self) :
		super().run(self.token)

	async def on_command(self, ctx):
		e = discord.Embed(title=f"Command : `{self.command_prefix}{ctx.command.name}`")
		e.description = f"Called to `{self.std}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n```" + ctx.message.clean_content + "```", inline=False)
		e.color = self.theme
		e.timestamp = ctx.message.created_at
		await self.log_channel.send(embed=e)
