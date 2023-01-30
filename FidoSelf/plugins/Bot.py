from FidoSelf import client
from FidoSelf.functions import runcmd

STRINGS = {
    "EN": {
        "ping": "^{STR} IM Online Forever!$",
        "bot": "^{STR} Bot Is Online!$",
        "reload": "^{STR} Reloading Bot ...$",
    },
    "FA": {
        "ping": "^{STR} من همیشه آنلاین هستم!$",
        "bot": "^{STR} ربات آنلاین است!$",
        "reload": "^{STR} در حال بازنشانی ربات ...$",
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

@client.Command(
    commands={
        "EN": "reload",
        "FA": "بازنشانی",
     }
)
async def reload(event):
    text = client.get_string("reload", STRINGS)
    await event.edit(text)
    await runcmd("python3 -m FidoSelf")
