from TNTSelf import client
from telethon import events, functions
from jdatetime import datetime
import aiocron
import random

__INFO__ = {
    "Category": "Groups",
    "Name": "Welcome",
    "Info": {
        "Help": "To Manage Auto Welcome In The Chats!",
        "Commands": {
            "{CMD}Welcome <On-Off>": {
                "Help": "To Turn On-Off Welcome Message",
            },
            "{CMD}SetWelcome": {
                "Help": "To Set Welcome Message",
                "Reply": ["Message", "Media"],
                "Vars": ["TIME", "DATE", "HEART", "NAME", "MENTION", "USERNAME", "TITLE", "CHATUSERNAME", "COUNT"],
            },
            "{CMD}DelWelcome": {
                "Help": "To Delete Welcome Message",
            },
            "{CMD}GetWelcome": {
                "Help": "To Getting Welcome Message",
            },
            "{CMD}WelcomeList": {
                "Help": "To Getting Welcome List",
            },
            "{CMD}CleanWelcomeList": {
                "Help": "To Cleaning Welcome List",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Welcome Mode Has Been {}!**",
    "setwelcome": "**{STR} The Welcome Message For This Chat Has Been Saved!**",
    "notsave": "**{STR} The Welcome Message For This Chat Is Not Saved!**",
    "delwelcome": "**{STR} The Welcome Message For This Chat Has Been Removed!**",
    "empty": "**{STR} The Welcome List Is Empty!**",
    "list": "**{STR} The Welcome List:**\n\n",
    "aempty": "**{STR} The Welcome List Is Already Empty**",
    "clean": "**{STR} The Welcome List Has Been Cleaned!**"
}

@client.Command(command="Welcome (On|Off)")
async def welcomemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("WELCOME_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="SetWelcome")
async def setwelcome(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    if reply:= event.checkReply():
        return await event.edit(reply)
    welcomes = event.client.DB.get_key("WELCOME_CHATS") or {}
    info = await event.reply_message.save()
    welcomes.update({event.chat_id: info})
    event.client.DB.set_key("WELCOME_CHATS", welcomes)
    await event.edit(client.getstrings(STRINGS)["setwelcome"])
    
@client.Command(command="DelWelcome")
async def delwelcome(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    welcomes = event.client.DB.get_key("WELCOME_CHATS") or {}
    if event.chat_id not in welcomes:
        return await event.edit(client.getstrings(STRINGS)["notsave"])  
    del welcomes[event.chat_id]
    event.client.DB.set_key("WELCOME_CHATS", welcomes)
    await event.edit(client.getstrings(STRINGS)["delwelcome"])

@client.Command(command="GetWelcome")
async def getwelcome(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group:
        return await event.edit(client.STRINGS["only"]["Group"])
    comments = event.client.DB.get_key("WELCOME_CHATS") or {}
    if event.chat_id not in comments:
        return await event.edit(client.getstrings(STRINGS)["notsave"])
    info = comments[event.chat_id]
    getmsg =  await event.client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
    await event.respond(getmsg)
    await event.delete()
    
@client.Command(command="WelcomeList")
async def welcomelist(event):
    await event.edit(client.STRINGS["wait"])
    welcomes = event.client.DB.get_key("WELCOME_CHATS") or {}
    if not welcomes:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, welcome in enumerate(welcomes):
        text += f"**{row + 1} -** `{welcome}`\n"
    await event.edit(text)

@client.Command(command="CleanWelcomeList")
async def cleanwelcomelist(event):
    await event.edit(client.STRINGS["wait"])
    welcomes = event.client.DB.get_key("WELCOME_CHATS") or {}
    if not welcomes:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("WELCOME_CHATS")
    await event.edit(client.getstrings(STRINGS)["clean"])
    
@client.on(events.ChatAction())
async def autowelcome(event):
    if event.user_joined or event.added_by:
        welcomemode = event.client.DB.get_key("WELCOME_MODE") or "OFF"
        chats = event.client.DB.get_key("WELCOME_CHATS") or {}
        if event.chat_id not in chats: return
        if welcomemode == "ON":
            info = chats[event.chat_id]
            getmsg =  await event.client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
            chat = await event.get_chat()
            user = await event.get_user()
            jtime = datetime.now()
            VARS = {
                "TIME": jtime.strftime("%H:%M"),
                "DATE": jtime.strftime("%Y") + "/" + jtime.strftime("%m") + "/" + jtime.strftime("%d"),
                "HEART": random.choice(client.functions.HEARTS),
                "FIRSTNAME": user.first_name,
                "MENTION": client.functions.mention(user),
                "USERNAME": user.username or "---",
                "TITLE": chat.title,
                "CHATUSERNAME": chat.username or "---",
                "COUNT": chat.participants_count or "---",
            }
            for VAR in VARS:
                getmsg.text = getmsg.text.replace(VAR, VARS[VAR])
            await event.reply(getmsg)