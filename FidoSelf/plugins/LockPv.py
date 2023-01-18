from FidoSelf import client
from telethon import functions

@client.Command(pattern=f"(?i)^\{client.cmd}LockPv (On|Off)$")
async def lockpv(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("LOCK_PV", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("LockPv_1").format(change))

@client.Command(sudo=False, edits=False)
async def locker(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("LOCK_PV") or "off"
    if mode == "on":
        await client(functions.contacts.BlockRequest(event.sender_id))
