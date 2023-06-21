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
    "autojoin": "**The Auto Join Joined You To Leaved Chat!**\n\n**ChatID:** ( `{}` )\n**Username:** ( `{}` )",
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
    if (event.user_left or event.user_kicked) and event.out:
        ajoinmode = client.DB.get_key("AUTOJOIN_MODE") or "OFF"
        if ajoinmode == "ON":
            try:
                chat = await event.get_chat()
                await client(functions.channels.JoinChannelRequest(channel=chat.id))
                text = STRINGS["autojoin"].format(chat.id, (chat.username or chat.title))
                await client.send_message(client.REALM, text)
            except:
                pass