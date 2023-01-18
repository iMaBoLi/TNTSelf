from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Save (.*)$")
async def savesaves(event):
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
async def delsaves(event):
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
async def getsaves(event):
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

category = "Tools"
plugin = "Save"
note = "Seve Your Message In Coustom Channel!"
client.HELP.update({
    plugin: {
        "category": category,
        "note": note,
        "commands": {
            "{CMD}Save <Text> [Reply]": "To Save Replyed Message White Name",
            "{CMD}Del <Text>": "To Delete Saved Message White Name",
            "{CMD}Get <Text>": "To Get Saved Message White Name",
            "{CMD}SaveList": "To Get List Of Saved Messages",
            "{CMD}CleanSaveList": "To Clean Saved Messages",
        },
    }
})
