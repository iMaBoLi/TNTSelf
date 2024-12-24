from TNTSelf import client
from telethon import functions, types, Button
import asyncio, random
import os

__INFO__ = {
    "Category": "Manage",
    "Name": "Enemy",
    "Info": {
        "Help": "To Seeting Enemy List And Send Foshs!",
        "Commands": {
            "{CMD}AddEnemy": {
                "Help": "To Add User On Enemy List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}DelEnemy": {
                "Help": "To Delete User From Enemy List",
                "Getid": "You Must Reply To User Or Input UserID/UserName",
            },
            "{CMD}EnemyList": {
                "Help": "To Getting Enemy List",
            },
            "{CMD}CleanEnemyList": {
                "Help": "To Clean Enemy List",
            },
            "{CMD}SetEnemySleep <Time>": {
                "Help":"Set Sleep For Send Fosh To Enemy!",
                "Input": {
                    "<Time>": "Sleep Time ( 0-120 )seconds",
                },
            },
            "{CMD}DelEnemyPms <On-Off>": {
                "Help": "To Turn On-Off Delete Enemy Pms",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "where": "**{STR} Select You Want This Enemy User To Be Saved For Where:**",
    "notall": "**{STR} The User ( {} ) Is Alredy In Enemy List In {} Location!",
    "add": "**{STR} The User** ( {} ) **Is Added To Enemy List For ( `{}` ) Location!**",
    "notin": "**{STR} The User** ( {} ) **Not In Enemy Lis!**",
    "wheredel": "**{STR} Select You Want To Be Deleted** ( {} ) **From Where:**",
    "del": "**{STR} The User** ( {} ) **From Enemy List For Location** ( `{}` ) **Has Been Deleted!**",
    "esleep": "**{STR} The Enemy Sleep Was Set To** ( `{}` )",
    "edelete": "**{STR} The Delete Enemy Pms Mode Has Been {}!**",
    "empty": "**{STR} The Enemy List Is Empty!**",
    "list": "**{STR} The Enemy List:**\n\n",
    "aempty": "**{STR} The Enwmy List Is Already Empty!**",
    "clean": "**{STR} The Enemy List Is Cleaned!**",
    "close": "**{STR} The Enemy Panel Successfuly Closed!**"
}
WHERES = ["All", "Groups", "Pvs", "Here"]

@client.Command(command="AddEnemy", userid=True)
async def addenemy(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    chatid = event.chat_id
    res = await event.client.inline_query(event.client.bot.me.username, f"addenemy:{chatid}:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="DelEnemy", userid=True)
async def delenemy(event):
    await event.edit(client.STRINGS["wait"])
    if not event.userid:
        return await event.edit(client.STRINGS["user"]["all"])
    Enemies = event.client.DB.get_key("ENEMY_LIST") or {}
    if event.userid not in Enemies:
        uinfo = await event.client.get_entity(event.userid)
        mention = client.functions.mention(uinfo)
        return await event.edit(client.getstrings(STRINGS)["notin"].format(mention))
    res = await event.client.inline_query(event.client.bot.me.username, f"delenemy:{event.userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="EnemyList")
async def enemylist(event):
    await event.edit(client.STRINGS["wait"])
    Enemies = event.client.DB.get_key("ENEMY_LIST") or {}
    if not Enemies:
        return await event.edit(client.getstrings(STRINGS)["empty"])
    text = client.getstrings(STRINGS)["list"]
    for row, enemy in enumerate(Enemies):
        text += f"**{row + 1}-** `{enemy}` \n"
    await event.edit(text)
    
@client.Command(command="CleanEnemyList")
async def cleanenemies(event):
    await event.edit(client.STRINGS["wait"])
    enemys = event.client.DB.get_key("ENEMY_LIST") or []
    if not enemys:
        return await event.edit(client.getstrings(STRINGS)["aempty"])
    event.client.DB.del_key("ENEMY_LIST")
    await event.edit(client.getstrings(STRINGS)["clean"])

@client.Command(command="SetEnemySleep (\\d*)")
async def setenemysleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = int(event.pattern_match.group(1))
    sleep = sleep if sleep <= 120 else 120
    event.client.DB.set_key("ENEMY_SLEEP", sleep)
    await event.edit(client.getstrings(STRINGS)["esleep"].format(client.functions.convert_time(int(sleep))))

@client.Command(command="DelEnemyPms (On|Off)")
async def delpms(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("DELENEMY_MSGS", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["edelete"].format(showchange))

@client.Command(onlysudo=False, allowedits=False)
async def enemyfosh(event):
    if event.is_white or event.is_ch: return
    userid = event.sender_id
    Enemies = event.client.DB.get_key("ENEMY_LIST") or {}
    if userid not in Enemies: return
    sleep = event.client.DB.get_key("ENEMY_SLEEP") or 0
    delete = event.client.DB.get_key("DELENEMY_MSGS") or "OFF"
    if ("All" in Enemies[userid]) or ("Groups" in Enemies[userid] and event.is_group) or ("Pvs" in Enemies[userid] and event.is_private) or (str(event.chat_id) in Enemies[userid]):
        if event.checkSpam(): return
        FOSHS = event.client.DB.get_key("FOSH_LIST") or client.functions.FOSHS
        fosh = random.choice(FOSHS)
        await asyncio.sleep(int(sleep))
        await event.reply(fosh)
        if delete == "ON" and event.is_private:
            await event.delete()

@client.Inline(pattern="addenemy\\:(.*)\\:(.*)")
async def inlineenemy(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = client.getstrings(STRINGS)["where"]
    buttons = []
    for where in WHERES:
        swhere = where if where != "Here" else chatid
        buttons.append(Button.inline(f"• {where} •", data=f"addenemy:{chatid}:{userid}:{swhere}"))
    buttons = list(client.functions.chunks(buttons, 4))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closeenemy")])
    await event.answer([event.builder.article("TNTSelf - Enemy", text=text, buttons=buttons)])

@client.Callback(data="addenemy\\:(.*)\\:(.*)\\:(.*)")
async def addenemies(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    where = event.data_match.group(3).decode('utf-8')
    userinfo = await event.client.get_entity(userid)
    Enemies = event.client.DB.get_key("ENEMY_LIST") or {}
    if userid not in Enemies:
        Enemies.update({userid: []})
    if where in Enemies[userid]:
        text = client.getstrings(STRINGS)["notall"].format(userinfo.first_name, where)
        return await event.answer(text, alert=True)
    Enemies[userid].append(where)
    event.client.DB.set_key("ENEMY_LIST", Enemies)
    text = client.getstrings(STRINGS)["add"].format(client.functions.mention(userinfo), where)
    await event.edit(text=text)

@client.Inline(pattern="delenemy\\:(.*)")
async def delenemyinline(event):
    userid = int(event.pattern_match.group(1))
    uinfo = await event.client.user.get_entity(userid)
    mention = client.functions.mention(uinfo)
    text = client.getstrings(STRINGS)["wheredel"].format(mention)
    Enemies = event.client.DB.get_key("ENEMY_LIST") or {}
    buttons = []
    for where in Enemies[userid]:
        buttons.append(Button.inline(f"• {where} •", data=f"delenemydel:{userid}:{where}"))
    await event.answer([event.builder.article("TNTSelf - Del Enemy", text=text, buttons=buttons)])

@client.Callback(data="delenemydel\\:(.*)\\:(.*)")
async def delenemies(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    where = str(event.data_match.group(2).decode('utf-8'))
    Enemies = event.client.DB.get_key("ENEMY_LIST") or {}
    uinfo = await event.client.user.get_entity(userid)
    mention = client.functions.mention(uinfo)
    Enemies[userid].remove(where)
    if not Enemies[userid]:
        del Enemies[userid]
    event.client.DB.set_key("ENEMY_LIST", Enemies)
    text = client.getstrings(STRINGS)["del"].format(mention, where)
    await event.edit(text=text)

@client.Callback(data="closeenemy")
async def closeenemy(event):
    await event.edit(text=client.getstrings(STRINGS)["close"])