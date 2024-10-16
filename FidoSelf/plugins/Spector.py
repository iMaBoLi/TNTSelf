from FidoSelf import client
from telethon import events, functions, types, Button
import asyncio
import datetime

__INFO__ = {
    "Category": "Manage",
    "Name": "Spector",
    "Info": {
        "Help": "To Get Spector Panel For Users!",
        "Commands": {
            "{CMD}Spector": {
                "Help": "To Get Spector Panel",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "spector": "**❊ Welcome To Spector Menu:**\n\n    **{STR} Select Options Below To Manage Spector Modes:**\n    **{STR} User:** ( {} )",
    "specstatus": "**{STR} User** ( {} - `{}` )\n    **➛ Is {} Now!** ( `{}` )",
    "specaction": "**{STR} User** ( {} - `{}` )\n    **➛ Is {} {} Now!** ( `{}` )",
    "specreadpv": "**{STR} User** ( {} - `{}` )\n    **➛ Is Read Your Pv Now!** ( `{}` )",
    "specjoingroup": "**{STR} User** ( {} - `{}` )\n    **➛ Is Joined To Group** ( `{}` - `{}` ) **Now!** ( `{}` )",
    "specleavegroup": "**{STR} User** ( {} - `{}` )\n    **➛ Is Leaved From Group** ( `{}` - `{}` ) **Now!** ( `{}` )",
    "closespector": "**{STR} The Spector Panel Successfuly Closed!**",
}

SPECS = [
    "STATUS",
    "ACTION",
    "READ_PV",
    "JOIN_GROUPS",
    "LEAVE_GROUPS",
]

async def get_spector_buttons(userid, chatid):
    buttons = []
    for spec in SPECS:
        lists = client.DB.get_key(f"SPECTOR_{spec}") or []
        smode = client.STRINGS["inline"]["On"] if userid in lists else client.STRINGS["inline"]["Off"]
        cmode = "del" if userid in lists else "add"
        show = spec.replace("_", " ").title()
        buttons.append(Button.inline(f"• {show} {smode}", data=f"SetSpector:{chatid}:{userid}:{spec}:{cmode}"))
    buttons = client.functions.chunker(buttons, [2,1])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="CloseSpector")])
    return buttons

@client.Command(command="Spector", userid=True)
async def Spector(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"Spector:{chatid}:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Spector\:(.*)\:(.*)")
async def inlinespector(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    text = client.getstrings(STRINGS)["spector"].format(mention)
    buttons = await get_spector_buttons(userid, chatid)
    await event.answer([event.builder.article("FidoSelf - Spector", text=text, buttons=buttons)])

@client.Callback(pattern="Spector\:(.*)\:(.*)")
async def callspector(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    text = client.getstrings(STRINGS)["spector"].format(mention)
    buttons = await get_spector_buttons(userid, chatid)
    await event.edit(text, buttons=buttons)

@client.Callback(data="SetSpector\:(.*)\:(.*)\:(.*)\:(.*)")
async def setspector(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    mode = event.data_match.group(3).decode('utf-8')
    change = event.data_match.group(4).decode('utf-8')
    info = await client.get_entity(userid)
    mode = "SPECTOR_" + mode
    lists = client.DB.get_key(mode) or []
    if change == "add":
        lists.append(userid)
        client.DB.set_key(mode, lists)
    elif change == "del":
        lists.remove(userid)
        client.DB.set_key(mode, lists)
    buttons = await get_spector_buttons(userid, chatid)
    await event.edit(buttons=buttons)

@client.Callback(data="CloseSpector")
async def closespector(event):
    text = client.getstrings(STRINGS)["closespector"]
    await event.edit(text=text)

@client.on(events.UserUpdate)
async def statusspec(event):
    if event.user_id == client.me.id or not event.status: return
    status = event.status.to_dict()["_"]
    if status not in ["UserStatusOnline", "UserStatusOffline", "UserStatusRecently"]: return
    lists = client.DB.get_key("SPECTOR_STATUS") or []
    if event.user_id in lists:
        info = await client.get_entity(event.user_id)
        mention = client.functions.mention(info)
        localtime = datetime.datetime.now()
        time = localtime.strftime("%H:%M:%S")
        text = client.getstrings(STRINGS)["specstatus"].format(mention, event.user_id, status.replace("UserStatus", ""), time)
        await client.bot.send_message(client.REALM, text)
        
@client.on(events.UserUpdate)
async def actionspec(event):
    if event.user_id == client.me.id or not event.action: return
    action = event.action.to_dict()["_"]
    actions = {
        "SendMessageTypingAction": "Typing Message",
        "SendMessageUploadPhotoAction": "Sending Photo",
        "SendMessageUploadVideoAction": "Sending Video",
        "SendMessageUploadAudioAction": "Sending Music",
        "SendMessageUploadDocumentAction": "Sending File",
        "SendMessageUploadRoundAction": "Sending Round Video",
        "SendMessageRecordVideoAction": "Recording Video",
        "SendMessageRecordAudioAction": "Recording Voice",
        "SendMessageRecordRoundAction": "Recording Round Video",
    }
    if action not in actions: return
    lists = client.DB.get_key("SPECTOR_ACTION") or []
    if event.user_id in lists:
        info = await client.get_entity(event.user_id)
        mention = client.functions.mention(info)
        localtime = datetime.datetime.now()
        time = localtime.strftime("%H:%M:%S")
        where = "In Your Pv" if "UpdateUser" in event.original_update.to_dict()["_"] else "In A Chat"
        text = client.getstrings(STRINGS)["specaction"].format(mention, event.user_id, actions[action], where, time)
        await client.bot.send_message(client.REALM, text)
        
@client.on(events.MessageRead)
async def readpvspec(event):
    if event.chat_id == client.me.id or not event.is_private: return
    userid = event.original_update.peer.user_id
    lists = client.DB.get_key("SPECTOR_READ_PV") or []
    if userid in lists:
        info = await client.get_entity(userid)
        mention = client.functions.mention(info)
        localtime = datetime.datetime.now()
        time = localtime.strftime("%H:%M:%S")
        text = client.getstrings(STRINGS)["specreadpv"].format(mention, userid, time)
        await client.bot.send_message(client.REALM, text)
        
@client.on(events.ChatAction)
async def joingroupspec(event):
    if not event.user_joined and not event.added_by: return
    userid = (await event.get_user()).id
    if userid == client.me.id: return
    lists = client.DB.get_key("SPECTOR_JOIN_GROUPS") or []
    if userid in lists:
        info = await client.get_entity(userid)
        mention = client.functions.mention(info)
        chat = await event.get_chat()
        localtime = datetime.datetime.now()
        time = localtime.strftime("%H:%M:%S")
        text = client.getstrings(STRINGS)["specjoingroup"].format(mention, userid, chat.title, chat.id, time)
        await client.bot.send_message(client.REALM, text)
        
@client.on(events.ChatAction)
async def leavegroupspec(event):
    if not event.user_left and not event.user_kicked: return
    userid = (await event.get_user()).id
    if userid == client.me.id: return
    lists = client.DB.get_key("SPECTOR_LEAVE_GROUPS") or []
    if userid in lists:
        info = await client.get_entity(userid)
        mention = client.functions.mention(info)
        chat = await event.get_chat()
        localtime = datetime.datetime.now()
        time = localtime.strftime("%H:%M:%S")
        text = client.getstrings(STRINGS)["specleavegroup"].format(mention, userid, chat.title, chat.id, time)
        await client.bot.send_message(client.REALM, text)