from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}AddEmoji (.*)")
async def addemoji(event):
    await event.edit(client.get_string("Wait"))
    data = event.pattern_match.group(1)
    emojis = client.DB.get_key("EMOJIES") or []
    for emoji in data.split(","):
        if emoji not in emojis:
            emojis.append(emoji)
    client.DB.set_key("EMOJIES", emojis)
    await event.edit(f"**{client.str} The Emojies** ( `{data}` ) **Is Added To Emoji List!**")  
    
@client.Command(pattern=f"(?i)^\{client.cmd}DelEmoji (.*)")
async def delemoji(event):
    await event.edit(client.get_string("Wait"))
    data = event.pattern_match.group(1)
    emojis = client.DB.get_key("EMOJIES") or []
    for emoji in data.split(","):
        if emoji in emojis:
            emojis.remove(emoji)
    client.DB.set_key("EMOJIES", emojis)
    await event.edit(f"**{client.str} The Emojies** ( `{data}` ) **Is Deleted From Emoji List!**")  

@client.Command(pattern=f"(?i)^\{client.cmd}EmojiList$")
async def emojilist(event):
    await event.edit(client.get_string("Wait"))
    emojis = client.DB.get_key("EMOJIES") or []
    if not emojis:
        return await event.edit(f"**{client.str} The Emoji List Is Empty!**")
    text = f"**{client.str} The Emoji List:**\n\n"
    row = 1
    for emoji in emojis:
        text += f"**{row} -** `{emoji}`\n"
        row += 1
    await event.edit(text)

@client.Command(pattern=f"(?i)^\{client.cmd}CleanEmojiList$")
async def cleanemojilist(event):
    await event.edit(client.get_string("Wait"))
    emojis = client.DB.get_key("EMOJIES") or []
    if not emojis:
        return await event.edit(f"**{client.str} The Emoji List Is Already Empty!**")
    client.DB.del_key("EMOJIES")
    await event.edit(f"**{client.str} The Emoji List Has Been Cleaned!**")
