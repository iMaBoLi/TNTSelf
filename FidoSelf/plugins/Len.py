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
    "count": "**The Number Of Characters:** ( `{}` )",
}

@client.Command(command="SLen")
async def getlen(event):
    await event.edit(client.STRINGS["wait"])
    reply, _ = event.checkReply("Text")
    if reply: return await event.edit(reply)
    text = event.reply_message.text
    await event.edit(STRINGS["count"].format(len(text)))