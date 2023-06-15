from FidoSelf import client
from telethon import functions, types

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Get Profiles",
    "Pluginfo": {
        "Help": "To Get Profile Photos Of Users!",
        "Commands": {
            "{CMD}GProfiles <Pv|Reply|UserID|Username>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**The Profile Photos For** ( {} ) **Is Not Found!**",
    "caption": "**The Profile Photos For** ( {} ) **Is Sended!**",
}

@client.Command(command="GProfiles ?(.*)?")
async def delprofiles(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    photos = await client.get_profile_photos(userid)
    if not photos:
        return await event.edit(STRINGS["not"].format(mention))
    caption = STRINGS["caption"].format(mention)
    for phs in client.functions.chunks(photos, 9):
        await event.respond(caption, file=phs)
    await event.delete()