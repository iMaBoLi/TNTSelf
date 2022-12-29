from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}Bio (On|off)$")
async def bio(event):
    await event.edit(f"**{client.str} Processing . . .**")
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("BIO_MODE", mode)
    change = "Actived" if mode == "on" else "DeActived"
    await event.edit(f"**{client.str} The Bio Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddBio (.*)$")
async def addbio(event):
    await event.edit(f"**{client.str} Processing . . .**")
    bios = client.DB.get_key("BIOS") or []
    newbio = str(event.pattern_match.group(1))
    if newbio in bios:
        return await event.edit(f"**{client.str} The Bio** ( `{newbio}` ) **Already In Bio List!**")  
    bios.append(newbio)
    client.DB.set_key("BIOS", bios)
    await event.edit(f"**{client.str} The Bio** ( `{newbio}` ) **Is Added To Bio List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}DelBio (.*)$")
async def delbio(event):
    await event.edit(f"**{client.str} Processing . . .**")
    bios = client.DB.get_key("BIOS") or []
    newbio = str(event.pattern_match.group(1))
    if newbio not in bios:
        return await event.edit(f"**{client.str} The Bio** ( `{newbio}` ) **Not In Bio List!**")  
    bios.remove(newbio)
    client.DB.set_key("BIOS", bios)
    await event.edit(f"**{client.str} The Bio** ( `{newbio}` ) **Deleted From Bio List!**")  
    
@client.Cmd(pattern=f"(?i)^\{client.cmd}BioList$")
async def biolist(event):
    await event.edit(f"**{client.str} Processing . . .**")
    bios = client.DB.get_key("BIOS") or []
    if not bios:
        return await event.edit(f"**{client.str} The Bio List Is Empty!**")
    text = f"**{client.str} The Bio List:**\n\n"
    row = 1
    for bio in bios:
        text += f"**{row} -** `{bio}`\n"
        row += 1
    await event.edit(text)

@client.Cmd(pattern=f"(?i)^\{client.cmd}CleanBioList$")
async def cleanbios(event):
    await event.edit(f"**{client.str} Processing . . .**")
    bios = client.DB.get_key("BIOS") or []
    if not bios:
        return await event.edit(f"**{client.str} The Bio List Is Already Empty!**")
    client.DB.del_key("BIOS")
    await event.edit(f"**{client.str} The Bio List Is Cleared!**")
