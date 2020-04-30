# EXPERIMENTAL
# การทดลอง
import asyncio
import sys
import os
from datetime import datetime

from pramual import Pramual, load_yml



with open(r'BUILD','r+') as f:
	dat = f.read().split('\n')
	buildnumber = int(dat[0])
	date = datetime.strptime(dat[1], "%Y-%m-%d %H:%M:%S")
	if (os.environ.get('PramualBuildCount', False)) :
		f.seek(0)
		f.write(str(buildnumber + 1))
		f.write('\n')
		f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	buildnumber += 1



loop = asyncio.get_event_loop()

bot = Pramual(	info=load_yml('configs/info.yml', 'configs/base_info.yml'),
				channels=load_yml('configs/channels.yml', 'configs/base_channels.yml'),
				auths=load_yml('configs/auth.yml', 'configs/base_auth.yml'),
				configs=load_yml('configs/configs.yml', 'configs/base_configs.yml'),
				resources=load_yml('configs/resources.yml', 'configs/base_resources.yml'),
				max_messages=13213,
				loop=loop,build_number=buildnumber,build_date=date)

print("Pramual 2.2 : Build", buildnumber)
print("Starting a Task...")
loop.create_task(bot.run_bot())
loop.run_until_complete(loop)
#loop.run_forever()
