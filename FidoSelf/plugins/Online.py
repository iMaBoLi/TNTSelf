from FidoSelf import client
from telethon import functions

@client.Command(onlysudo=False)
async def online(event):
    mode = client.DB.get_key("ONLINE_MODE") or "off"
    if mode == "on":
        await client(functions.account.UpdateStatusRequest(offline=False))
