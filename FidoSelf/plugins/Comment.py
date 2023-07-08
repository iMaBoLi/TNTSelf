from FidoSelf import client
from telethon import functions
from jdatetime import datetime
import aiocron
import random

__INFO__ = {
    "Category": "Groups",
    "Name": "Comment",
    "Info": {
        "Help": "To Manage Auto Comment In The Channel Messages!",
        "Commands": {
            "{CMD}Comment <On-Off>": None,
            "{CMD}SetComment <Reply>": None,
            "{CMD}DelComment": None,
            "{CMD}GetComment": None,
            "{CMD}CommentList": None,
            "{CMD}CleanCommentList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Comment Mode Has Been {}!**",
    "setcomment": "**{STR} The Comment Message For This Chat Has Been Saved!**",
    "notsave": "**{STR} The Comment Message For This Chat Is Not Saved!**",
    "delcomment": "**{STR} The Comment Message For This Chat Has Been Removed!**",
    "empty": "**{STR} The Comment List Is Empty!**",
    "list": "**{STR} The Comment List:**\n\n",
    "aempty": "**{STR} The Comment List Is Already Empty**",
    "clean": "**{STR} The Comment List Has Been Cleaned!**"
}

@client.Command(command="Comment (On|Off)")
async def commentmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("COMMENT_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="SetComment")
async def setcomment(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if reply:= event.checkReply():
        return await event.edit(reply)
    comments = client.DB.get_key("COMMENT_CHATS") or {}
    info = await event.reply_message.save()
    comments.update({event.chat_id: info})
    client.DB.set_key("COMMENT_CHATS", comments)
    await event.edit(client.getstrings(STRINGS)["setcomment"])
    
@client.Command(command="DelComment")
async def delcomment(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    comments = client.DB.get_key("COMMENT_CHATS") or {}
    if event.chat_id not in comments:
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    del comments[event.chat_id]
    client.DB.set_key("COMMENT_CHATS", comments)
    await event.edit(client.getstrings(STRINGS)["delcomment"])

@client.Command(command="GetComment")
async def getcomment(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    comments = client.DB.get_key("COMMENT_CHATS") or {}
    if event.chat_id not in comments:
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    info = comments[event.chat_id]
    getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await event.respond(getmsg)
    await event.delete()

@client.Command(command="CommentList")
async def commentlist(event):
    await event.edit(client.STRINGS["wait"])
    comments = client.DB.get_key("COMMENT_CHATS") or {}
    if not comments:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    row = 1
    for comment in comments:
        text += f"**{row} -** `{comment}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanCommentList")
async def cleancommentlist(event):
    await event.edit(client.STRINGS["wait"])
    comments = client.DB.get_key("COMMENT_CHATS") or {}
    if not comments:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    client.DB.del_key("COMMENT_CHATS")
    await event.edit(client.getstrings(STRINGS)["clean"])
    
@client.Command(onlysudo=False, allowedits=False)
async def autocomment(event):
    if not event.is_group or not event.fwd_from or not event.fwd_from.saved_from_peer: return
    cmode = client.DB.get_key("COMMENT_MODE") or "OFF"
    comments = client.DB.get_key("COMMENT_CHATS") or {}
    if event.chat_id not in comments: return
    if cmode == "ON":
        info = comments[event.chat_id]
        getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
        jtime = datetime.now()
        VARS = {
            "TIME": jtime.strftime("%H:%M"),
            "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
            "HEART": random.choice(client.functions.HEARTS),
        }
        for VAR in VARS:
            getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
        await event.reply(getmsg)