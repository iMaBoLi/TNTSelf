from FidoSelf import client
from telethon import Button
import random
import secrets

__INFO__ = {
    "Category": "Tools",
    "Name": "Najva",
    "Info": {
        "Help": "To Create Private Messages For Users!",
        "Commands": {
            f"@{client.bot.me.username} Najva:<ID>,<Text>": {
               "Help": "To Create Najva",
                "Input": {
                    "<ID>": "UserID/Username Of User",
                    "<Text>": "Your Message ( Max: 50 )",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notfound": "**{STR} The Entered UserID/Username Is Not Found!**",
    "najva": "**{STR} The Najva For User** ( {} )\n\n**{STR} Only You Can Open Najva!**",
    "notyou": "{STR} This Najva Is Not For You!",
    "notnaj": "**{STR} This Najva Is Not Available!**",
}

NAJVAS = {}

@client.Inline(pattern="Najva\\:(.*)\,(.*)")
async def najva(event):
    inputid = event.pattern_match.group(1)
    message = event.pattern_match.group(2)
    userid = None
    inputid = int(inputid) if inputid.isdigit() else str(inputid)
    try:
        userinfo = await client.get_entity(inputid)
        if userinfo.to_dict()["_"] == "User":
            userid = userinfo.id
    except:
        pass
    if not userid:
        text = client.getstrings(STRINGS)["notfound"]
        return await event.answer([event.builder.article("Najva - ( User Not Found )", text=text)])
    if len(message) > 50:
        message = message[:50]
    token = secrets.token_hex(nbytes=5)
    NAJVAS.update({token: message})
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    text = client.getstrings(STRINGS)["najva"].format(mention)
    buttons = [[Button.inline("• Open Najva •", data=f"OpenNajva:{token}:{userid}")]]
    await event.answer([event.builder.article("FidoSelf - Najva", text=text, buttons=buttons)])
    
@client.Callback(data="OpenNajva\\:(.*)\\:(.*)", onlysudo=False)
async def opennajva(event):
    najtoken = event.data_match.group(1).decode('utf-8')
    userid = int(event.data_match.group(2).decode('utf-8'))
    if event.sender_id != userid:
        return await event.answer(client.getstrings(STRINGS)["notyou"], alert=True)
    if najtoken not in NAJVAS:
        return await event.edit(client.getstrings(STRINGS)["notnaj"])
    message = NAJVAS[najtoken]
    await event.answer(message, alert=True)