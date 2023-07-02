from FidoSelf import client
import os

__INFO__ = {
    "Category": "Account",
    "Plugname": "Font",
    "Pluginfo": {
        "Help": "To Save Font File For Profile Time!",
        "Commands": {
            "{CMD}SetFont <Reply(File)>": None,
            "{CMD}DelFont": None,
            "{CMD}GetFont": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "setfont": "**The Font File Has Been Saved!**",
    "delfont": "**The Font File Has Been Deleted!**",
    "notsave": "**The Font File Is Not Saved!**",
    "getfont": "**The Font File For Profile Time!**",
}

@client.Command(command="SetFont")
async def setfontfile(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply(["TTF"])
    if reply: return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "FontFile.ttf")
    client.DB.set_key("FONT_FILE", info)
    await event.edit(STRINGS["setfont"])

@client.Command(command="DelFont")
async def delfontfile(event):
    await event.edit(client.STRINGS["wait"])
    client.DB.del_key("FONT_FILE")
    font = client.PATH + "FontFile.ttf"
    if os.path.exists(font):
        os.remove(font)
    await event.edit(STRINGS["delfont"])
    
@client.Command(command="GetFont")
async def getfontfile(event):
    await event.edit(client.STRINGS["wait"])
    font = client.PATH + "FontFile.ttf"
    if not os.path.exists(font):
        return await event.edit(STRINGS["notsave"])
    caption = STRINGS["getfont"]
    await event.respond(caption, file=font)
    await event.delete()