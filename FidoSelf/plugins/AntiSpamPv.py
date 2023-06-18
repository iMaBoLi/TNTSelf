from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Private",
    "Plugname": "Anti Spam",
    "Pluginfo": {
        "Help": "To Setting Anti Spam For Pv!",
        "Commands": {
            "{CMD}AntiSpamPv <On-Off>": None,
            "{CMD}AntiSpamWarn <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "antimode": "**The Anti Spam Pv Mode Has Been {}!**",
    "warnmode": "**The Anti Spam Warn Message Has Been {}!**",
    "nolimit": "**The Anti Spam Limit Must Be Between** ( `{}` ) **And** ( `{}` )",
    "limit": "**The Anti Spam Limit Messages Was Set To** ( `{}` )",
    "saveanti": "**The Anti Spam Message Was Saved!**",
    "saveantiwarn": "**The Anti Spam Warn Message Was Saved!**",
}

@client.Command(command="AntiSpamPv (On|Off)")
async def antipvmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("ANTISPAM_PV", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["antimode"].format(ShowChange))

@client.Command(command="AntiSpamWarn (On|Off)")
async def antipvwarn(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("ANTISPAM_WARN", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["warnmode"].format(ShowChange))

@client.Command(command="SetSpamPvLimit (\d*)")
async def setautodeletesleep(event):
    await event.edit(STRINGS["wait"])
    limit = event.pattern_match.group(1)
    if 3 > limit > 20:
        return await event.edit(STRINGS["nolimit"].format(3, 20))
    client.DB.set_key("ANTISPAM_LIMIT", limit)
    await event.edit(STRINGS["limit"].format(limit))

@client.Command(command="SetAntiSpam")
async def setanti(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["replyMedia"]["NotAll"])
    info = await event.reply_message.save()
    client.DB.set_key("ANTISPAM_MEDIA", info)
    await event.edit(STRINGS["saveanti"])
    
@client.Command(command="SetAntiSpamWarn")
async def setantiwarn(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_reply:
        return await event.edit(client.STRINGS["replyMedia"]["NotAll"])
    info = await event.reply_message.save()
    client.DB.set_key("ANTIWARN_MEDIA", info)
    await event.edit(STRINGS["saveantiwarn"])

WARNS = {}

@client.Command(onlysudo=False, alowedits=False)
async def antispam(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    antimode = client.DB.get_key("ANTISPAM_PV") or "off"
    if antimode == "off": return
    if not event.sender_id in WARNS:
        WARNS.update({event.sender_id: 0})
    lwarns = WARNS[event.sender_id]
    nwarns = lwarns + 1
    WARNS.update({event.sender_id: nwarns})
    limit = client.DB.get_key("ANTISPAM_LIMIT") or 5
    WARNSTEXT = f"{nwarns}/{limit}"
    if limit >= nwarns:
        manti = client.DB.get_key("ANTISPAM_MEDIA")
        if manti:
            getmsg = await client.get_messages(int(manti["chat_id"]), ids=int(manti["msg_id"]))
            getmsg.text = await client.AddVars(getmsg.text, event)
            getmsg.text = getmsg.text.replace("{WARNS}", WARNSTEXT)
            await event.reply(getmsg)
        WARNS.update({event.sender_id: 0})
        umode = client.DB.get_key("ANTISPAM_TYPE") or "Mute"
        if umode == "Mute":
            mutes = client.DB.get_key("MUTEPV_USERS")
            mutes.append(event.sender_id)
            client.DB.set_key("MUTEPV_USERS", mutes)
        else:
            await client(functions.contacts.BlockRequest(event.sender_id))
    else:
        wanti = client.DB.get_key("ANTISPAM_MEDIA")
        if wanti:
            getmsg = await client.get_messages(int(wanti["chat_id"]), ids=int(wanti["msg_id"]))
            getmsg.text = await client.AddVars(getmsg.text, event)
            getmsg.text = getmsg.text.replace("{WARNS}", WARNSTEXT)
            await event.reply(getmsg)