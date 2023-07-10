from FidoSelf import client
from telethon import types

__INFO__ = {
    "Category": "Account",
    "Name": "Share Me",
    "Info": {
        "Help": "To Share My Account Contact!",
        "Commands": {
            "{CMD}ShareMe": {
                "Help": "To Share Contact",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(command="ShareMe")
async def shareme(event):
    await event.edit(client.STRINGS["wait"])
    contact = types.InputMediaContact(phone_number=client.me.phone, first_name=client.me.first_name, last_name=client.me.last_name, vcard="0")
    await client.send_file(event.chat_id, contact)
    await event.delete()