from FidoSelf import client

__INFO__ = {
    "Category": "Funs",
    "Plugname": "Len",
    "Pluginfo": {
        "Help": "To Get Len Of Characters In Message!",
        "Commands": {
            "{CMD}SLen <Reply(Text)>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "num": "**The Number Of Characters:** ( `{}` )",
}

@client.Command(command="SLen")
async def len(event):
    await event.edit(client.STRINGS["wait"])
    mtype = client.functions.mediatype(event.reply_message)
    if not event.is_reply or not event.reply_message.text:
        medias = client.STRINGS["replyMedia"]
        media = medias["Text"]
        rtype = medias[mtype]
        text = client.STRINGS["replyMedia"]["Main"].format(rtype, media)
        return await event.edit(text)
    text = event.reply_message.text
    await event.edit(STRINGS["num"].format(len(text)))