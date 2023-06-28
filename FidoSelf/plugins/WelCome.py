from FidoSelf import client
from telethon import events, functions
from jdatetime import datetime
import aiocron
import random

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Welcome",
    "Pluginfo": {
        "Help": "To Manage Auto Welcome In The Chats!",
        "Commands": {
            "{CMD}Welcome <On-Off>": None,
            "{CMD}SetWelcome <Reply>": None,
            "{CMD}DelWelcome": None,
            "{CMD}GetWelcome": None,
            "{CMD}WelcomeList": None,
            "{CMD}CleanWelcomeList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Welcome Mode Has Been {}!**",
    "setwelcome": "**The Welcome Message For This Chat Has Been Saved!**",
    "notsave": "**The Welcome Message For This Chat Is Not Saved!**",
    "delwelcome": "**The Welcome Message For This Chat Has Been Removed!**",
    "empty": "**The Welcome List Is Empty!**",
    "list": "**The Welcome List:**\n\n",
    "aempty": "**The Welcome List Is Already Empty**",
    "clean": "**The Welcome List Has Been Cleaned!**",
}

@client.Command(command="Welcome (On|Off)")
async def welcomemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("WELCOME_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="SetWelcome")
async def setwelcome(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    reply, _ = event.checkReply()
    if reply: return await event.edit(reply)
    welcomes = client.DB.get_key("WELCOME_CHATS") or {}
    info = await event.reply_message.save()
    welcomes.update({event.chat_id: info})
    client.DB.set_key("WELCOME_CHATS", welcomes)
    await event.edit(STRINGS["setwelcome"])
    
@client.Command(command="DelWelcome")
async def delwelcome(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    welcomes = client.DB.get_key("WELCOME_CHATS") or {}
    if event.chat_id not in welcomes:
        return await event.edit(STRINGS["notsave"])  
    del welcomes[event.chat_id]
    client.DB.set_key("WELCOME_CHATS", welcomes)
    await event.edit(STRINGS["delwelcome"])

@client.Command(command="GetWelcome")
async def getwelcome(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    comments = client.DB.get_key("WELCOME_CHATS") or {}
    if event.chat_id not in comments:
        return await event.edit(STRINGS["notsave"])
    info = comments[event.chat_id]
    getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await event.respond(getmsg)
    await event.delete()
    
@client.Command(command="WelcomeList")
async def welcomelist(event):
    await event.edit(client.STRINGS["wait"])
    welcomes = client.DB.get_key("WELCOME_CHATS") or {}
    if not welcomes:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for welcome in welcomes:
        text += f"**{row} -** `{welcome}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanWelcomeList")
async def cleanwelcomelist(event):
    await event.edit(client.STRINGS["wait"])
    welcomes = client.DB.get_key("WELCOME_CHATS") or {}
    if not welcomes:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("WELCOME_CHATS")
    await event.edit(STRINGS["clean"])
    
@client.on(events.ChatAction())
async def autowelcome(event):
    if event.user_joined or event.added_by:
        welcomemode = client.DB.get_key("WELCOME_MODE") or "OFF"
        chats = client.DB.get_key("WELCOME_CHATS") or {}
        if event.chat_id not in chats: return
        if welcomemode == "ON":
            info = chats[event.chat_id]
            getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
            chat = await event.get_chat()
            user = await event.get_user()
            jtime = datetime.now()
            VARS = {
                "TIME": jtime.strftime("%H:%M"),
                "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
                "HEART": random.choice(client.functions.HEARTS),
                "FIRSTNAME": user.first_name,
                "MENTION": client.mention(user),
                "USERNAME": user.username,
                "TITLE": chat.title,
                "CHATUSERNAME": chat.username,
                "COUNT": chat.participants_count,
            }
            for VAR in VARS:
                getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
            await event.reply(getmsg)