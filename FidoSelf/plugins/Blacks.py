from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddBlack ?(.*)?")
async def addblack(event):
    await event.edit(client.get_string("Wait").format(client.str))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(f"**{client.str} Please Enter Userid Or Username Or Reply To User Or Send In Private Chats!**")
    blacks = client.DB.get_key("BLACKS") or []
    if event.userid in blacks:
        return await event.edit(f"**{client.str} The User** ( {client.mention(event.userid)} ) **Already In Black List!**")  
    blacks.append(event.userid)
    client.DB.set_key("BLACKS", blacks)
    await event.edit(f"**{client.str} The User** ( {client.mention(event.userid)} ) **Is Added To Black List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}DelBlack ?(.*)?")
async def delblack(event):
    await event.edit(client.get_string("Wait").format(client.str))
    event = await client.get_ids(event)
    if not event.userid:
        return await event.edit(f"**{client.str} Please Enter Userid Or Username Or Reply To User Or Send In Private Chats!**")
    blacks = client.DB.get_key("BLACKS") or []
    if event.userid not in blacks:
        return await event.edit(f"**{client.str} The User** ( {client.mention(event.userid)} ) **Is Not In Black List!**")  
    blacks.remove(event.userid)
    client.DB.set_key("BLACKS", blacks)
    await event.edit(f"**{client.str} The User** ( {client.mention(event.userid)} ) **Deleted From Black List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}BlackList$")
async def blacklist(event):
    await event.edit(client.get_string("Wait").format(client.str))
    blacks = client.DB.get_key("BLACKS") or []
    if not blacks:
        return await event.edit(f"**{client.str} The Black List Is Empty!**")
    text = f"**{client.str} The Black List:**\n\n"
    row = 1
    for black in blacks:
        text += f"**{row} -** `{black}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanBlackList$")
async def cleanblacklist(event):
    await event.edit(client.get_string("Wait").format(client.str))
    blacks = client.DB.get_key("BLACKS") or []
    if not blacks:
        return await event.edit(f"**{client.str} The Black List Is Already Empty!**")
    client.DB.del_key("BLACKS")
    await event.edit(f"**{client.str} The Black List Has Been Cleaned!**")
