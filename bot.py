# EXPERIMENTAL
# การทดลอง
import asyncio
import sys
import os
import yaml

from pramual import Pramual

def load_yml(filename) :
	with open(filename, encoding="utf8") as f:
		return yaml.safe_load(f)







loop = asyncio.get_event_loop()

bot = Pramual(	info=load_yml('configs/info.yml'),
				channels=load_yml('configs/channels.yml'),
				auths=load_yml('configs/auth.yml'),
				configs=load_yml('configs/configs.yml'),
				max_messages=13213,
				loop=loop)

print("Pramual 2.1")
print("Starting a Task...")
loop.create_task(bot.run_bot())
loop.run_until_complete(loop)
#loop.run_forever()
