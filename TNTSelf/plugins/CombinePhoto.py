from TNTSelf import client
from PIL import Image
import os

__INFO__ = {
    "Category": "Convert",
    "Name": "Combine Photo",
    "Info": {
        "Help": "To Create Combine Photo For Your Photos!",
        "Commands": {
            "{CMD}SCVer <Count>": {
                "Help": "To Vertical Combine",
                "Input": {
                    "<Count>": "Number For Photos",
                },
                "Reply": ["Photo"]
            },
            "{CMD}SCHor <Count>": {
                "Help": "To Horizontal Combine",
                "Input": {
                    "<Count>": "Number For Photos",
                },
                "Reply": ["Photo"]
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "vercoming": "**{STR} Comining Your Photos In Vertical Mode ...**\n**{STR} Photo Count:** ( `{}` )",
    "vercom": "**{STR} The Selected Photos Is Combined In Vertical Mode!**\n**{STR} Photo Count:** ( `{}` )",
    "horcoming": "**{STR} Comining Your Photos In Horizontal Mode ...**\n**{STR} Photo Count:** ( `{}` )",
    "horcom": "**{STR} The Selected Photos Is Combined In Horizontal Mode!**\n**{STR} Photo Count:** ( `{}` )",
}

@client.Command(command="SCVer (\\d*)")
async def verticalcombine(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    count = int(event.pattern_match.group(1))
    count = count if count <= 100 else 100
    photos = []
    for i in range(count):
        getmsg = await client.get_messages(event.chat_id, ids=(event.reply_message.id + i))
        mtype = getmsg.mediatype()
        if getmsg and getmsg.media and "Photo" in mtype:
            photo = await client.download_media(getmsg.media, client.PATH)
            photos.append(photo)
    await event.edit(client.getstrings(STRINGS)["vercoming"].format(len(photos)))
    widths = 0
    heights = 0
    for photo in photos:
        img = Image.open(photo)
        width, height = img.size
        widths += width
        heights += height + 5
    rowidth = round(widths / len(photos))
    newimg = Image.new("RGBA", (rowidth + 10, heights + 5), (255, 255, 255))
    cheight = 5
    for photo in photos:
        nphoto = Image.open(photo)
        _, height = nphoto.size
        nphoto = nphoto.resize((rowidth, height))
        newimg.paste(nphoto, (5, cheight))
        cheight += height + 5
    newphoto = client.PATH + "VerticalCombine.png"
    newimg.save(newphoto)
    callback = event.progress(upload=True)
    caption = client.getstrings(STRINGS)["vercom"].format(len(photos))
    await client.send_file(event.chat_id, newphoto, force_document=True, caption=caption, progress_callback=callback)
    os.remove(newphoto)
    for photo in photos:
        os.remove(photo)
    await event.delete()
    
@client.Command(command="SCHor (\\d*)")
async def horizontalcombine(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["Photo"]):
        return await event.edit(reply)
    count = int(event.pattern_match.group(1))
    count = count if count <= 100 else 100
    photos = []
    for i in range(count):
        getmsg = await client.get_messages(event.chat_id, ids=(event.reply_message.id + i))
        mtype = getmsg.mediatype()
        if getmsg and getmsg.media and "Photo" in mtype:
            photo = await client.download_media(getmsg.media, client.PATH)
            photos.append(photo)
    await event.edit(client.getstrings(STRINGS)["horcoming"].format(len(photos)))
    heights = 0
    widths = 0
    for photo in photos:
        img = Image.open(photo)
        width, height = img.size
        heights += height
        widths += width + 5
    roheight = round(heights / len(photos))
    newimg = Image.new("RGBA", (widths + 5, roheight + 10), (255, 255, 255))
    cwidth = 5
    for photo in photos:
        nphoto = Image.open(photo)
        width, _ = nphoto.size
        nphoto = nphoto.resize((width, roheight))
        newimg.paste(nphoto, (cwidth, 5))
        cwidth += width + 5
    newphoto = client.PATH + "HorizontalCombine.png"
    newimg.save(newphoto)
    callback = event.progress(upload=True)
    caption = client.getstrings(STRINGS)["horcom"].format(len(photos))
    await client.send_file(event.chat_id, newphoto, force_document=True, caption=caption, progress_callback=callback)
    os.remove(newphoto)
    for photo in photos:
        os.remove(photo)
    await event.delete()