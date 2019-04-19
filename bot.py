# EXPERIMENTAL
# การทดลอง
import asyncio

from pramual import Pramual

loop = asyncio.get_event_loop()

import yaml
with open('configs/proc.yml') as f:
    proclist = yaml.safe_load(f)

for p in proclist["proc_dev"] :
    with open('configs/{}.yml'.format(p), encoding="utf8") as f:
        config = yaml.safe_load(f)

bot_dev = Pramual(name=config["info"]["name"], description=config["info"]["description"], command_prefix=config["info"]["command_prefix"], std=config["info"]["std"], loop=loop, timezone=config["info"]["timezone"], lang=config["info"]["lang"],log_ch=config["info"]["log_ch"], err_ch=config["info"]["err_ch"], theme=config["info"]["theme"], cog_list=config["cogs"])

print("Starting a Task... (Experimental)")
loop.create_task(bot_dev.run_bot())
loop.run_until_complete(loop)
loop.run_forever()
