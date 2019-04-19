# EXPERIMENTAL
# การทดลอง
import asyncio

from pramual import Pramual

loop = asyncio.get_event_loop()

bot_dev = Pramual(command_prefix='>>', std='PramualDev', loop=loop, timezone="Asia/Bangkok", lang="th",log_ch=530055377249894421, err_ch=568682030817345556, theme=0xff7f00)

print("Starting a Task... (Experimental)")
loop.create_task(bot_dev.run_bot())
loop.run_until_complete(task)
loop.run_forever()
