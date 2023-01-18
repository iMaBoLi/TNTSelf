from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}(Ping|Bot|Self)$")
async def ping(event):
    await event.edit(client.get_string("Ping"))
