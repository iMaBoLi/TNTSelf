from FidoSelf import client
from telethon import functions
import aiocron

__INFO__ = {
    "Category": "Setting",
    "Name": "Online",
    "Info": {
        "Help": "To Setting Online Status For Account!",
        "Commands": {
            "{CMD}Online <On-Off>": {
                "Help": "To Turn On-Off Online Mode",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

@aiocron.crontab("*/5 * * * * *")
async def autosender():
    onmode = client.DB.get_key("ONLINE_MODE") or "OFF"
    if onmode == "ON":
        await client(functions.account.UpdateStatusRequest(offline=False))
