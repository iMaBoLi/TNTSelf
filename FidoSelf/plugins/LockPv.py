from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Private",
    "Plugname": "LockPv",
    "Pluginfo": {
        "Help": "To Lock Pv And Block Users In Pv!",
        "Commands": {
            "{CMD}LockPv <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(onlysudo=False, alowedits=False)
async def lockepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("LOCK_PV") or "off"
    if mode == "on":
        await client(functions.contacts.BlockRequest(event.sender_id))