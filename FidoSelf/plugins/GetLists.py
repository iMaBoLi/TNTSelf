from FidoSelf import client
from telethon import Button

STRINGS = {
    "emptylist": "**{STR} The List Of Your Saved** ( `{}` ) **Is Empty!**",
    "getlist": "**{STR} List Of Your Saved** ( `{}` )**:**\n\n",
}

LISTS = {
    "Save": ["Saveds", "SAVED_LIST", 1],
    "Enemy": ["Enemies", "ENEMY_LIST", 1],
    "Timer": ["Timers", "TIMER_LIST", 1],
    "Until": ["Untils", "UNTIL_LIST", 1],
    "White": ["White Users", "WHITE_LIST", 1],
    "Black": ["Black Users", "BLACK_LIST", 1],
    "Name": ["Names", "NAME_LIST", 1],
    "Bio": ["Bios", "BIO_LIST", 1],
    "Photo": ["Photos", "PHOTO_LIST", 1],
    "Texttime": ["Text Times", "TEXTTIME_LIST", 1],
    "Echo": ["Echo Users" "ECHO_USERS", 1],
    "Repeat": ["Repeats", "REPEAT_LIST", 1],
    "Love": ["Loves", "LOVE_LIST", 1],
    "Lovetime": ["Love Times", "LOVETIME_LIST", 1],
    "Auto": ["Auto Chats", "AUTO_CHATS", 1],
    "Action": ["Action Chats", "ACTION_CHATS", 1],
    "Reaction": ["Reaction Chats", "REACTION_CHATS", 1],
    "Comment": ["Comment Chats" "COMMENT_CHATS", 1],
    "Welcome": ["Welcome Chats", "WELCOME_CHATS", 1],
    "Goodby": ["Goodby Chats", "GOODBY_CHATS", 1],
    "Mutepv": ["MutePv Users", "MUTEPV_USERS", 1],
    "Filterpv": ["FilterPv Words", "FILTERPV_WORDS", 1],
}

STRING = ""
for List in LISTS:
    STRING += List + "|"
STRING = STRING[:-1]

@client.Command(command=f"({STRING}) list")
async def getlists(event):
    await event.edit(client.STRINGS["wait"])
    inlist = event.pattern_match.group(1).title()
    listname = LISTS[inlist][0]
    dblist = LISTS[inlist][1]
    listtype = LISTS[inlist][2]
    lists = client.DB.get_key(dblist)
    if not lists:
        return await event.edit(client.getstrings(STRINGS)["emptylist"].format(listname))
    text = client.getstrings(STRINGS)["getlist"].format(listname)
    if listtype == 1:
        for row, item in enumerate(lists):
            text += f"**{row + 1} -** `{item}`\n"
    elif listtype == 2:
        for row, item in enumerate(lists):
            ititem = lists[item]
            text += f"**{row + 1} -** `{item}` ( `{ititem}` )\n"
    await event.edit(text)