from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Pv",
    "Name": "LockPv",
    "Info": {
        "Help": "To Lock Pv And Block Users In Pv!",
        "Commands": {
            "{CMD}LockPv <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Lock Pv Mode Has Been {}!**",
}
@client.Command(command="LockPv (On|Off)")
async def lockpvmode(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("LOVKPV_MODE", change)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(onlysudo=False, allowedits=False)
async def lockepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("LOVKPV_MODE") or "OFF"
    if mode == "ON":
        await client(functions.contacts.BlockRequest(event.sender_id))