from TNTSelf import client
from telethon import functions
import os

__INFO__ = {
    "Category": "Users",
    "Name": "Get Stories",
    "Info": {
        "Help": "To Get Stories Of Users!",
        "Commands": {
            "{CMD}GetStories": {
                "Help": "To Get Stories",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}GetPinStories": {
                "Help": "To Get Pinned Stories",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**{STR} The Stories For** ( {} ) **Is Not Found!**",
    "sending": "**{STR} The Stories For** ( {} ) **Is Sending ...**",
    "caption": "**{STR} Story:** ( `{}` )",
    "sended": "**{STR} The Stories For** ( {} ) **Is Sended!**",
    "notall": "**{STR} The Stories For** ( {} ) **Is Not Found!**",
    "sendingall": "**{STR} The All Stories For** ( {} ) **Is Sending ...**",
    "captionall": "**{STR} Story:** ( `{}` )",
    "sendedall": "**{STR} The All Stories For** ( {} ) **Is Sended!**",
    "notpin": "**{STR} The Pinned Stories For** ( {} ) **Is Not Found!**",
    "sendingpin": "**{STR} The Pinned Stories For** ( {} ) **Is Sending ...**",
    "captionpin": "**{STR} Pinned Story:** ( `{}` )",
    "sendedpin": "**{STR} The Pinned Stories For** ( {} ) **Is Sended!**",
}

@client.Command(command="GetStories", userid=True)
async def getStories(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    stories = await client(functions.stories.GetPeerStoriesRequest(peer=event.userid))
    stories = stories.stories.stories
    if not stories:
        return await event.edit(client.getstrings(STRINGS)["not"].format(mention))
    await event.edit(client.getstrings(STRINGS)["sending"].format(mention))
    numstory = 1
    for story in stories:
        sfile = await client.download_media(story.media)
        caption = client.getstrings(STRINGS)["caption"].format(str(numstory))
        await client.send_file(event.chat_id, sfile, caption=caption)        
        os.remove(sfile)
        numstory += 1
    await event.edit(client.getstrings(STRINGS)["sended"].format(mention))

@client.Command(command="GetAllStories", userid=True)
async def getallStories(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    stories = await client(functions.stories.GetStoriesArchiveRequest(peer=event.userid, offset_id=0, limit=100))
    stories = stories.stories
    if not stories:
        return await event.edit(client.getstrings(STRINGS)["notall"].format(mention))
    await event.edit(client.getstrings(STRINGS)["sendingall"].format(mention))
    numstory = 1
    for story in stories:
        sfile = await client.download_media(story.media)
        caption = client.getstrings(STRINGS)["captionall"].format(str(numstory))
        await client.send_file(event.chat_id, sfile, caption=caption)        
        os.remove(sfile)
        numstory += 1
    await event.edit(client.getstrings(STRINGS)["sendedall"].format(mention))

@client.Command(command="GetPinStories", userid=True)
async def getpinStories(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    pinstories = await client(functions.stories.GetPinnedStoriesRequest(peer=event.userid, offset_id=0, limit=100))
    if not pinstories:
        return await event.edit(client.getstrings(STRINGS)["notpin"].format(mention))
    stories = await client(functions.stories.GetStoriesByIDRequest(peer=event.userid, id=pinstories.pinned_to_top))
    stories = stories.stories
    await event.edit(client.getstrings(STRINGS)["sendingpin"].format(mention))
    numstory = 1
    for story in stories:
        sfile = await client.download_media(story.media)
        caption = client.getstrings(STRINGS)["captionpin"].format(str(numstory))
        await client.send_file(event.chat_id, sfile, caption=caption)        
        os.remove(sfile)
        numstory += 1
    await event.edit(client.getstrings(STRINGS)["sendedpin"].format(mention))