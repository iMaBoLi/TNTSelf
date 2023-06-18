from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Save",
    "Pluginfo": {
        "Help": "To Save Your Contents In Backup Channel!",
        "Commands": {
            "{CMD}Save <Name>": "Save Your Content White Name!**",
            "{CMD}Delete <Name>": "Delete Your Content White Name!**",
            "{CMD}Get <Name>": "Get Your Content White Name!**",
            "{CMD}SaveList": None,
            "{CMD}CleanSaveList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**The Name** ( `{}` ) **Already In Saveds List!**",
    "save": "**The Message White Name** ( `{}` ) **Is Saved!**",
    "notin": "**The Name** ( `{}` ) **Is Not In Saveds List!**",
    "del": "**The Name And Message** ( `{}` ) **Deleted From Saveds List!**",
    "notav": "**The Message White Name** ( `{}` ) **Is Not Available To Send!**",
    "empty": "**The Saveds List Is Empty!**",
    "list": "**The Saveds List:**\n\n",
    "aempty": "**The Saveds List Is Already Empty!**",
    "clean": "**The Saveds List Has Been Cleaned!**",
}

@client.Command(command="Save (.*)")
async def savesaves(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    if not event.is_reply:
        return await event.edit(client.STRINGS["replyMedia"]["NotAll"])
    saves = client.DB.get_key("SAVES") or {}
    if name in saves:
        return await event.edit(STRINGS["notall"].format(name))
    info = await event.reply_message.save()
    saves.update({name: info})
    client.DB.set_key("SAVES", saves)
    await event.edit(STRINGS["save"].format(name))

@client.Command(command="Delete (.*)$")
async def delsaves(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    saves = client.DB.get_key("SAVES") or {}
    if name not in saves:
        return await event.edit(STRINGS["notin"].format(name))
    info = saves[name]
    try:
        message = await client.get_messages(info["chat_id"], ids=info["msg_id"])
        await message.delete()
    except:
        pass
    del saves[name]
    client.DB.set_key("SAVES", saves)
    await event.edit(STRINGS["del"].format(name))

@client.Command(command="Get (.*)$")
async def getsaves(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    saves = client.DB.get_key("SAVES") or {}
    if name not in saves:
        return await event.edit(STRINGS["notin"].format(name))
    info = saves[name]
    try:
        message = await client.get_messages(info["chat_id"], ids=info["msg_id"])
        await event.respond(message)
        await event.delete()
    except:
        await event.edit(STRINGS["notav"].format(name))
        
@client.Command(command="SaveList")
async def savelist(event):
    await event.edit(client.STRINGS["wait"])
    saves = client.DB.get_key("SAVES") or {}
    if not saves:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for save in saves:
        text += f"**{row} -** `{save}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanSaveList")
async def cleansaves(event):
    await event.edit(client.STRINGS["wait"])
    saves = client.DB.get_key("SAVES") or {}
    if not saves:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("SAVES")
    await event.edit(STRINGS["clean"])