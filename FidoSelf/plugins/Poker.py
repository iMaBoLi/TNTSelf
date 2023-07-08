from FidoSelf import client

__INFO__ = {
    "Category": "Practical",
    "Name": "Poker",
    "Info": {
        "Help": "To Setting Send Poker Sticker To Pokers!",
        "Commands": {
            "{CMD}Poker <On-Off>": None,
            "{CMD}PokerAll <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "pokerall": "**The Poker Mode Has Been {}!**",
    "pokerchat": "**The Poker Mode For This Chat Has Been {}!**",
}

@client.Command(command="Poker (On|Off)")
async def pokerchat(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = client.DB.get_key("POKER_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("POKER_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("POKER_CHATS", acChats)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["pokerchat"].format(showchange))

@client.Command(command="PokerAll (On|Off)")
async def pokerall(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("POKER_MODE", change)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["pokerall"].format(showchange))
 
@client.Command(onlysudo=False, allowedits=False)
async def poker(event):
    if event.is_sudo or event.is_bot or not event.text or "😐" not in event.text: return
    pomode = client.DB.get_key("POKER_MODE") or "OFF"
    pochats = client.DB.get_key("POKER_CHATS") or []
    if pomode == "ON" or event.chat_id in pochats:
        await event.reply("😐")