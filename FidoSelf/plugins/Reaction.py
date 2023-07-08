from FidoSelf import client
from telethon import functions, types
import asyncio
import random

__INFO__ = {
    "Category": "Practical",
    "Name": "Reaction",
    "Info": {
        "Help": "To Setting Send Chat Reactions To Messages!",
        "Commands": {
            "{CMD}Reaction <On-Off>": "Send Reaction For This Chat!",
            "{CMD}ReactionAll <On-Off>": "Send Reaction For All Chats!",
            "{CMD}SetReaction <Mode>": "Set Reaction Emoji!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "reactall": "**The Send Reaction To Messages Has Been {}!**",
    "reactchat": "**The Send Reaction To Messages For This Chat Has Been {}!**",
    "notreact": "**The Reaction** ( `{}` ) **Is Not Available!**",
    "setreact": "**The Reaction Emoji Was Set To** ( `{}` )",
}

@client.Command(command="Reaction (On|Off)")
async def reactionchat(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    acChats = client.DB.get_key("REACTION_CHATS") or []
    chatid = event.chat_id
    if change == "ON":
        if chatid not in acChats:
            acChats.append(chatid)
            client.DB.set_key("REACTION_CHATS", acChats)
    else:
        if chatid in acChats:
            acChats.remove(chatid)
            client.DB.set_key("REACTION_CHATS", acChats)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["reactchat"].format(showchange))

@client.Command(command="ReactionAll (On|Off)")
async def reactionall(event):
    await event.edit(client.getstrings()["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("REACTION_MODE", change)
    showchange = client.getstrings()["On"] if change == "ON" else client.getstrings()["Off"]
    await event.edit(client.getstrings(STRINGS)["reactall"].format(showchange))

@client.Command(command="SetReaction (.*)")
async def setreaction(event):
    await event.edit(client.getstrings()["wait"])
    emoji = event.pattern_match.group(1)
    if emoji not in (await getemojis()) and emoji != "random":
        return await event.edit(client.getstrings(STRINGS)["notreact"].format(emoji))
    client.DB.set_key("REACTION_EMOJI", emoji)
    await event.edit(client.getstrings(STRINGS)["setreact"].format(emoji.title()))

async def getemojis():
    result = await client(functions.messages.GetAvailableReactionsRequest(hash=0))
    reactlist = []
    for react in result.reactions:
        reactlist.append(react.reaction)
    return reactlist
 
@client.Command(onlysudo=False, allowedits=False)
async def reaction(event):
    if event.is_sudo or event.is_bot: return
    reacMode = client.DB.get_key("REACTION_MODE") or "OFF"
    reacChats = client.DB.get_key("REACTION_CHATS") or []
    emoji = client.DB.get_key("REACTION_EMOJI")
    if reacMode == "ON" or event.chat_id in reacChats:
        if emoji == "random":
            emoji = random.choice(await getemojis())
        try:
            await client(functions.messages.SendReactionRequest(peer=event.chat_id, msg_id=event.id, reaction=[types.ReactionEmoji(emoticon=emoji)]))
        except:
            if event.chat.megagroup or event.chat.broadcast:
                info = (await client(functions.channels.GetFullChannelRequest(event.chat_id))).full_chat
            else:
                info = (await client(functions.messages.GetFullChatRequest(event.chat_id))).full_chat
            if info.available_reactions:
                avreacts = info.available_reactions.reactions
                emoji = random.choice(avreacts)
                await client(functions.messages.SendReactionRequest(peer=event.chat_id, msg_id=event.id, reaction=[types.ReactionEmoji(emoticon=emoji.emoticon)]))