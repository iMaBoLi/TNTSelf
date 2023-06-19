from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Plugname": "MarkRead",
    "Pluginfo": {
        "Help": "To Mark Read Messages In Chats!",
        "Commands": {
            "{CMD}Read <On-Off>": None,
            "{CMD}ReadAll <On-Off>": None,
            "{CMD}ReadPv <On-Off>": None,
            "{CMD}ReadGp <On-Off>": None,
            "{CMD}ReadCh <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "markchat": "**The MarkRead Mode For This Chat Has Been {}!**",
    "markread": "**The MarkRead {} Messages Mode Has Been {}!**",
}

@client.Command(command="Read (On|Off)")
async def readchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = client.DB.get_key("READ_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("READ_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("READ_CHATS", acChats)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["markchat"].format(ShowChange))

@client.Command(command="Read(All|Pv|Gp|Ch) (On|Off)")
async def readmode(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1)
    change = event.pattern_match.group(2).lower()
    setmode = "READ" + type.upper() + "_MODE"
    client.DB.set_key(setmode, change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    Types = {
        "All": "All",
        "Pv": "Pvs",
        "Gp": "Groups",
        "Ch": "Channels",
    }
    await event.edit(STRINGS["markread"].format(Types[type.title()], ShowChange))

@client.Command(onlysudo=False)
async def mark(event):
    chats = client.DB.get_key("READ_CHATS") or []
    all = client.DB.get_key("READALL_MODE") or "OFF"
    pv = client.DB.get_key("READPV_MODE") or "OFF"
    gp = client.DB.get_key("READGP_MODE") or "OFF"
    ch = client.DB.get_key("READCH_MODE") or "OFF"
    if all == "ON" or (event.chat_id in chats) or (pv == "ON" and event.is_private) or (gp == "ON" and event.is_group) or (ch == "ON" and event.is_ch):
        await client.send_read_acknowledge(event.chat_id)