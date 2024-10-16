from TNTSelf import client
import string

__INFO__ = {
    "Category": "Funs",
    "Name": "Len",
    "Info": {
        "Help": "To Get Length Of Characters In Message!",
        "Commands": {
            "{CMD}GetLen": {
                "Help": "To Get Length",
                "Reply": ["Text"],
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "count": "**{STR} All Characters:** ( `{}` )\n\n**{STR} Words:** ( `{}` )\n**{STR} Numbers:** ( `{}` )",
}

@client.Command(command="GetLen")
async def getlen(event):
    await event.edit(client.STRINGS["wait"])
    if not event.reply_message or not event.reply_message.text:
        return await event.edit(client.STRINGS["replytext"])
    text = str(event.reply_message.text)
    allch = 0
    words = 0
    numbers = 0
    for character in text:
        allch += 1
        if character in string.ascii_letters:
            words += 1
        if character in string.digits:
            numbers += 1
    await event.edit(client.getstrings(STRINGS)["count"].format(allch, words, numbers))