from FidoSelf import client

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Delete Msg",
    "Pluginfo": {
        "Help": "To Delete Message In Chats!",
        "Commands": {
            "{CMD}Del <Count>": None,
            "{CMD}Del <Count><Reply>": "Delete Messages Of User!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "chatdel": "**The** ( `{}` ) **Message In This Chat Was Deleted!**",
    "userdel": "**The** ( `{}` ) **Message From User** ( {} ) **In This Chat Was Deleted!**",
}

@client.Command(command="Del (\d*)")
async def deletemsg(event):
    await event.edit(client.STRINGS["wait"])
    limit = event.pattern_match.group(1)
    if not limit:
        if event.is_reply:
            await event.reply_message.delete(revoke=True)
        return await event.delete(revoke=True)
    if event.is_reply:
        mention = client.mention(event.reply_message.sender)
        count = 0
        async for message in client.iter_messages(event.chat_id, from_user=event.reply_message.sender_id, offset_id=(event.id - 1), limit=limit):
            await message.delete(revoke=True)
            count += 1
        await event.edit(STRINGS["userdel"].format(count, mention))
    else:
        count = 0
        async for message in client.iter_messages(event.chat_id, offset_id=(event.id - 1), limit=limit):
            await message.delete(revoke=True)
            count += 1
        await event.edit(STRINGS["chatdel"].format(count))