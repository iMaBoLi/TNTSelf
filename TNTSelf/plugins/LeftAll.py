from TNTSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Name": "Left",
    "Info": {
        "Help": "To Left From All Channels or Groups!",
        "Commands": {
            "{CMD}LeftChs": {
                "Help": "To Left Channels",
            },
            "{CMD}LeftGps": {
                "Help": "To Left Groups",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "not": "**{STR} The {} List In Your Account Is Empty!**",
    "lefting": "**{STR} Lefting From** ( `{}` ) **{} In Your Account ...**",
    "left": "**{STR} Successfuly Lefted From** ( `{}` ) **{} In Your Account!**",
}

@client.Command(command="Left(Chs|Gps)")
async def leftall(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).upper()
    chats = []
    names = {"CHS": "Channel", "GPS": "Group"}
    async for dialog in client.iter_dialogs():
        if dialog.entity.to_dict()["_"] == "Channel":
            if type == "CHS" and dialog.entity.broadcast:
                chid = dialog.id
                chats.append(chid)
            elif type == "GPS" and not dialog.entity.broadcast:
                chid = dialog.id
                chats.append(chid)
    if not chats:
        return await event.edit(client.getstrings(STRINGS)["not"].format(names[type]))
    await event.edit(client.getstrings(STRINGS)["lefting"].format(len(chats), names[type]))
    for chat in chats:
        await client(functions.channels.LeaveChannelRequest(channel=chat))
    await event.edit(client.getstrings(STRINGS)["left"].format(len(chats), names[type]))