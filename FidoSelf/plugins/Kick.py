from FidoSelf import client
from telethon.errors import ChatAdminRequiredError

@client.Cmd(pattern=f"(?i)^\{client.cmd}Kick ?(.*)?")
async def kick(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    info = await client.get_entity(event.userid)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UU"))
    try:
        await client.edit_permissions(event.chat_id, event.userid, view_messages=False)
        await client.edit_permissions(event.chat_id, event.userid)
    except ChatAdminRequiredError:
        return await event.edit(client.get_string("Kick_1"))
    except Exception as e:
        return await event.edit(client.get_string("Kick_2").format(str(e)))
    await event.edit(client.get_string("Kick_3").format(client.mention(info)))

@client.Cmd(pattern=f"(?i)^\{client.cmd}Ban ?(.*)?")
async def ban(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    info = await client.get_entity(event.userid)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UU"))
    try:
        await client.edit_permissions(event.chat_id, event.userid, view_messages=False)
    except ChatAdminRequiredError:
        return await event.edit(client.get_string("Kick_1"))
    except Exception as e:
        return await event.edit(client.get_string("Kick_2").format(str(e)))
    await event.edit(client.get_string("Kick_3").format(client.mention(info)))

@client.Cmd(pattern=f"(?i)^\{client.cmd}UnBan ?(.*)?")
async def unban(event):
    await event.edit(client.get_string("Wait"))
    event = await client.get_ids(event)
    info = await client.get_entity(event.userid)
    if not event.userid:
        return await event.edit(client.get_string("Reply_UU"))
    try:
        await client.edit_permissions(event.chat_id, event.userid)
    except ChatAdminRequiredError:
        return await event.edit(client.get_string("Kick_1"))
    except Exception as e:
        return await event.edit(client.get_string("Kick_2").format(str(e)))
    await event.edit(client.get_string("Kick_3").format(client.mention(info)))
