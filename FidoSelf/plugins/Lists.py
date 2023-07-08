from FidoSelf import client
from telethon import Button

__INFO__ = {
    "Category": "Setting",
    "Name": "Lists",
    "Info": {
        "Help": "To Get Lists Of Your Saveds Items!",
        "Commands": {
            "{CMD}Lists": {
                "Help": "To Get Lists Panel",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "main": "**ᯓ Dear** ( {} )\n\n    **✾ Please Select The List You Want:**",
    "emptylist": "✾ The List Of Your {} Was Empty!",
    "getlist": "**✾ The List Of Your {}:**\n\n",
    "cleanlist": "**✾ The List Of Your {} Has Been Cleaned!**",
    "closelists": "**☻ The Lists Panel Successfully Closed!**",
}

LISTS = {
    "Saves": "SAVED_LIST",
    "Enemy Users": "ENEMY_LIST",
    "White Users": "WHITE_LIST",
    "Black Users": "BLACK_LIST",
    "Names": "NAME_LIST",
    "Bios": "BIO_LIST",
    "Photos": "PHOTO_LIST",
    "Text Times": "TEXTTIME_LIST",
    "Auto Chats": "AUTO_CHATS",
    "Action Chats": "ACTION_CHATS",
    "Reaction Chats": "REACTION_CHATS",
    "Echo Users": "ECHO_USERS",
    "Love Users": "LOVE_LIST",
    "Love Times": "LOVETIME_LIST",
    "Comment Chats": "COMMENT_CHATS",
    "WelCome Chats": "WELCOME_CHATS",
    "GoodBy Chats": "GOODBY_CHATS",
    "MutePv Users": "MUTEPV_USERS",
    "FilterPv Words": "FILTERPV_WORDS",
}

@client.Command(command="Lists")
async def lists(event):
    await event.edit(client.getstrings()["wait"])
    res = await client.inline_query(client.bot.me.username, "Lists")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Lists")
async def inlinelists(event):
    text = client.getstrings(STRINGS)["main"].format(client.functions.mention(client.me))
    buttons = []
    for slist in LISTS:
        sname = "• " + slist + " •"
        buttons.append(Button.inline(sname, data=f"GetList:{slist}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.getstrings()["inline"]["Close"], data="CloseLists")])
    await event.answer([event.builder.article("FidoSelf - Lists", text=text, buttons=buttons)])

@client.Callback(data="Lists")
async def calllists(event):
    text = client.getstrings(STRINGS)["main"].format(client.functions.mention(client.me))
    buttons = []
    for slist in LISTS:
        sname = "• " + slist + " •"
        buttons.append(Button.inline(sname, data=f"GetList:{slist}"))
    buttons = list(client.functions.chunks(buttons, 2))
    buttons.append([Button.inline(client.getstrings()["inline"]["Close"], data="CloseLists")])
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="GetList\:(.*)")
async def getlistitems(event):
    listname = str(event.data_match.group(1).decode('utf-8'))
    getdb = LISTS[listname]
    lists = client.DB.get_key(getdb)
    if not lists:
        return await event.answer(client.getstrings(STRINGS)["emptylist"].format(listname), alert=True)
    text = client.getstrings(STRINGS)["getlist"].format(listname)
    for row, item in enumerate(lists):
        text += f"**{row + 1} -** `{item}`\n"
    buttons = [[Button.inline(client.getstrings()["inline"]["Clean"], data=f"CleanList:{listname}")], [Button.inline(client.getstrings()["inline"]["Back"], data="Lists"), Button.inline(client.getstrings()["inline"]["Close"], data="CloseLists")]]
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="CleanList\:(.*)")
async def cleanlist(event):
    listname = str(event.data_match.group(1).decode('utf-8'))
    getdb = LISTS[listname]
    client.DB.del_key(getdb)
    text = client.getstrings(STRINGS)["cleanlist"].format(listname)
    await event.edit(text=text)

@client.Callback(data="CloseLists")
async def closelists(event):
    text = client.getstrings(STRINGS)["closelists"]
    await event.edit(text=text)