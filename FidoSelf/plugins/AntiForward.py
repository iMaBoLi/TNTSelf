from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Anti Forward",
    "Pluginfo": {
        "Help": "To Delete Forwarded Messages And Send Whitout Forward!",
        "Commands": {
            "{CMD}AntiForward <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Anti Forward Mode Has Been {}!**",
}

@client.Command(command="AntiForward (On|Off)")
async def setanti(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ANTIFORWARD_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(alowedits=False)
async def antiforward(event):
    if event.checkCmd() or not event.fwd_from or event.is_ch: return
    antimode = client.DB.get_key("ANTIFORWARD_MODE") or "OFF"
    if antimode == "ON":
        getmsg = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(getmsg)
        await event.delete()