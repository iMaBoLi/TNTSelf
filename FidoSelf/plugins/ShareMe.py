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
    edit = await event.tryedit(client.STRINGS["wait"])
    contact = types.InputMediaContact(phone_number=client.me.phone or "", first_name=client.me.first_name or "", last_name=client.me.last_name or "", vcard="0")
    await client.send_file(event.chat_id, contact)
    await edit.delete()