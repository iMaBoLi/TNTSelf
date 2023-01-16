from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Save (.*)$")
async def save(event):
    await event.edit(client.get_string("Wait"))
    name = event.pattern_match.group(1)
    if not event.is_reply:
        return await event.edit(client.get_string("ReplyMedia_NotAll"))
    saves = client.DB.get_key("SAVES") or {}
    if name in saves:
        return await event.edit(client.get_string("Save_1").format(name))
    res, info = await event.reply_message.save()
    if not res:
        return await event.edit(info)
    saves.update({name: info})
    client.DB.set_key("SAVES", saves)
    await event.edit(client.get_string("Save_2").format(name))

@client.Cmd(pattern=f"(?i)^\{client.cmd}Del (.*)$")
async def del(event):
    await event.edit(client.get_string("Wait"))
    name = event.pattern_match.group(1)
    saves = client.DB.get_key("SAVES") or {}
    if name not in saves:
        return await event.edit(client.get_string("Save_3").format(name))
    info = saves[name]
    try:
        message = await client.get_messages(info["chat_id"], ids=info["msg_id"])
        await message.delete()
    except:
        pass
    del saves[name]
    client.DB.set_key("SAVES", saves)
    await event.edit(client.get_string("Save_4").format(name))

@client.Cmd(pattern=f"(?i)^\{client.cmd}Get (.*)$")
async def get(event):
    await event.edit(client.get_string("Wait"))
    name = event.pattern_match.group(1)
    saves = client.DB.get_key("SAVES") or {}
    if name not in saves:
        return await event.edit(client.get_string("Save_3").format(name))
    info = saves[name]
    try:
        message = await client.get_messages(info["chat_id"], ids=info["msg_id"])
        await event.respond(message)
        await event.delete()
    except:
        await event.edit(client.get_string("Save_5").format(name))

@client.Cmd(pattern=f"(?i)^\{client.cmd}SaveList$")
async def savelist(event):
    await event.edit(client.get_string("Wait"))
    saves = client.DB.get_key("SAVES") or {}
    if not saves:
        return await event.edit(client.get_string("Save_6"))
    text = client.get_string("Save_7")
    row = 1
    for save in saves:
        text += f"**{row} -** `{save}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanSaveList$")
async def cleansaves(event):
    await event.edit(client.get_string("Wait"))
    saves = client.DB.get_key("SAVES") or {}
    if not saves:
        return await event.edit(client.get_string("Save_8"))
    for save in saves:
        info = saves[save]
        try:
            message = await client.get_messages(info["chat_id"], ids=info["msg_id"])
            await message.delete()
        except:
            pass
    client.DB.del_key("SAVES")
    await event.edit(client.get_string("Save_9"))
