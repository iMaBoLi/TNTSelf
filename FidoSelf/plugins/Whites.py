from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}AddWhite ?(.*)?")
async def addwhite(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    whites = client.DB.get_key("WHITES") or []
    info = await client.get_entity(event.userid)
    if event.userid in whites:
        return await event.edit(client.get_string("Whites_1").format(client.mention(info)))
    whites.append(event.userid)
    client.DB.set_key("WHITES", whites)
    blacks = client.DB.get_key("BLACKS") or []
    if event.userid in blacks:
        blacks.remove(event.userid)
        client.DB.set_key("BLACKS", blacks)
    await event.edit(client.get_string("Whites_2").format(client.mention(info)))
    
@client.Command(pattern=f"(?i)^\{client.cmd}DelWhite ?(.*)?")
async def delwhite(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    whites = client.DB.get_key("WHITES") or []
    info = await client.get_entity(event.userid)
    if event.userid not in whites:
        return await event.edit(client.get_string("Whites_3").format(client.mention(info)))  
    whites.remove(event.userid)
    client.DB.set_key("WHITES", whites)
    await event.edit(client.get_string("Whites_4").format(client.mention(info)))
    
@client.Command(pattern=f"(?i)^\{client.cmd}WhiteList$")
async def whitelist(event):
    await event.edit(client.get_string("Wait"))
    whites = client.DB.get_key("WHITES") or []
    if not whites:
        return await event.edit(client.get_string("Whites_5"))
    text = client.get_string("Whites_6")
    row = 1
    for white in whites:
        text += f"**{row} -** `{white}`\n"
        row += 1
    await event.edit(text)

@client.Command(pattern=f"(?i)^\{client.cmd}CleanWhiteList$")
async def cleanwhitelist(event):
    await event.edit(client.get_string("Wait"))
    whites = client.DB.get_key("WHITES") or []
    if not whites:
        return await event.edit(client.get_string("Whites_5"))
    client.DB.del_key("WHITES")
    await event.edit(client.get_string("Whites_7"))
