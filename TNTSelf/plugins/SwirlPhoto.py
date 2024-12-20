from TNTSelf import client
from wand.image import Image
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Swirl Photo",
    "Info": {
        "Help": "To Swirl Your Photo!",
        "Commands": {
            "{CMD}Swirl <Num>": {
                "Help": "To Swirl Photo",
                "Input": {
                    "<Num>": "Number For Swirl",
                },
                "Reply": ["Photo"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "swirl": "**{STR} The Photo Was Swirled To** ( `{}°` )",
}

@client.Command(command="Swirl (\\-?\\d*)")
async def swirlphoto(event):
    await event.edit(client.STRINGS["wait"])
    darge = int(event.pattern_match.group(1))
    darge = darge if darge < 9999 else 9999
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    photo = await event.reply_message.download_media(client.PATH)
    newphoto = client.PATH + f"SwirlImage-{str(darge)}.jpg"
    simg = Image(filename=photo)
    simg.swirl(degree=darge) 
    simg.save(filename=newphoto)
    await event.respond(client.getstrings(STRINGS)["swirl"].format(str(darge)), file=newphoto)        
    os.remove(photo)
    os.remove(newphoto)
    await event.delete()