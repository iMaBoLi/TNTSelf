from TNTSelf import client
from telethon import functions, types
import re
import os

__INFO__ = {
    "Category": "Account",
    "Name": "Add Contacts",
    "Info": {
        "Help": "To Add Contact To Your Account Contacts!",
        "Commands": {
            "{CMD}AddContacts": {
                "Help": "To Add To Contacts",
            },
            "Reply": ["File"],
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "notadd": "**{STR} The** ( `{}` ) **Contact Finded But None Of Them Were Added To Contacts!**",
    "adding": "**{STR} The** ( `{}` ) **Contact Finded And Adding To Contacts ...**",
    "addcon": "**{STR} The** ( `{}` ) **Contact Finded And** ( `{}` ) **Of Them Is Added To Contacts!**",
}

@client.Command(command="AddContacts")
async def addcontacts(event):
    await event.edit(client.STRINGS["wait"])
    if reply:= event.checkReply(["File"]):
        return await event.edit(reply)
    file = await event.reply_message.download_media(client.PATH)
    data = open(file, "r").read()
    datas = str(data).split("END")
    alls = re.findall("TEL", data)
    count = 0
    await event.edit(client.getstrings(STRINGS)["adding"].format(len(alls)))
    for cont in datas:
        number = re.search("TEL;CELL;PREF:(.*)", cont)
        name = re.search("FN:(.*)", cont)
        if number and name:
            try:
                contact = await client(functions.contacts.ImportContactsRequest(contacts=[types.InputPhoneContact(client_id=random.randrange(-2**63, 2**63), phone=number[1], first_name=name[1], last_name="")]))
                if contact.users:
                    count += 1
                exnumber = re.search("TEL;CELL:(.*)", cont)
                if exnumber:
                    contact = await client(functions.contacts.ImportContactsRequest(contacts=[types.InputPhoneContact(client_id=random.randrange(-2**63, 2**63), phone=exnumber[1], first_name=name[1], last_name="")]))
                    if contact.users:
                        count += 1
            except:
                continue
    os.remove(file)
    if not count:
        return await event.edit(client.getstrings(STRINGS)["notadd"].format(len(alls)))
    await event.edit(client.getstrings(STRINGS)["addcon"].format(len(alls), count))