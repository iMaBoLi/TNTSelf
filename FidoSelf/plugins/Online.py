from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Name": "Online",
    "Info": {
        "Help": "To Set Online Mode For Account!",
        "Commands": {
            "{CMD}Online <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(onlysudo=False)
async def online(event):
    mode = client.DB.get_key("ONLINE_MODE") or "OFF"
    if mode == "ON":
        await client(functions.account.UpdateStatusRequest(offline=False))
