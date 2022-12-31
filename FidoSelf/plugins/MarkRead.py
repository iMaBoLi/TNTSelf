from FidoSelf import client

@client.Cmd(pattern=f"(?i)^\{client.cmd}MarkRead(All|Pv|Gp|Ch) (On|off)$")
async def markread(event):
    await event.edit(client.get_string("Wait"))
    type = event.pattern_match.group(1).lower()
    key = "READ" + type.upper() + "_Mode"
    change = event.pattern_match.group(2).lower()
    changer = client.get_string("Change_1") if change == "on" else client.get_string("Change_2")
    client.DB.set_key(key, change)
    await event.edit(client.get_string("MarkRead_1").format(type.title(), changer))

@client.Cmd()
async def mark(event):
    all = client.DB.get_key("READALL_MODE") or "off"
    pv = client.DB.get_key("READPV_MODE") or "off"
    gp = client.DB.get_key("READGP_MODE") or "off"
    ch = client.DB.get_key("READCH_MODE") or "off"
    if all == "on":
        await client.send_read_acknowledge(event.chat_id)
    elif pv == "on" and event.is_private:
        await client.send_read_acknowledge(event.chat_id)
    elif gp == "on" and event.is_group:
        await client.send_read_acknowledge(event.chat_id)
    elif ch == "on" and event.is_ch:
        await client.send_read_acknowledge(event.chat_id)
