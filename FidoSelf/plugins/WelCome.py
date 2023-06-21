from FidoSelf import client
from telethon import events, functions
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
            "{CCMDCleanWelcomeList": None,
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
    
@client.Command(command="DelWelcome (.*)")
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
        client.LOGS.error(str(1))
        welcomemode = client.DB.get_key("WELCOME_MODE") or "OFF"
        chats = client.DB.get_key("WELCOME_CHATS") or {}
        client.LOGS.error(str(2))
        if event.chat_id not in chats: return
        client.LOGS.error(str(3))
        if welcomemode == "ON":
            client.LOGS.error(str(4))
            info = chats[event.chat_id]
            getmsg = await client.get_messages(int(info["chat_id"]), ids=int(info["msg_id"]))
            getmsg.text = await client.AddVars(getmsg.text, event)
            client.LOGS.error(str(5))
            await event.reply(getmsg)