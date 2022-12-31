from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}SelfAll (On|Off)$", selfmode=False)
async def selfallmode(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("SELF_ALL_MODE", mode)
    client.DB.del_key("SELF_MODE")
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(f"**{client.str} The Self Has Been {change} For All Chats!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}Self (On|Off)$", selfmode=False)
async def selfmode(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    mode = event.pattern_match.group(1).lower()
    chats = client.DB.get_key("SELF_MODE") or []
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    if mode == "off":
        if event.chat_id not in chats:
            chats.append(event.chat_id)
            client.DB.set_key("SELF_MODE", chats)
            await event.edit(f"**{client.str} The Self Has Been {change} In This Chat!**")
        else:
            await event.edit(f"**{client.str} The Self Is Already {change} In This Chat!**")
    elif mode == "on":
        if event.chat_id in chats:
            chats.remove(event.chat_id)
            client.DB.set_key("SELF_MODE", chats)
            await event.edit(f"**{client.str} The Self Has Been {change} In This Chat!**")
        else:
            await event.edit(f"**{client.str} The Self Is Already {change} In This Chat!**")
