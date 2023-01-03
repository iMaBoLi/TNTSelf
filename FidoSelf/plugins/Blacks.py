from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddBlack ?(.*)?")
async def addblack(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    blacks = client.DB.get_key("BLACKS") or []
    info = await client.get_entity(event.userid)
    if event.userid in blacks:
        return await event.edit(client.get_string("Blacks_1").format(client.mention(info))
    blacks.append(event.userid)
    client.DB.set_key("BLACKS", blacks)
    await event.edit(client.get_string("Black_2").format(client.mention(info))
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}DelBlack ?(.*)?")
async def delblack(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    blacks = client.DB.get_key("BLACKS") or []
    info = await client.get_entity(event.userid)
    if event.userid not in blacks:
        return await event.edit(client.get_string("Black_3").format(client.mention(info))  
    blacks.remove(event.userid)
    client.DB.set_key("BLACKS", blacks)
    await event.edit(client.get_string("Black_4").format(client.mention(info))
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}BlackList$")
async def blacklist(event):
    await event.edit(client.get_string("Wait"))
    blacks = client.DB.get_key("BLACKS") or []
    if not blacks:
        return await event.edit(client.get_string("Blacks_5"))
    text = client.get_string("Blacks_6")
    row = 1
    for black in blacks:
        text += f"**{row} -** `{black}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanBlackList$")
async def cleanblacklist(event):
    await event.edit(client.get_string("Wait"))
    blacks = client.DB.get_key("BLACKS") or []
    if not blacks:
        return await event.edit(client.get_string("Blacks_5"))
    client.DB.del_key("BLACKS")
    await event.edit(client.get_string("Blacks_7"))
