from FidoSelf import client
from datetime import datetime
import aiocron
import asyncio

@aiocron.crontab("*/1 * * * *")
async def Avkeys():
    time = datetime.now().strftime("%H:%M")
    if str(time) == "19:30":
        await client.send_message("Avkeys_Group", "Avkeys")
    elif (int(str(time).split(":")[1]) % 5) == 0:
        await client.bot.send_message("TheaBoLi", f"This is Worked!\n\nTime: {time}")

Avkeys.start()
