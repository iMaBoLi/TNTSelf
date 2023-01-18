from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}Name (On|Off)$")
async def name(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("NAME_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(f"**{client.str} The Name Mode Has Been {change}!**")

@client.Command(pattern=f"(?i)^\{client.cmd}AddName (.*)$")
async def addname(event):
    await event.edit(client.get_string("Wait"))
    names = client.DB.get_key("NAMES") or []
    newname = str(event.pattern_match.group(1))
    if newname in names:
        return await event.edit(f"**{client.str} The Name** ( `{newname}` ) **Already In Name List!**")  
    names.append(newname)
    client.DB.set_key("NAMES", names)
    await event.edit(f"**{client.str} The Name** ( `{newname}` ) **Added To Name List!**")  
    
@client.Command(pattern=f"(?i)^\{client.cmd}DelName (.*)$")
async def delname(event):
    await event.edit(client.get_string("Wait"))
    names = client.DB.get_key("NAMES") or []
    newname = str(event.pattern_match.group(1))
    if newname not in names:
        return await event.edit(f"**{client.str} The Name** ( `{newname}` ) **Not In Name List!**")  
    names.remove(newname)
    client.DB.set_key("NAMES", names)
    await event.edit(f"**{client.str} The Name** ( `{newname}` ) **Deleted From Name List!**")  
    
@client.Command(pattern=f"(?i)^\{client.cmd}NameList$")
async def namelist(event):
    await event.edit(client.get_string("Wait"))
    names = client.DB.get_key("NAMES") or []
    if not names:
        return await event.edit(f"**{client.str} The Name List Is Empty!**")
    text = f"**{client.str} The Name List:**\n\n"
    row = 1
    for name in names:
        text += f"**{row} -** `{name}`\n"
        row += 1
    await event.edit(text)

@client.Command(pattern=f"(?i)^\{client.cmd}CleanNameList$")
async def cleannames(event):
    await event.edit(client.get_string("Wait"))
    names = client.DB.get_key("NAMES") or []
    if not names:
        return await event.edit(f"**{client.str} The Name List Is Already Empty!**")
    client.DB.del_key("NAMES")
    await event.edit(f"**{client.str} The Name List Is Cleared!**")
