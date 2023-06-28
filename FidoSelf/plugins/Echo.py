from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random
import os

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Echo",
    "Pluginfo": {
        "Help": "To Setting Echo Users And Send User Messages!",
        "Commands": {
            "{CMD}AddEcho <Pv|Reply|UserId|Username>": None,
            "{CMD}DelEcho <Pv|Reply|UserId|Username>": None,
            "{CMD}EchoList": None,
            "{CMD}CleanEchoList": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "where": "**Select You Want This Echo User To Be Saved For Where:**",
    "notall": "The User ( {} ) Is Alredy In Echo List In {} Location!",
    "add": "**The User** ( {} ) **Is Added To Echo List For ( `{}` ) Location!**",
    "notin": "**The User** ( {} ) **Not In Echo Lis!**",
    "wheredel": "**Select You Want This Echo User To Be Deleted From Where:**",
    "del": "**The User** ( {} ) **From Echo List For Location** ( `{}` ) **Has Been Deleted!**",
    "esleep": "**The Echo Sleep Was Set To** ( `{}` )",
    "empty": "**The Echo List Is Empty!**",
    "list": "**The Echo List:**\n\n",
    "aempty": "**The Echo List Is Already Empty!**",
    "clean": "**The Echo List Is Cleaned!**",
    "close": "**The Echo Panel Successfuly Closed!**",
}
WHERES = ["All", "Groups", "Pvs", "Here"]

@client.Command(command="AddEcho ?(.*)?")
async def addecho(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"addecho:{chatid}:{userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="DelEcho ?(.*)?")
async def delecho(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    Echos = client.DB.get_key("ECHOS") or {}
    if userid not in Echos:
        uinfo = await client.get_entity(userid)
        mention = client.mention(uinfo)
        return await event.edit(STRINGS["notin"].format(mention))
    res = await client.inline_query(client.bot.me.username, f"delecho:{userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="EchoList")
async def echolist(event):
    await event.edit(client.STRINGS["wait"])
    Echos = client.DB.get_key("ECHOS") or {}
    if not Echos:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for echo in Echos:
        text += f"**{row}-** `{echo}` \n"
        row += 1
    await event.edit(text)

@client.Command(command="CleanEchoList")
async def cleanechos(event):
    await event.edit(client.STRINGS["wait"])
    echos = client.DB.get_key("ECHOS") or []
    if not echos:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("ECHOS")
    await event.edit(STRINGS["clean"])

@client.Command(command="SetEchoSleep (\d*)")
async def setechosleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = event.pattern_match.group(1)
    client.DB.set_key("ECHO_SLEEP", sleep)
    await event.edit(STRINGS["esleep"].format(client.functions.convert_time(int(sleep))))

@client.Command(onlysudo=False, allowedits=False)
async def echofosh(event):
    if event.is_ch: return
    userid = event.sender_id
    Echos = client.DB.get_key("ECHOS") or {}
    if userid not in Echos: return
    sleep = client.DB.get_key("ECHO_SLEEP") or 0
    if ("All" in Echos[userid]) or ("Groups" in Echos[userid] and event.is_group) or ("Pvs" in Echos[userid] and event.is_private) or (str(event.chat_id) in Echos[userid]):
        await asyncio.sleep(int(sleep))
        message = await client.get_messages(event.chat_id, ids=event.id)
        await event.respond(message)

@client.Inline(pattern="addecho\:(.*)\:(.*)")
async def inlineecho(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = STRINGS["where"]
    buttons = []
    for where in WHERES:
        swhere = where if where != "Here" else chatid
        buttons.append(Button.inline(f"• {where} •", data=f"addecho:{chatid}:{userid}:{swhere}"))
    buttons = list(client.functions.chunks(buttons, 4))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closeecho")])
    await event.answer([event.builder.article("FidoSelf - Echo", text=text, buttons=buttons)])

@client.Callback(data="addecho\:(.*)\:(.*)\:(.*)")
async def addechos(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    where = event.data_match.group(3).decode('utf-8')
    userinfo = await client.get_entity(userid)
    Echos = client.DB.get_key("ECHOS") or {}
    if userid not in Echos:
        Echos.update({userid: []})
    if where in Echos[userid]:
        text = STRINGS["notall"].format(userinfo.first_name, where)
        return await event.answer(text, alert=True)
    Echos[userid].append(where)
    client.DB.set_key("ECHOS", Echos)
    text = STRINGS["add"].format(client.mention(userinfo), where)
    await event.edit(text=text)

@client.Inline(pattern="delecho\:(.*)")
async def delechoinline(event):
    userid = int(event.pattern_match.group(1))
    text = STRINGS["wheredel"]
    Echos = client.DB.get_key("ECHOS") or {}
    buttons = []
    for where in Echos[userid]:
        buttons.append(Button.inline(f"• {where} •", data=f"delechodel:{userid}:{where}"))
    await event.answer([event.builder.article("FidoSelf - Del Echo", text=text, buttons=buttons)])

@client.Callback(data="delechodel\:(.*)\:(.*)")
async def delechos(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    where = str(event.data_match.group(2).decode('utf-8'))
    Echos = client.DB.get_key("ECHOS") or {}
    uinfo = await client.get_entity(userid)
    mention = client.mention(uinfo)
    Echos[userid].remove(where)
    if not Echos[userid]:
        del Echos[userid]
    client.DB.set_key("ECHOS", Echos)
    text = STRINGS["del"].format(mention, where)
    await event.edit(text=text)

@client.Callback(data="closeecho")
async def closeecho(event):
    await event.edit(text=STRINGS["close"])