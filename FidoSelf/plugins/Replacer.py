from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Name": "Replace",
    "Info": {
        "Help": "To Replace Words In Text!",
        "Commands": {
            "{CMD}SReplace <Word>,<Word>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "replace": "**The Replace Word** ( `{}` ) **Instead Of Word** ( `{}` ) **Completed!**",
}

@client.Command(command="SReplace (.*)\,(.*)")
async def replacer(event):
    await event.edit(client.STRINGS["wait"])
    if not (event.reply_message or event.reply_message.text):
        return await event.edit(client.STRINGS["replytext"])
    fword = str(event.pattern_match.group(1))
    tword = str(event.pattern_match.group(2))
    lasttext = event.reply_message.text
    newtext = event.reply_message.text.replace(fword, tword)
    if newtext != lasttext:
        await event.reply(newtext)
    await event.edit(STRINGS["replace"].format(fword, tword))