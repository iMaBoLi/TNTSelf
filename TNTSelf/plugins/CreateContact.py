from FidoSelf import client
from telethon import types

__INFO__ = {
    "Category": "Funs",
    "Name": "Contact",
    "Info": {
        "Help": "To Create Contact With Name And Phone!",
        "Commands": {
            "{CMD}SContact <Name>:<Phone>": {
                "Help": "To Create Contact",
                "Input": {
                    "<Name>": "Name Of Contact",
                    "<Phone>": "Phone Of Contact",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "created": "**{STR} The Contact With Name** ( `{}` ) **And Phone** ( `{}` ) **Has Been Created!**",
}

@client.Command(command="SContact (.*)\\:(.*)")
async def createcontact(event):
    await event.edit(client.STRINGS["wait"])
    name = str(event.pattern_match.group(1))
    phone = str(event.pattern_match.group(2))
    firstname = name.split(" ")[0]
    lastname = name.split(" ")[1] if len(name.split(" ")) > 1 else ""
    await event.edit(client.getstrings(STRINGS)["created"].format(name, phone))
    contact = types.InputMediaContact(phone_number=phone, first_name=firstname, last_name=lastname, vcard="0")
    await client.send_file(event.chat_id, contact)