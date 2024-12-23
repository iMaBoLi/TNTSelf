from TNTSelf import client
from telethon import events, types

__INFO__ = {
    "Category": "Practical",
    "Name": "Anti Edit",
    "Info": {
        "Help": "To Delete Edited Messages And Send Whitout Edit!",
        "Commands": {
            "{CMD}AntiEdit <On-Off>": {
                "Help": "To Turn On-Off Anti Edit"
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Anti Edit Mode Has Been {}!**"
}

@client.Command(command="AntiEdit (On|Off)")
async def setantiedit(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("ANTIEDIT_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(checkCmd=True)
async def antiedit(event):
    if event.original_update.to_dict()["_"] not in ["UpdateEditMessage", "UpdateEditChannelMessage"]: return
    antimode = event.client.DB.get_key("ANTIEDIT_MODE") or "OFF"
    if antimode == "ON":
        getmsg = await event.client.get_messages(event.chat_id, ids=event.id)
        if getmsg.reply_to:
            await event.respond(getmsg, reply_to=getmsg.reply_to.reply_to_msg_id)
        else:
            await event.respond(getmsg)
        await event.delete()