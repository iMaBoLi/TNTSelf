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

STRINGS = {
    "change": "**The Lock Pv Mode Has Been {}!**",
}
@client.Command(command="LockPv (On|Off)")
async def lockpvmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("LOCK_PV", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(onlysudo=False, alowedits=False)
async def lockepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("LOCK_PV") or "off"
    if mode == "on":
        await client(functions.contacts.BlockRequest(event.sender_id))