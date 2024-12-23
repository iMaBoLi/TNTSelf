from TNTSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "Save",
    "Info": {
        "Help": "To Save Your Contents In Backup Channel!",
        "Commands": {
            "{CMD}Save <Name>": {
                "Help": "To Save Your Content White Name",
                "Input": {
                    "<Name>": "Name For Content",
                },
            },
            "{CMD}Delete <Name>": {
                "Help": "To Delete Your Saved Content White Name",
                "Input": {
                    "<Name>": "Name For Content",
                },
            },
            "{CMD}Get <Name>": {
                "Help": "To Get Your Saved Content White Name",
                "Input": {
                    "<Name>": "Name For Content",
                },
            },
            "{CMD}SaveList": {
                "Help": "To Getting Saved Content List",
            },
            "{CMD}CleanSaveList": {
                "Help": "To Clean Saved Content List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notall": "**{STR} The Name** ( `{}` ) **Already In Saves List!**",
    "save": "**{STR} The Message White Name** ( `{}` ) **Is Saves List!**",
    "notin": "**{STR} The Name** ( `{}` ) **Is Not In Saves List!**",
    "del": "**{STR} The Name And Message** ( `{}` ) **Deleted From Saves List!**",
    "notav": "**{STR} The Message White Name** ( `{}` ) **Is Not Available!**",
    "empty": "**{STR} The Saves List Is Empty!**",
    "list": "**{STR} The List Of Your Saves:**\n\n",
    "aempty": "**{STR} The Saves List Is Already Empty!**",
    "clean": "**{STR} The Saves List Has Been Cleaned!**"
}

@client.Command(command="Save (.*)")
async def savesaves(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    if reply:= event.checkReply():
        return await event.edit(reply)
    saves = event.client.DB.get_key("SAVED_LIST") or {}
    if name in saves:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(name))
    info = await event.reply_message.save()
    saves.update({name: info})
    event.client.DB.set_key("SAVED_LIST", saves)
    await event.edit(client.getstrings(STRINGS)["save"].format(name))

@client.Command(command="Delete (.*)$")
async def delsaves(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    saves = event.client.DB.get_key("SAVED_LIST") or {}
    if name not in saves:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(name))
    del saves[name]
    event.client.DB.set_key("SAVED_LIST", saves)
    await event.edit(client.getstrings(STRINGS)["del"].format(name))

@client.Command(command="Get (.*)$")
async def getsaves(event):
    await event.edit(client.STRINGS["wait"])
    name = event.pattern_match.group(1)
    saves = event.client.DB.get_key("SAVED_LIST") or {}
    if name not in saves:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(name))
    info = saves[name]
    try:
        message = await event.client.get_messages(info["chat_id"], ids=info["msg_id"])
        await event.respond(message)
        await event.delete()
    except:
        await event.edit(client.getstrings(STRINGS)["notav"].format(name))
        
@client.Command(command="SaveList")
async def savelist(event):
    await event.edit(client.STRINGS["wait"])
    saves = event.client.DB.get_key("SAVED_LIST") or {}
    if not saves:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for save in saves:
        text += f"**{row} -** `{save}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanSaveList")
async def cleansaves(event):
    await event.edit(client.STRINGS["wait"])
    saves = event.client.DB.get_key("SAVED_LIST") or {}
    if not saves:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("SAVED_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])