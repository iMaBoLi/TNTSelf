from FidoSelf import client
from telethon import events, types

__INFO__ = {
    "Category": "Practical",
    "Name": "Anti Edit",
    "Info": {
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
async def setantiedit(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ANTIEDIT_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command()
async def antiedit(event):
    if event.original_update.to_dict()["_"] not in ["UpdateEditMessage", "UpdateEditChannelMessage"]: return
    if event.checkCmd(): return
    antimode = client.DB.get_key("ANTIEDIT_MODE") or "OFF"
    if antimode == "ON":
        getmsg = await client.get_messages(event.chat_id, ids=event.id)
        if getmsg.reply_to:
            await event.respond(getmsg, reply_to=getmsg.reply_to.reply_to_msg_id)
        else:
            await event.respond(getmsg)
        await event.delete()