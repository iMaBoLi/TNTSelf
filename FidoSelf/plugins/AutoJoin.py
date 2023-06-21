from FidoSelf import client
from telethon import events, functions

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Auto Join",
    "Pluginfo": {
        "Help": "To Manage Auto Join To Leaved Chats!",
        "Commands": {
            "{CMD}AutoJoin <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Auto Join Mode Has Been {}!**",
}

@client.Command(command="AutoJoin (On|Off)")
async def autojoinmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("AUTOJOIN_MODE", change)
    schange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(schange))
    
@client.on(events.ChatAction())
async def autojoin(event):
    if not event.user_left and not event.user_kicked: return
    user = await event.get_user()
    if user.id != client.me.id: return
    ajoinmode = client.DB.get_key("AUTOJOIN_MODE") or "OFF"
    if ajoinmode == "ON":
        chat = await event.get_chat()
        await client(functions.channels.JoinChannelRequest(channel=chat.id))