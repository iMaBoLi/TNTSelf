from FidoSelf import client

__INFO__ = {
    "Category": "Funs",
    "Name": "Len",
    "Info": {
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
    if not (event.reply_message or event.reply_message.text):
        return await event.edit(client.STRINGS["replytext"])
    text = event.reply_message.text
    await event.edit(client.getstrings(STRINGS)["count"].format(len(text)))