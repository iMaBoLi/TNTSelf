from FidoSelf import client
from telethon import functions
from jdatetime import datetime
import random

__INFO__ = {
    "Category": "Pv",
    "Name": "Anti Spam",
    "Info": {
        "Help": "To Setting Anti Spam For Pv And Protection!",
        "Commands": {
            "{CMD}AntiSpamPv <On-Off>": {
                "Help": "To Turn On-Off AntiSpam Pv",
            },
            "{CMD}AntiSpamWarn <On-Off>": {
                "Help": "To Turn On-Off AntiSpam Pv Warn Message",
            },
            "{CMD}SetSpamPvLimit <Limit>": {
                "Help": "To Set AntiSpam Pv Limit",
                "Input": {
                    "<Limit>": "Limit For Messages ( 3-20 )",
                },
            },
            "{CMD}SetAntiSpam": {
                "Help": "To Set AntiSapm Pv Message",
                "Reply": ["Message", "Media"],
                "Vars": ["TIME", "DATE", "HEART", "NAME", "MENTION", "USERNAME", "WARNS"],
            },
            "{CMD}SetAntiSpamWarn": {
                "Help": "To Set AntiSpam Pv Warn Message",
                "Reply": ["Message", "Media"],
                "Vars": ["TIME", "DATE", "HEART", "NAME", "MENTION", "USERNAME", "WARNS"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "antimode": "**{STR} The Anti Spam Pv Mode Has Been {}!**",
    "warnmode": "**{STR} The Anti Spam Warn Message Has Been {}!**",
    "nolimit": "**{STR} The Anti Spam Limit Must Be Between** ( `{}` ) **And** ( `{}` )",
    "limit": "**{STR} The Anti Spam Limit Messages Was Set To** ( `{}` )",
    "saveanti": "**{STR} The Anti Spam Message Was Saved!**",
    "saveantiwarn": "**{STR} The Anti Spam Warn Message Was Saved!**"
}

@client.Command(command="AntiSpamPv (On|Off)")
async def antipvmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ANTISPAMPV_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["antimode"].format(showchange))

@client.Command(command="AntiSpamWarn (On|Off)")
async def antipvwarn(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ANTISPAMPVWARN_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["warnmode"].format(showchange))

@client.Command(command="SetSpamPvLimit (\d*)")
async def setspamlimit(event):
    await event.edit(client.getstrings(STRINGS)["wait"])
    limit = event.pattern_match.group(1)
    if 3 > limit > 20:
        return await event.edit(client.getstrings(STRINGS)["nolimit"].format(3, 20))
    client.DB.set_key("ANTISPAM_LIMIT", limit)
    await event.edit(client.getstrings(STRINGS)["limit"].format(limit))

@client.Command(command="SetAntiSpam")
async def setanti(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply():
        return await event.edit(reply)
    info = await event.reply_message.save()
    client.DB.set_key("ANTISPAM_MEDIA", info)
    await event.edit(client.getstrings(STRINGS)["saveanti"])
    
@client.Command(command="SetAntiSpamWarn")
async def setantiwarn(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply():
        return await event.edit(reply)
    info = await event.reply_message.save()
    client.DB.set_key("ANTISPAMWARN_MEDIA", info)
    await event.edit(client.getstrings(STRINGS)["saveantiwarn"])

WARNS = {}

@client.Command(onlysudo=False, allowedits=False)
async def antispam(event):
    if (
        not event.is_private
        or event.is_white
        or event.is_sudo
        or event.is_bot
    ):
        return
    antimode = client.DB.get_key("ANTISPAMPV_MODE") or "OFF"
    if antimode == "OFF": return
    mutes = client.DB.get_key("MUTEPV_USERS") or []
    if event.sender_id in mutes: return
    if not event.sender_id in WARNS:
        WARNS.update({event.sender_id: 0})
    lwarns = WARNS[event.sender_id]
    nwarns = lwarns + 1
    WARNS.update({event.sender_id: nwarns})
    limit = client.DB.get_key("ANTISPAM_LIMIT") or 5
    WARNSTEXT = f"{nwarns}/{limit}"
    swarn = client.DB.get_key("ANTISPAMPVWARN_MODE") or "OFF"
    if nwarns >= limit:
        manti = client.DB.get_key("ANTISPAM_MEDIA")
        if swarn == "ON" and manti:
            getmsg = await client.get_messages(int(manti["chat_id"]), ids=int(manti["msg_id"]))
            getmsg.text = await client.AddVars(getmsg.text, event)
            getmsg.text = getmsg.text.replace("{WARNS}", WARNSTEXT)
            await event.reply(getmsg)
        WARNS.update({event.sender_id: 0})
        umode = client.DB.get_key("ANTISPAMPV_TYPE") or "Mute"
        if umode == "Mute":
            mutes = client.DB.get_key("MUTEPV_USERS") or []
            mutes.append(event.sender_id)
            client.DB.set_key("MUTEPV_USERS", mutes)
        else:
            await client(functions.contacts.BlockRequest(event.sender_id))
    else:
        wanti = client.DB.get_key("ANTISPAMWARN_MEDIA")
        if swarn == "ON" and wanti:
            getmsg = await client.get_messages(int(wanti["chat_id"]), ids=int(wanti["msg_id"]))
            info = await client.get_entity(event.chat_id)
            jtime = datetime.now()
            VARS = {
                "TIME": jtime.strftime("%H:%M"),
                "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
                "HEART": random.choice(client.functions.HEARTS),
                "NAME": info.first_name,
                "MENTION": client.functions.mention(info),
                "USERNAME": info.username or "---",
                "WARNS": WARNSTEXT,
            }
            for VAR in VARS:
                getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
            await event.reply(getmsg)