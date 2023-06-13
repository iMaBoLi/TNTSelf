from FidoSelf import client

STRINGS = {
    "chatdel": "**The** ( `{}` ) **Message In This Chat Was Deleted!**",
    "userdel": "**The** ( `{}` ) **Message From User** ( {} ) **In This Chat Was Deleted!**",
    "newadd": "**The Bio** ( `{}` ) **Added To Bio List!**",
    "delnot": "**The Bio** ( `{}` ) **Not In Bio List!**",
    "del": "**The Bio** ( `{}` ) **Deleted From Bio List!**",
    "empty": "**The Bio List Is Empty!**",
    "list": "**The Bio List:**\n\n",
    "aempty": "**The Bio List Is Already Empty!**",
    "clean": "**The Bio List Is Cleaned!**",
}

@client.Command(command="Del (\d*)")
async def deletemsg(event):
    await event.edit(client.STRINGS["wait"])
    limit = int(event.pattern_match.group(1))
    if event.private:
        if event.is_reply:
            mention = client.mention(event.reply_message.sender)
            count = 0
            async for message in client.iter_messages(event.chat_id, from_user=event.reply_message.sender_id, limit=limit):
                await message.delete(revoke=True)
                count += 1
            return await event.edit(STRINGS["userdel"].format(count, mention))
        else:
            count = 0
            async for message in client.iter_messages(event.chat_id, limit=limit):
                await message.delete(revoke=True)
                count += 1
            return await event.edit(STRINGS["chatdel"].format(count))