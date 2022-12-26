from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddEnemy ?(.*)?")
async def addenemy(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_private and not event.userid:
        return await event.edit(f"**{client.str} Please Enter Userid Or Username Or Send In Private Chats!**")
    if not event.userid:
        event.userid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"addenemy:{event.userid}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Cmd(sudo=False, edits=False)
async def quicksupdate(event):
    if event.is_sudo or not event.text: return
    Enemies = client.DB.get_key("ENEMIES") or {}
    if not Enemies: return
    sleep = client.DB.get_key("ENEMY_SLEEP") or 0
    delete = client.DB.get_key("ENEMY_DELETE") or "off"
    for enemy in Enemies:
        info = Enemies[enemy]
        if not info["where"] == "All":
            if info["where"] == "Groups" and not event.is_group: continue
            if info["where"] == "Privates" and not event.is_private: continue
            if info["where"].startswith("chat") and not event.chat_id == int(info["where"].replace("chat", "")): continue
        try:
            if info["type"] == "Original":
                foshs = client.DB.get_key("ORGFOSHS_FILE") or {}
                if not foshs: continue
                getfile = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
                ffile = await getfile.download_media()
                Foshs = open(ffile, "r").readlines()
                await asyncio.sleep(int(sleep))
                await event.reply(random.choice(Foshs))
                if delete and event.is_private:
                    await event.delete()
                continue
            elif info["type"] == "Friend":
                foshs = client.DB.get_key("FRIENDFOSHS_FILE") or {}
                if not foshs: continue
                getfile = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
                ffile = await getfile.download_media()
                Foshs = open(ffile, "r").readlines()
                await asyncio.sleep(int(sleep))
                await event.reply(random.choice(Foshs))
                if delete and event.is_private:
                    await event.delete()
                continue
        except:
            continue

@client.Inline(pattern="addenemy\:(.*)")
async def inlineenemy(event):
    userid = event.pattern_match.group(1)
    text = f"**{client.str} Please Select Type Of This Enemy:"
    buttons = [[Button.inline("• Orginal Enemy •", data=f"addenemy:{userid}:Original"), Button.inline("• Friend Enemy •", data=f"addenemy:{userid}:Friend")]]
    buttons.append([Button.inline("🚫 Close 🚫", data="closeenemy")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Enemy", text=text, buttons=buttons)])

@client.Callback(data="addenemy\:(.*)")
async def addenemies(event):
    data = str(event.data_match.group(1).decode('utf-8')).split(":")
    userid = int(data[0])
    userinfo = await client.get_entity(userid)
    type = data[1]
    Enemies = client.DB.get_key("ENEMIES") or {}
    if len(data) == 2:
        text = f"**{client.str} Please Select You Want This Enemy User To Be Saved For Where:**"
        buttons = [[Button.inline("• All •", data=f"addenemy:{userid}:{type}:All"), Button.inline("• Groups •", data=f"addenemy:{userid}:{type}:Groups"), Button.inline("• Privates •", data=f"addenemy:{userid}:{type}:Privates"), Button.inline("• Here •", data=f"addenemy:{userid}:{type}:chat{event.chat_id}")]]
        buttons.append([Button.inline("🚫 Close 🚫", data="closeenemy")])
        await event.edit(text=text, buttons=buttons)
    else:
        where = data[2]
        Wheres = ""
        for enemy in Enemies:
            if Enemies[enemy]["user_id"] == userid:
                if not Wheres:
                    Wheres += f'{Enemies[enemy]["where"]}'
                else:
                    Wheres += f':{Enemies[enemy]["where"]}'
        if Enemies[userid]["where"] in Wheres.split(":"):
            return await event.answer(f"{client.str} The User ( {userinfo.first_name} ) Is Alredy In {type} Enemy List In {where} Location!", alert=True)
        rand = random.randint(11111111, 99999999)
        Enemies.update({rand: {"user_id": userid, "type": type, "where": where}})
        client.DB.set_key("ENEMIES", Enemies)
        await event.edit(text=f"**{client.str} The User** ( {client.mention(userinfo)} ) **Is Added To {type} Enemy List For {where} Location!**")

@client.Callback(data="closeenemy")
async def closeenemy(event):
    await event.edit(text=f"**{client.str} The Enemy Panel Successfuly Closed!**")
