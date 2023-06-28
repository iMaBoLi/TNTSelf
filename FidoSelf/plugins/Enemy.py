from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random
import os

__INFO__ = {
    "Category": "Manage",
    "Plugname": "Enemy",
    "Pluginfo": {
        "Help": "To Seeting Enemy List And Send Foshs!",
        "Commands": {
            "{CMD}AddEnemy <Pv|Reply|UserId|Username>": None,
            "{CMD}DelEnemy <Pv|Reply|UserId|Username>": None,
            "{CMD}EnemyList": None,
            "{CMD}CleanEnemyList": None,
            "{CMD}SetEnemySleep <Time>": "Set Sleep For Send Fosh To Enemy!",
            "{CMD}DelEnemyPms <On-Off>": "Delete Pv Messages Of Enemies!",
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "where": "**Select You Want This Enemy User To Be Saved For Where:**",
    "notall": "The User ( {} ) Is Alredy In Enemy List In {} Location!",
    "add": "**The User** ( {} ) **Is Added To Enemy List For ( `{}` ) Location!**",
    "notin": "**The User** ( {} ) **Not In Enemy Lis!**",
    "wheredel": "**Select You Want This Enemy User To Be Deleted From Where:**",
    "del": "**The User** ( {} ) **From Enemy List For Location** ( `{}` ) **Has Been Deleted!**",
    "esleep": "**The Enemy Sleep Was Set To** ( `{}` )",
    "edelete": "**The Delete Enemy Pms Mode Has Been {}!**",
    "empty": "**The Enemy List Is Empty!**",
    "list": "**The Enemy List:**\n\n",
    "aempty": "**The Enwmy List Is Already Empty!**",
    "clean": "**The Enemy List Is Cleaned!**",
    "close": "**The Enemy Panel Successfuly Closed!**",
}
WHERES = ["All", "Groups", "Pvs", "Here"]

@client.Command(command="AddEnemy ?(.*)?")
async def addenemy(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    chatid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"addenemy:{chatid}:{userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="DelEnemy ?(.*)?")
async def delenemy(event):
    await event.edit(client.STRINGS["wait"])
    userid = await event.userid(event.pattern_match.group(1))
    if not userid:
        return await event.edit(client.STRINGS["getuserID"])
    Enemies = client.DB.get_key("ENEMIES") or {}
    if userid not in Enemies:
        uinfo = await client.get_entity(userid)
        mention = client.mention(uinfo)
        return await event.edit(STRINGS["notin"].format(mention))
    res = await client.inline_query(client.bot.me.username, f"delenemy:{userid}")
    if event.is_reply:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="EnemyList")
async def enemylist(event):
    await event.edit(client.STRINGS["wait"])
    Enemies = client.DB.get_key("ENEMIES") or {}
    if not Enemies:
        return await event.edit(STRINGS["empty"])
    text = STRINGS["list"]
    row = 1
    for enemy in Enemies:
        text += f"**{row}-** `{enemy}` \n"
        row += 1
    await event.edit(text)
    
@client.Command(command="CleanEnemyList")
async def cleanenemies(event):
    await event.edit(client.STRINGS["wait"])
    enemys = client.DB.get_key("ENEMIES") or []
    if not enemys:
        return await event.edit(STRINGS["aempty"])
    client.DB.del_key("ENEMIES")
    await event.edit(STRINGS["clean"])

@client.Command(command="SetEnemySleep (\d*)")
async def setenemysleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = event.pattern_match.group(1)
    client.DB.set_key("ENEMY_SLEEP", sleep)
    await event.edit(STRINGS["esleep"].format(client.functions.convert_time(int(sleep))))

@client.Command(command="DelEnemyPms (On|Off)")
async def delpms(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("ENEMY_DELETE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["edelete"].format(ShowChange))

@client.Command(onlysudo=False, allowedits=False)
async def enemyfosh(event):
    if event.is_white or event.is_ch: return
    userid = event.sender_id
    Enemies = client.DB.get_key("ENEMIES") or {}
    if userid not in Enemies: return
    if event.checkSpam(): return
    sleep = client.DB.get_key("ENEMY_SLEEP") or 0
    delete = client.DB.get_key("ENEMY_DELETE") or "OFF"
    if ("All" in Enemies[userid]) or ("Groups" in Enemies[userid] and event.is_group) or ("Pvs" in Enemies[userid] and event.is_private) or (str(event.chat_id) in Enemies[userid]):
        if os.path.exists(client.PATH + "FOSHS.txt"):
            FOSHS = open(client.PATH + "FOSHS.txt", "r").readlines()
        else:
            FOSHS = client.functions.FOSHS
        fosh = random.choice(FOSHS)
        await asyncio.sleep(int(sleep))
        await event.reply(fosh)
        if delete == "ON" and event.is_private:
            await event.delete()

@client.Inline(pattern="addenemy\:(.*)\:(.*)")
async def inlineenemy(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = STRINGS["where"]
    buttons = []
    for where in WHERES:
        swhere = where if where != "Here" else chatid
        buttons.append(Button.inline(f"• {where} •", data=f"addenemy:{chatid}:{userid}:{swhere}"))
    buttons = list(client.functions.chunks(buttons, 4))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closeenemy")])
    await event.answer([event.builder.article("FidoSelf - Enemy", text=text, buttons=buttons)])

@client.Callback(data="addenemy\:(.*)\:(.*)\:(.*)")
async def addenemies(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    where = event.data_match.group(3).decode('utf-8')
    userinfo = await client.get_entity(userid)
    Enemies = client.DB.get_key("ENEMIES") or {}
    if userid not in Enemies:
        Enemies.update({userid: []})
    if where in Enemies[userid]:
        text = STRINGS["notall"].format(userinfo.first_name, where)
        return await event.answer(text, alert=True)
    Enemies[userid].append(where)
    client.DB.set_key("ENEMIES", Enemies)
    text = STRINGS["add"].format(client.mention(userinfo), where)
    await event.edit(text=text)

@client.Inline(pattern="delenemy\:(.*)")
async def delenemyinline(event):
    userid = int(event.pattern_match.group(1))
    text = STRINGS["wheredel"]
    Enemies = client.DB.get_key("ENEMIES") or {}
    buttons = []
    for where in Enemies[userid]:
        buttons.append(Button.inline(f"• {where} •", data=f"delenemydel:{userid}:{where}"))
    await event.answer([event.builder.article("FidoSelf - Del Enemy", text=text, buttons=buttons)])

@client.Callback(data="delenemydel\:(.*)\:(.*)")
async def delenemies(event):
    userid = int(event.data_match.group(1).decode('utf-8'))
    where = str(event.data_match.group(2).decode('utf-8'))
    Enemies = client.DB.get_key("ENEMIES") or {}
    uinfo = await client.get_entity(userid)
    mention = client.mention(uinfo)
    Enemies[userid].remove(where)
    if not Enemies[userid]:
        del Enemies[userid]
    client.DB.set_key("ENEMIES", Enemies)
    text = STRINGS["del"].format(mention, where)
    await event.edit(text=text)

@client.Callback(data="closeenemy")
async def closeenemy(event):
    await event.edit(text=STRINGS["close"])