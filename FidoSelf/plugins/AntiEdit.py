from FidoSelf import client
from telethon import events, types

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Anti Edit",
    "Pluginfo": {
        "Help": "To Delete Edited Messages And Send Whitout Edit!",
        "Commands": {
            "{CMD}AntiEdit <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Anti Edit Mode Has Been {}!**",
}

@client.Command(command="AntiEdit (On|Off)")
async def setanti(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("ANTIEDIT_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.on(events.Raw(types.UpdateEditChannelMessage))
@client.on(events.Raw(types.UpdateEditMessage))
async def antiedit(event):
    if not event.message.out or event.checkCmd() or event.message.via_bot_id: return
    antimode = client.DB.get_key("ANTIEDIT_MODE") or "off"
    if antimode == "on":
        getmsg = await client.get_messages(event.chat_id, ids=event.id)
        if getmsg.reply_to:
            await event.respond(getmsg, reply_to=getmsg.reply_to.reply_to_msg_id)
        else:
            await event.respond(getmsg)
        await event.delete()