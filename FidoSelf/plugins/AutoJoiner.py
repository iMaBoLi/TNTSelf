from FidoSelf import client
from telethon import functions

@client.Cmd(pattern=f"(?i)^\{client.cmd}S(Join|Leave)$")
async def autojoiner(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    if not event.is_reply:
        return await event.edit(f"**{client.str} Please Reply To Message**")
    links = []
    for entity in event.reply_message.entities:
        if entity.to_dict()["_"] in ["MessageEntityMention", "MessageEntityUrl"]:
            links.append(event.reply_message.text[entity.offset:entity.offset+entity.length])
    for buttons in event.reply_message.buttons:
        for but in buttons:
            if but.url:
                links.append(but.url)
    if mode == "join":
        joined = 0
        for link in links:
            try:
                await client(functions.channels.JoinChannelRequest(channel=link))
                joined += 1
            except:
                pass
        await event.edit(f"**{client.str} The Join To** ( `{joined}` ) **Channel Was Completed!**")
    elif mode == "leave":
        leaved = 0
        for link in links:
            try:
                await client(functions.channels.LeaveChannelRequest(channel=link)) 
                leaved += 1
            except:
                pass
        await event.edit(f"**{client.str} The Leave From** ( `{leaved}` ) **Channel Was Completed!**")
