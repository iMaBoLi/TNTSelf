from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}AddEcho ?(.*)?")
async def addecho(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    echos = client.DB.get_key("ECHOS") or []
    info = await client.get_entity(event.userid)
    if event.userid in echos:
        return await event.edit(client.get_string("Echo_1").format(client.mention(info)))
    echos.append(event.userid)
    client.DB.set_key("ECHOS", echos)
    await event.edit(client.get_string("Echo_2").format(client.mention(info)))
    
@client.Command(pattern=f"(?i)^\{client.cmd}DelEcho ?(.*)?")
async def delecho(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UUP"))
    echos = client.DB.get_key("ECHOS") or []
    info = await client.get_entity(event.userid)
    if event.userid not in echos:
        return await event.edit(client.get_string("Echo_3").format(client.mention(info)))  
    echos.remove(event.userid)
    client.DB.set_key("ECHOS", echos)
    await event.edit(client.get_string("Echo_4").format(client.mention(info)))
    
@client.Command(pattern=f"(?i)^\{client.cmd}EchoList$")
async def echolist(event):
    await event.edit(client.get_string("Wait"))
    echos = client.DB.get_key("ECHOS") or []
    if not echos:
        return await event.edit(client.get_string("Echo_5"))
    text = client.get_string("Echo_6")
    row = 1
    for echo in echos:
        text += f"**{row} -** `{echo}`\n"
        row += 1
    await event.edit(text)

@client.Command(pattern=f"(?i)^\{client.cmd}CleanEchoList$")
async def cleanecholist(event):
    await event.edit(client.get_string("Wait"))
    echos = client.DB.get_key("ECHOS") or []
    if not echos:
        return await event.edit(client.get_string("Echo_5"))
    client.DB.del_key("ECHOS")
    await event.edit(client.get_string("Echo_7"))

@client.Command(sudo=False, edits=False)
async def echo(event):
    echos = client.DB.get_key("ECHOS") or []
    if event.sender_id in echos:
        message = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(message)
