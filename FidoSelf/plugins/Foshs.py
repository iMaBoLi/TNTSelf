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
    reply, mtype = event.checkReply(["TXT File"])
    if reply: return await event.edit(reply)
    info = await event.reply_message.save()
    get = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await get.download_media(client.PATH + "FOSHS.txt")
    client.DB.set_key("FOSHS_FILE", info)
    await event.edit(STRINGS["save"])

@client.Command(command="DelFosh")
async def delfoshfile(event):
    await event.edit(client.STRINGS["wait"])
    if os.path.exists(client.PATH + "FOSHS.txt"):
        os.remove(client.PATH + "FOSHS.txt")
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