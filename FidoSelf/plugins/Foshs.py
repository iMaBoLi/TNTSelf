from FidoSelf import client
import os

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Foshs",
    "Pluginfo": {
        "Help": "To Manage Fosh File For Enemies!",
        "Commands": {
            "{CMD}AddFosh <Reply(File)>": None,
            "{CMD}DelFosh": None,
            "{CMD}GetFosh": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "save": "**The Enemy Foshs File Has Been Saved!**",
    "del": "**The Enemy Foshs File Has Been Deleted!**",
    "nsave": "**The Enemy Foshs File Is Not Saved!**",
    "file": "**The Foshs File!**\n**Count:** ( `{}` )",
}

@client.Command(command="AddFosh")
async def savefoshfile(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or mtype not in ["File"]:
        medias = client.STRINGS["replyMedia"]
        media = medias["File"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    format = str(event.reply_message.media.document.attributes[0].file_name).split(".")[-1]
    if format != "txt":
        return await event.edit(STRINGS["txt"])
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "FOSHS.txt")
    client.DB.set_key("FOSHS_FILE", info)
    await event.edit(STRINGS["save"])

@client.Command(command="DelFosh")
async def delfoshfile(event):
    await event.edit(client.STRINGS["wait"])
    client.DB.del_key("FOSHS_FILE")
    await event.edit(STRINGS["del"])

@client.Command(command="GetFosh")
async def getfoshfile(event):
    await event.edit(client.STRINGS["wait"])
    foshs = client.DB.get_key("FOSHS_FILE")
    if not foshs:
        return await event.edit(STRINGS["nsave"])
    file = client.PATH + "FOSHS.txt"
    lines = len(open(file, "r").readlines())
    await event.respond(STRINGS["file"].format(lines), file=file)
    os.remove(file)