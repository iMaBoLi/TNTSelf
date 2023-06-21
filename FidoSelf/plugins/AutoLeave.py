from FidoSelf import client
from telethon import events, functions

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Auto Leave",
    "Pluginfo": {
        "Help": "To Manage Auto Leave To Joined Chats!",
        "Commands": {
            "{CMD}AutoLeave <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Auto Leave Mode Has Been {}!**",
    "autoleave": "**The Auto Leave Leaved You From New Joined Chat!**\n\n**ChatID:** ( `{}` )\n**Username:** ( `{}` )",
}

@client.Command(command="AutoLeave (On|Off)")
async def autoleavemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("AUTOLEAVE_MODE", change)
    schange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(schange))
    
@client.on(events.ChatAction())
async def autoleave(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        aleavemode = client.DB.get_key("AUTOLEAVE_MODE") or "OFF"
        if aleavemode == "ON" and user.id == client.me.id:
            try:
                chat = await event.get_chat()
                await client(functions.channels.LeaveChannelRequest(channel=chat.id))
                text = STRINGS["autoleave"].format(chat.id, (chat.username or chat.title))
                await client.send_message(client.REALM, text)
            except:
                pass