from FidoSelf import client
from telethon import functions

@client.Command(onlysudo=False, alowedits=False)
async def lockepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("LOCK_PV") or "off"
    if mode == "on":
        await client(functions.contacts.BlockRequest(event.sender_id))