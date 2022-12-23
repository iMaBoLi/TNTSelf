from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Scopy$")
async def scopy(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.reply_message:
        return await event.edit("**✥ Please Reply To Message For Copy!**")
    forward = await event.reply_message.forward_to(client.realm)
    client.DB.set_key("COPY_PASTE", str(forward.id))
    await event.edit("**✥ The Message Successfuly Copied !**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}Spaste$")
async def spaste(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mes = client.DB.get_key("COPY_PASTE")
    if not mes:
        return await event.edit("**✥ Not Message Have Been Copied !**")
    get = await client.get_messages(client.realm, ids=int(mes))
    if not get:
        client.DB.set_key("COPY_PASTE", None)
        return await event.edit("**✥ The Copied Message Has Been Deleted Copy Again!**")
    await client.send_message(event.chat_id, get)
    await event.delete()
