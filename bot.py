# EXPERIMENTAL
# การทดลอง
import asyncio
import sys
import os

from pramual import Pramual, load_yml







loop = asyncio.get_event_loop()

bot = Pramual(	info=load_yml('configs/info.yml', 'configs/base_info.yml'),
				channels=load_yml('configs/channels.yml', 'configs/base_channels.yml'),
				auths=load_yml('configs/auth.yml', 'configs/base_auth.yml'),
				configs=load_yml('configs/configs.yml', 'configs/base_configs.yml'),
				max_messages=13213,
				loop=loop)

print("Pramual 2.1")
print("Starting a Task...")
loop.create_task(bot.run_bot())
loop.run_until_complete(loop)
#loop.run_forever()
