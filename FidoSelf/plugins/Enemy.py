from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random
import os

STRINGS = {
    "where": "**Select You Want This Enemy User To Be Saved For Where:**",
    "notall": "The User ( {} ) Is Alredy In Enemy List In {} Location!",
    "add": "**The User** ( {} ) **Is Added To Enemy List For ( `{}` ) Location!**",
}
WHERES = ["All", "Groups", "Pvs", "Here"]

@client.Command(command="AddEnemy ?(.*)?")
async def addenemy(event):
    await event.edit(client.STRINGS["wait"])
    result, userid = await event.userid(event.pattern_match.group(1))
    if not result and str(userid) == "Invalid":
        return await event.edit(client.STRINGS["getid"]["IU"])
    elif not result and not userid:
        return await event.edit(client.STRINGS["getid"]["UUP"])
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
    event = await client.get_ids(event)
    Enemies = client.DB.get_key("ENEMIES") or {}
    elist = []
    info = await client.get_entity(event.userid)
    for enemy in Enemies:
        if int(event.userid) == Enemies[enemy]["user_id"]:
            elist.append(Enemies[enemy])
    if not elist:
        return await event.edit("**The User** ( {client.mention(info)} ) **Not In Enemy Lists!**")    
    res = await client.inline_query(client.bot.me.username, f"delenemy:{event.userid}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Command(command="EnemyList")
async def enemylist(event):
    await event.edit(client.STRINGS["wait"])
    Enemies = client.DB.get_key("ENEMIES") or {}
    if not Enemies:
        return await event.edit("**The Bio List Is Empty!**")
    text = "**The Enemy List:**\n\n"
    row = 1
    for enemy in Enemies:
        text += f"""**{row}-** `{Enemies[enemy]["user_id"]}` - ( `{Enemies[enemy]["type"]}` - `{Enemies[enemy]["where"]}` )\n"""
        row += 1
    await event.edit(text)

@client.Command(command="DelEnemyPms (On|off)")
async def delenemypm(event):
    await event.edit(client.STRINGS["wait"])
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("ORGENEMY_DELETE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit("**The Delete Original Enemy Messages Mode Has Been {change}!**")

@client.Command(command="SetEnemySleep (\d*)")
async def setenemysleep(event):
    await event.edit(client.STRINGS["wait"])
    sleep = event.pattern_match.group(1)
    client.DB.set_key("ORGENEMY_SLEEP", str(sleep))
    await event.edit("**The Original Enemy Sleep Has Been Set To {client.utils.convert_time(int(sleep))}!**")

@client.Command(onlysudo=False, alowedits=False)
async def enemyfosh(event):
    if event.is_ch: return
    Enemies = client.DB.get_key("ENEMIES") or {}
    if not Enemies: return
    foshs = client.DB.get_key("FOSHS_FILE")
    if not foshs and not os.path.exists("FOSHS.txt"): return
    userid = event.sender_id
    sleep = client.DB.get_key("ENEMY_SLEEP") or 0
    delete = client.DB.get_key("ENEMYPV_DELETE") or "off"
    for where in Enemies:
        if where.startswith("CHAT-") and event.chat_id == int(where.replace("CHAT-", "")):
            if not os.path.exists("FOSHS.txt"):
                get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
                await get.download_media("FOSHS.txt")
            FOSHS = open("FOSHS.txt", "r").readlines()
            await asyncio.sleep(int(sleep))
            if delete == "on" and event.is_private:
                await event.reply(random.choice(FOSHS))
                return await event.delete()
            return await event.reply(random.choice(FOSHS))
    if ("All" in Enemies and userid in Enemies["All"]) or ("Groups" in Enemies and userid in Enemies["Groups"] and event.is_group) or ("Pvs" in Enemies and userid in Enemies["Pvs"] and event.is_private):
        if not os.path.exists("FOSHS.txt"):
            get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
            await get.download_media("FOSHS.txt")
        FOSHS = open("FOSHS.txt", "r").readlines()
        await asyncio.sleep(int(sleep))
        if delete == "on" and event.is_private:
            await event.reply(random.choice(FOSHS))
            return await event.delete()
        return await event.reply(random.choice(FOSHS))

@client.Inline(pattern="addenemy\:(.*)\:(.*)")
async def inlineenemy(event):
    chatid = int(event.pattern_match.group(1))
    userid = int(event.pattern_match.group(2))
    text = STRINGS["where"]
    buttons = []
    for where in WHERES:
        where = where if where != "Here" else "CHAT-" + str(chatid)
        buttons.append(Button.inline(f"• {where} •", data=f"addenemy:{chatid}:{userid}:{where}"))
    buttons = list(client.functions.chunks(buttons, 3))
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data="closeenemy")])
    await event.answer([event.builder.article("FidoSelf - Enemy", text=text, buttons=buttons)])

@client.Callback(data="addenemy\:(.*)\:(.*)\:(.*)")
async def addenemies(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    userid = int(event.data_match.group(2).decode('utf-8'))
    where = event.data_match.group(3).decode('utf-8')
    userinfo = await client.get_entity(userid)
    Enemies = client.DB.get_key("ENEMIES") or {}
    if where in Enemies and userid in Enemies[where]:
        text = STRINGS["notall"].format(userinfo.first_name, where)
        return await event.answer(text, alert=True)
    Enemies[where].append(userid)
    client.DB.set_key("ENEMIES", Enemies)
    text = STRINGS["add"].format(client.mention(userinfo), where)
    await event.edit(text=text)

@client.Inline(pattern="delenemy\:(.*)")
async def delenemyinline(event):
    cmd = str(event.pattern_match.group(1))
    text = "**Please Choose From Which List You Want This Enemy User To Be Deleted:**"
    Enemies = client.DB.get_key("ENEMIES") or {}
    buttons = []
    for enemy in Enemies:
        info = Enemies[enemy]
        buttons.append([Button.inline(f"""( {info["where"].replace("chat", "")} ) - ( {info["type"]} )""", data=f"delenemydel:{enemy}")])
    await event.answer([event.builder.article("FidoSelf - Del Enemy", text=text, buttons=buttons)])

@client.Callback(data="delenemydel\:(.*)")
async def delenemies(event):
    enemy = str(event.data_match.group(1).decode('utf-8'))
    Enemies = client.DB.get_key("ENEMIES") or {}
    info = await client.get_entity(int(Enemies[enemy]["user_id"]))
    await event.edit(text=f"""**{client.str} The User** ( {client.mention(info)} ) **From Enemy List** ( `{Enemies[enemy]["where"]} -> {Enemies[enemy]["type"]}` ) **Has Been Deleted!**""")
    del Enemies[enemy]
    client.DB.set_key("ENEMIES", Enemies)

@client.Callback(data="closeenemy")
async def closeenemy(event):
    await event.edit(text="**The Enemy Panel Successfuly Closed!**")
