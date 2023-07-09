from FidoSelf import client
from telethon import Button
import random

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

@client.Inline(pattern="Najva\:(.*)\,(.*)")
async def najva(event):
    userid = event.pattern_match.group(1)
    message = event.pattern_match.group(2)
    userid = await client.functions.getuserid(event, userid)
    if not userid:
        text = client.getstrings(STRINGS)["notfound"]
        return await event.answer([event.builder.article("Najva - ( User Not Found )", text=text)])
    if len(message) > 50:
        message = message[:50]
    najid = random.randint(0, 999999)
    NAJVAS.update({najid: message})
    info = await client.get_entity(userid)
    mention = client.functions.mention(info)
    text = client.getstrings(STRINGS)["najva"].format(mention)
    buttons = [[Button.inline("• Open Najva •", data=f"OpenNajva:{najid}:{userid}")]]
    await event.answer([event.builder.article("FidoSelf - Najva", text=text, buttons=buttons)])
    
@client.Callback(data="OpenNajva\:(.*)\:(.*)", onlysudo=False)
async def opennajva(event):
    najid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    if event.sender_id != userid:
        return await event.answer(client.getstrings(STRINGS)["notyou"], alert=True)
    if najid not in NAJVAS:
        return await event.edit(client.getstrings(STRINGS)["notnaj"])
    message = NAJVAS[najid]
    await event.answer(message, alert=True)