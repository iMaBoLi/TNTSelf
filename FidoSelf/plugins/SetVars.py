from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetStr (.*)$")
async def messagesstarter(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    string = event.pattern_match.group(1)
    client.DB.set_key("MESSAGES_STARTER", str(string))
    client.str = str(string)
    await event.edit(f"**{client.str} The Messages Starter String Has Been Set To {string}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetCmd (.*)$")
async def cmdmessage(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    cmd = event.pattern_match.group(1)
    client.DB.set_key("SELF_CMD", str(cmd))
    client.cmd = str(cmd)
    await event.edit(f"**{client.str} The Self Commands Starter Has Been Set To {cmd}!**")

@client.Cmd(pattern=f"(?i)^.DelCmd$")
async def dcmdmessage(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    client.DB.del_key("SELF_CMD")
    client.cmd = "."
    await event.edit(f"**{client.str} The Self Commands Starter Has Been Deleted!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetRealm$")
async def realm(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    if not event.is_group:
        return await event.edit(f"**{client.str} Please Send In Group For Added Realm Chat!**")
    client.DB.set_key("REALM_CHAT", event.chat_id)
    client.realm = event.chat_id
    await event.edit(f"**{client.str} This Chat Is Saved For Realm Chat!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetBackCh$")
async def backch(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    if not event.is_ch:
        return await event.edit(f"**{client.str} Please Send In Channel For Added BackUp Channel!**")
    client.DB.set_key("BACKUP_CHANNEL", event.chat_id)
    client.backch = event.chat_id
    await event.edit(f"**{client.str} This Channel Is Saved For BackUp Channel!**")
