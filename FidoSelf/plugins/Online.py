from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Plugname": "Online",
    "Pluginfo": {
        "Help": "To Set Online Mode For Account!",
        "Commands": {
            "{CMD}Online <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(onlysudo=False)
async def online(event):
    mode = client.DB.get_key("ONLINE_MODE") or "off"
    if mode == "on":
        await client(functions.account.UpdateStatusRequest(offline=False))
