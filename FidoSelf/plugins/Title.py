from FidoSelf import client
from telethon import functions
import aiocron
import random

__INFO__ = {
    "Category": "Practical",
    "Plugname": "Title",
    "Pluginfo": {
        "Help": "To Manage Titles For Chats And Update Title Chats!",
        "Commands": {
            "{CMD}Title <On-Off>": None,
            "{CMD}AddTitle <Text>": None,
            "{CMD}DelTitle <Text>": None,
            "{CMD}TitleList": None,
            "{CMD}CleanTitleList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Title Mode Has Been {}!**",
    "onlychat": "**Please Send In Group Or Channel!**",
    "notall": "**The Title** ( `{}` ) **Already In Title List!**",
    "addtitle": "**The Title** ( `{}` ) **Is Added To Title List!**",
    "notin": "**The Title** ( `{}` ) **Is Not In Title List!**",
    "deltitle": "**The Title** ( `{}` ) **Deleted From Title List!**",
    "empty": "**The Title List Is Empty!**",
    "list": "**The Title List:**\n\n",
    "aempty": "**The Title List Is Already Empty**",
    "clean": "**The Title List Has Been Cleaned!**",
}

@client.Command(command="Title (On|Off)")
async def titlemode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("TITLE_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="AddTitle (.*)")
async def addtitle(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group and not event.is_ch:
        return await event.edit(STRINGS["onlychat"])
    newtitle = event.pattern_match.group(1)
    chatid = event.chat_id
    titles = client.DB.get_key("TITLE_CHATS") or {}
    if chatid not in titles:
        titles.update({chatid: []})
        client.DB.set_key("TITLE_CHATS", titles)
    if newtitle in titles[chatid]:
        return await event.edit(STRINGS["notall"].format(newtitle))
    titles[chatid].append(newtitle)
    client.DB.set_key("TITLE_CHATS", titles)
    await event.edit(STRINGS["addtitle"].format(newtitle))
    
@client.Command(command="DelTitle (.*)")
async def deltitle(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group and not event.is_ch:
        return await event.edit(STRINGS["onlychat"])
    deltitle = event.pattern_match.group(1)
    chatid = event.chat_id
    titles = client.DB.get_key("TITLE_CHATS") or {}
    if chatid not in titles:
        titles.update({chatid: []})
        client.DB.set_key("TITLE_CHATS", titles)
    if deltitle not in titles[chatid]:
        return await event.edit(STRINGS["notin"].format(deltitle))  
    titles[chatid].remove(deltitle)
    client.DB.set_key("TITLE_CHATS", titles)
    await event.edit(STRINGS["deltitle"].format(deltitle))
    
@client.Command(command="TitleList")
async def titlelist(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group and not event.is_ch:
        return await event.edit(STRINGS["onlychat"])
    chatid = event.chat_id
    titles = client.DB.get_key("TITLE_CHATS") or {}
    if chatid not in titles or not titles[chatid]:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for title in titles[chatid]:
        text += f"**{row} -** `{title}`\n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanTitleList")
async def cleantitlelist(event):
    await event.edit(client.STRINGS["wait"])
    if not event.is_group and not event.is_ch:
        return await event.edit(STRINGS["onlychat"])
    chatid = event.chat_id
    titles = client.DB.get_key("TITLE_CHATS") or {}
    if chatid not in titles or not titles[chatid]:
        return await event.edit(STRINGS["aempty"])
    del titles[chatid]
    client.DB.set_key("TITLE_CHATS", titles)
    await event.edit(STRINGS["clean"])

@aiocron.crontab("*/1 * * * *")
async def autotitle():
    lmode = client.DB.get_key("TITLE_MODE") or "OFF"
    if lmode == "ON":
        tichats = client.DB.get_key("TITLE_CHATS") or {}
        for chat in tichats:
            titles = tichats[chat]
            if titles:
                title = random.choice(titles)
                title = await client.AddVars(title)
                await client(functions.messages.EditChatTitleRequest(chat_id=int(chat), title=title))