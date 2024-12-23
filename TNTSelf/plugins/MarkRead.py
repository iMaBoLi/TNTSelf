from TNTSelf import client

__INFO__ = {
    "Category": "Manage",
    "Name": "MarkRead",
    "Info": {
        "Help": "To Mark Read Messages In Chats!",
        "Commands": {
            "{CMD}Read <On-Off>": {
                "Help": "To Turn On-Off Mark Read For This Chat",
            },
            "{CMD}ReadAll <On-Off>": {
                "Help": "To Turn On-Off Mark Read For All Chats",
            },
            "{CMD}ReadPv <On-Off>": {
                "Help": "To Turn On-Off Mark Read For Pvs",
            },
            "{CMD}ReadGp <On-Off>": {
                "Help": "To Turn On-Off Mark Read For Groups",
            },
            "{CMD}ReadCh <On-Off>": {
                "Help": "To Turn On-Off Mark Read For Channels",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "markchat": "**{STR} The MarkRead Mode For This Chat Has Been {}!**",
    "markread": "**{STR} The MarkRead {} Messages Mode Has Been {}!**"
}

@client.Command(command="Read (On|Off)")
async def readchat(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = event.client.DB.get_key("READ_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            event.client.DB.set_key("READ_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            event.client.DB.set_key("READ_CHATS", acChats)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["markchat"].format(showchange))

@client.Command(command="Read(All|Pv|Gp|Ch) (On|Off)")
async def readmode(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1)
    change = event.pattern_match.group(2).upper()
    setmode = "READ" + type.upper() + "_MODE"
    event.client.DB.set_key(setmode, change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    Types = {
        "All": "All",
        "Pv": "Pvs",
        "Gp": "Groups",
        "Ch": "Channels",
    }
    await event.edit(client.getstrings(STRINGS)["markread"].format(Types[type.title()], showchange))

@client.Command(onlysudo=False)
async def mark(event):
    chats = event.client.DB.get_key("READ_CHATS") or []
    all = event.client.DB.get_key("READALL_MODE") or "OFF"
    pv = event.client.DB.get_key("READPV_MODE") or "OFF"
    gp = event.client.DB.get_key("READGP_MODE") or "OFF"
    ch = event.client.DB.get_key("READCH_MODE") or "OFF"
    if all == "ON" or (event.chat_id in chats) or (pv == "ON" and event.is_private) or (gp == "ON" and event.is_group) or (ch == "ON" and event.is_ch):
        await event.client.send_read_acknowledge(event.chat_id)