from FidoSelf import client

__INFO__ = {
    "Category": "Tools",
    "Plugname": "Replace",
    "Pluginfo": {
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
    reply, _ = event.checkReply("Text")
    if reply: return await event.edit(reply)
    fword = str(event.pattern_match.group(1))
    tword = str(event.pattern_match.group(2))
    lasttext = event.reply_message.text
    newtext = event.reply_message.text.replace(fword, tword)
    if newtext != lasttext:
        if event.reply_message.out:
            await event.reply_message.edit(newtext)
        else:
            await event.reply_message.reply(newtext)
    await event.edit(STRINGS["replace"].format(fword, tword))