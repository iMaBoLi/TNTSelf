from FidoSelf import client

STRINGS = {
    "EN": {
        "ping": "^{STR} IM Online Forever!$",
        "bot": "^{STR} Bot Is Online!$",
    },
    "FA": {
        "ping": "^{STR} من همیشه آنلاین هستم!$",
        "bot": "^{STR} ربات آنلاین است!$",
    },
}

@client.Command(
    commands={
        "EN": "Ping",
        "FA": "پینگ",
     }
)
async def ping(event):
    text = client.get_string("ping", STRINGS)
    await event.edit(text)

@client.Command(
    commands={
        "EN": "Bot",
        "FA": "ربات",
     }
)
async def bot(event):
    text = client.get_string("bot", STRINGS)
    await event.edit(text)
