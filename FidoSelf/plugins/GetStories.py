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
    "not": "**{STR} The Stories For** ( {} ) **Is Not Found!**",
    "caption": "**{STR} The Stories For** ( {} ) **Is Sended!**"
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
        return await event.edit(client.getstrings(STRINGS)["not"].format(mention))
    caption = client.getstrings(STRINGS)["caption"].format(mention)
    for story in stories:
        sfile = await client.download_media(story.media)
        await client.send_file(event.chat_id, sfile, caption=caption)        
        os.remove(sfile)
    await event.delete()