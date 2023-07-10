from FidoSelf import client
from telethon import types

__INFO__ = {
    "Category": "Funs",
    "Name": "Contact",
    "Info": {
        "Help": "To Create Contact With Name And Phone!",
        "Commands": {
            "{CMD}SContact <Name>:<Phone": {
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

@client.Command(command="SContact (.*)\:(.*)")
async def createcontact(event):
    await event.edit(client.STRINGS["wait"])
    name = str(event.pattern_match.group(1))
    phone = str(event.pattern_match.group(2))
    caption = client.getstrings(STRINGS)["created"].format(name, phone)
    contact = types.InputMediaContact(phone_number=phone, first_name=name, last_name="", vcard="0")
    await client.send_file(event.chat_id, contact)
    await event.delete()