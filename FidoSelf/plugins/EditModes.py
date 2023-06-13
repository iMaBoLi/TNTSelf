from FidoSelf import client

EDITS ={
    "Bold",
    "Mono",
    "Italic",
    "Underline",
    "Strike",
    "Spoiler",
    "Hashtag",
    "Mention",
}

@client.Command(alowedits=False)
async def editmodes(event):
    if not event.text or event.checkCmd(): return
    allmode = client.DB.get_key("EDITALL_MODE") or ""
    chats = client.DB.get_key("EDITCHATS_MODE") or {}
    lasttext = str(event.text)
    if allmode == "Bold" or (event.chat_id in chats and chats[event.chat_id] == "Bold"):
        await event.edit("**" + lasttext + "**")
    elif allmode == "Mono" or (event.chat_id in chats and chats[event.chat_id] == "Mono"):
        await event.edit("`" + lasttext + "`")
    elif allmode == "Italic" or (event.chat_id in chats and chats[event.chat_id] == "Italic"):
        await event.edit("__" + lasttext + "__")
    elif allmode == "Underline" or (event.chat_id in chats and chats[event.chat_id] == "Underline"):
        await event.edit("<u>" + lasttext + "</u>", parse_mode="HTML")
    elif allmode == "Strike" or (event.chat_id in chats and chats[event.chat_id] == "Strike"):
        await event.edit("~~" + lasttext + "~~")
    elif allmode == "Spoiler" or (event.chat_id in chats and chats[event.chat_id] == "Spoiler"):
        await event.edit("||" + lasttext + "||")
    elif allmode == "Hashtag" or (event.chat_id in chats and chats[event.chat_id] == "Hashtag"):
        lasttext = lasttext.replace(" ", "_")
        lasttext = lasttext.replace("\n", "_")
        await event.edit("#" + lasttext)
    elif allmode == "Mention" or (event.chat_id in chats and chats[event.chat_id] == "Mention"):
        if event.is_reply:
            userid = event.reply_message.sender_id
        elif event.is_private:
            userid = event.chat_id
        else:
            userid = event.sender_id
        text = f"[{event.text}](tg://user?id={userid})"
        await event.edit(text)
        