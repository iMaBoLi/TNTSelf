from FidoSelf import client
from datetime import datetime
import aiocron

@aiocron.crontab("*/1 * * * *")
async def Avkeys():
    time = datetime.now().strftime("%H:%M")
    if str(time) == "21:00":
        await client.send_message("Avkeys_Group", "Avkeys")
    elif str(time) == "20:58":
        await client.send_message("Avkeys_Group", "سلام")
    else:
        await client.bot.send_message("TheaBoLi", f"This Worked!\nTime: {time}")

Avkeys.start()
