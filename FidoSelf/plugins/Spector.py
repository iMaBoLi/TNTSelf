from FidoSelf import client
from telethon import functions, Button
import asyncio

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
    "spector": "**❊ Welcome To Spector Menu:**\n\n    {STR} Select Options Below To Manage Spector Modes:**\n    **{STR} User:** ( {} )",
    "closespector": "**{STR} The Spector Panel Successfuly Closed!**",
}

SPECS = [
    "STATUS",
    "NAME",
    "USERNAME",
    "BIO",
    "PHOTO",
    "READ_PV",
    "READ_GROUP",
]

async def get_spector_buttons(userid, chatid):
    buttons = []
    for spec in SPECS:
        lists = client.DB.get_key(f"SPECTOR_{spec}") or []
        smode = client.STRINGS["inline"]["On"] if userid in lists else client.STRINGS["inline"]["Off"]
        cmode = "del" if userid in lists else "add"
        show = spec.replace("_", " ").title()
        buttons.append(Button.inline(f"{show} {smode}", data=f"SetSpector:{chatid}:{userid}:{spec}:{cmode}"))
    buttons = list(client.functions.chunks(buttons, 2))
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