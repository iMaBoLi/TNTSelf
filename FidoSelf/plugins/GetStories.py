from FidoSelf import client
from telethon import functions, types

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
    stories = await client(functions.stories.GetPeerStoriesRequest(peer="@vahed135"))
    stories = stories.stories.stories
    if not stories:
        return await event.edit(client.getstrings(STRINGS)["not"].format(mention))
    caption = client.getstrings(STRINGS)["caption"].format(mention)
    for storis in client.functions.chunks(stories, 9):
        await event.respond(caption, file=storis)
    await event.delete()