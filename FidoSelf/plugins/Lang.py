from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Set(en|fa)$")
async def language(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("LANGUAGE", mode)
    text = client.get_string("Lang")
    await event.edit(text)
