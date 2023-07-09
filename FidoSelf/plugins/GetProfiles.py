from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Users",
    "Name": "Get Profiles",
    "Info": {
        "Help": "To Get Profile Photos Of Users!",
        "Commands": {
            "{CMD}GProfiles": {
                "Help": "To Get Profiles",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**{STR} The Profile Photos For** ( {} ) **Is Not Found!**",
    "caption": "**{STR} The Profile Photos For** ( {} ) **Is Sended!**"
}

@client.Command(command="GProfiles", userid=True)
async def getprofiles(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    info = await client.get_entity(event.userid)
    mention = client.functions.mention(info)
    photos = await client.get_profile_photos(event.userid)
    if not photos:
        return await event.edit(client.getstrings(STRINGS)["not"].format(mention))
    caption = client.getstrings(STRINGS)["caption"].format(mention)
    for phs in client.functions.chunks(photos, 9):
        await event.respond(caption, file=phs)
    await event.delete()