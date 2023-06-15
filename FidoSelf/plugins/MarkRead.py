from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Plugname": "MarkRead",
    "Pluginfo": {
        "Help": "To Mark Read Messages In Chats!",
        "Commands": {
            "{CMD}ReadAll <On-Off>": None,
            "{CMD}ReadPv <On-Off>": None,
            "{CMD}ReadGp <On-Off>": None,
            "{CMD}ReadCh <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

@client.Command(onlysudo=False)
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