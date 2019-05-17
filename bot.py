# EXPERIMENTAL
# การทดลอง
import asyncio
import sys
import os

from pramual import Pramual

loop = asyncio.get_event_loop()

import yaml

with open('configs/proc.yml') as f:
    proclist = yaml.safe_load(f)

for p in proclist["proc_pai" if len(sys.argv) <= 1 else sys.argv[1]] :
    with open('configs/{}.yml'.format(p), encoding="utf8") as f:
        config = yaml.safe_load(f)

databaseHost = os.environ.get((config["info"]["database_host"])[1:], None) if config["info"]["database_host"].startswith('?') else config["info"]["database_host"]
databaseUsername = os.environ.get((config["info"]["database_username"])[1:], None) if config["info"]["database_username"].startswith('?') else config["info"]["database_username"]
databasePassword = os.environ.get((config["info"]["database_password"])[1:], None) if config["info"]["database_password"].startswith('?') else config["info"]["database_password"]
databaseDatabase = os.environ.get((config["info"]["database_database"])[1:], None) if config["info"]["database_database"].startswith('?') else config["info"]["database_database"]
token = os.environ.get((config["info"]["token"])[1:], None) if config["info"]["token"].startswith('?') else config["info"]["token"]

bot_dev = Pramual(name=config["info"]["name"], description=config["info"]["description"], command_prefix=config["info"]["command_prefix"], std=config["info"]["std"], token=token, loop=loop, timezone=config["info"]["timezone"], lang=config["info"]["lang"],log_ch=config["info"]["log_ch"], err_ch=config["info"]["err_ch"], theme=config["info"]["theme"], cog_list=config["cogs"], owner=config["info"]["owner"], databaseHost=databaseHost, databaseUsername=databaseUsername, databasePassword=databasePassword, databaseDatabase=databaseDatabase)

print("Starting a Task... (Experimental)")
loop.create_task(bot_dev.run_bot())
loop.run_until_complete(loop)
loop.run_forever()
