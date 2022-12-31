from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Ping$")
async def ping(event):
    await event.edit(client.get_string("Ping").format(client.me.id))
