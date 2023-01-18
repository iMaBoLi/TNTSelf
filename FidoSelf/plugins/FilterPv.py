from FidoSelf import client

@client.Command(pattern=f"(?i)^\{client.cmd}AddFilterPv (.*)")
async def addfilterpv(event):
    await event.edit(client.get_string("Wait"))
    word = str(event.pattern_match.group(1))
    filterpvs = client.DB.get_key("FILTER_PVS") or []
    if word in filterpvs:
        return await event.edit(client.get_string("FilterPv_1").format(word))
    filterpvs.append(word)
    client.DB.set_key("FILTER_PVS", filterpvs)
    await event.edit(client.get_string("FilterPv_2").format(word))
    
@client.Command(pattern=f"(?i)^\{client.cmd}DelFilterPv (.*)")
async def delfilterpv(event):
    await event.edit(client.get_string("Wait"))
    word = str(event.pattern_match.group(1))
    filterpvs = client.DB.get_key("FILTER_PVS") or []
    if word not in filterpvs:
        return await event.edit(client.get_string("FilterPv_3").format(word))
    filterpvs.remove(word)
    client.DB.set_key("FILTER_PVS", filterpvs)
    await event.edit(client.get_string("FilterPv_4").format(word))
    
@client.Command(pattern=f"(?i)^\{client.cmd}FilterPvList$")
async def filterpvlist(event):
    await event.edit(client.get_string("Wait"))
    filterpvs = client.DB.get_key("FILTER_PVS") or []
    if not filterpvs:
        return await event.edit(client.get_string("FilterPv_5"))
    text = client.get_string("FilterPv_6")
    row = 1
    for word in filterpvs:
        text += f"**{row} -** `{word}`\n"
        row += 1
    await event.edit(text)

@client.Command(pattern=f"(?i)^\{client.cmd}CleanFilterPvList$")
async def cleanfilterpv(event):
    await event.edit(client.get_string("Wait"))
    filterpvs = client.DB.get_key("FILTER_PVS") or []
    if not filterpvs:
        return await event.edit(client.get_string("FilterPv_5"))
    client.DB.del_key("FILTER_PVS")
    await event.edit(client.get_string("FilterPv_7"))
    
@client.Command(sudo=False, edits=False)
async def filterpv(event):
    if not event.text or not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    words = client.DB.get_key("FILTER_PVS") or []
    if not words: return
    for word in words:
        if word in event.text:
            try:
                await event.delete()
            except:
                pass
