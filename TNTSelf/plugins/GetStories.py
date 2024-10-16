from FidoSelf import client
from telethon import functions
import os

__INFO__ = {
    "Category": "Users",
    "Name": "Get Stories",
    "Info": {
        "Help": "To Get Stories Of Users!",
        "Commands": {
            "{CMD}GStories": {
                "Help": "To Get Stories",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "EN": {
        "not": "**{STR} The Stories For** ( {} ) **Is Not Found!**",
        "sending": "**{STR} The Stories For** ( {} ) **Is Sending ...**",
        "caption": "**{STR} Story:** ( `{}` )",
        "sended": "**{STR} The Stories For** ( {} ) **Is Sended!**",
    },
    "FA": {
        "not": "**{STR} هیچ استوری برای** ( {} ) **پیدا نشد!**",
        "sending": "**{STR} درحال ارسال استوری های کاربر:** ( {} )",
        "caption": "**{STR} استوری:** ( `{}` )",
        "sended": "**{STR} همه استوری های** ( {} ) **ارسال شد!**",
    },
}

@client.Command(command="GStories", userid=True)
async def getStories(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    stories = await client(functions.stories.GetPeerStoriesRequest(peer=event.userid))
    stories = stories.stories.stories
    if not stories:
        return await event.edit(client.getstring(STRINGS, "not").format(mention))
    await event.edit(client.getstring(STRINGS, "sending").format(mention))
    numstory = 1
    for story in stories:
        sfile = await client.download_media(story.media)
        caption = client.getstring(STRINGS, "caption").format(str(numstory))
        await client.send_file(event.chat_id, sfile, caption=caption)        
        os.remove(sfile)
        numstory += 1
    await event.edit(client.getstring(STRINGS, "sended").format(mention))
    