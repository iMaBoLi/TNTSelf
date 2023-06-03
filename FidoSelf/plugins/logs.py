from FidoSelf import client
import os

@client.Command("log")
async def logs(event):
    if os.path.exists("Fido.log"):
        await event.respond("**The Console Logs File!**", file="Fido.log")
        await event.delete()
    else:
        await event.edit("**The Log File Is Not Available!**")
