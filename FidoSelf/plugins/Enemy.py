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

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelEnemy ?(.*)?")
async def delenemy(event):
    await event.edit(f"**{client.str} Processing . . .**")
    if not event.is_private and not event.userid:
        return await event.edit(f"**{client.str} Please Enter Userid Or Username Or Send In Private Chats!**")
    if not event.userid:
        event.userid = event.chat_id
    res = await client.inline_query(client.bot.me.username, f"delenemy:{event.userid}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Inline(pattern="(.*)enemy\:(.*)")
async def inlineenemy(event):
    work = str(event.pattern_match.group(1))
    userid = event.pattern_match.group(2)
    text = f"**{client.str} Please Select Type Of This Enemy:"
    buttons = [[Button.inline("• Orginal Enemy •", data=f"{work}enemy:{userid}:Original"), Button.inline("• Friend Enemy •", data=f"{work}enemy:{userid}:Friend")]]
    buttons.append([Button.inline("🚫 Close 🚫", data="closeenemy")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Enemy", text=text, buttons=buttons)])

@client.Callback(data="(.*)enemy\:(.*)")
async def cenemies(event):
    work = str(event.data_match.group(1).decode('utf-8'))
    data = str(event.data_match.group(2).decode('utf-8')).split(":")
    userid = data[0]
    userinfo = await client.get_entity(userid)
    type = data[1]
    Enemies = client.DB.get_key("ENEMIES") or {}
    if len(data) == 2:
        if userid in Enemies and Enemies[userid]["type"] == type:
            return await event.answer(f"{client.str} The User ( {userinfo.first_name} ) Is Alredy In Enemy List In {type}!")
        if work == "add":
            text = f"**{client.str} Please Select You Want This Enemy User To Be Saved For Where:**"
        elif work == "del":
            text = f"**{client.str} Please Select You Want This Enemy User To Be Deleted From Where:**"
        buttons = [[Button.inline("• All •", data=f"{work}enemy:{userid}:{type}:All"), Button.inline("• Groups •", data=f"{work}enemy:{userid}:{type}:Groups"), Button.inline("• Privates •", data=f"{work}enemy:{userid}:{type}:Privates"), Button.inline("• Here •", data=f"{work}enemy:{userid}:{type}:chat{event.chat_id}")]]
        buttons.append([Button.inline("🚫 Close 🚫", data="closeenemy")])
        await event.edit(text=text, buttons=buttons)
    else:
        where = data[2]
        if userid in Enemies and Enemies[userid]["where"] == where:
            return await event.answer(f"{client.str} The User ( {userinfo.first_name} ) Is Alredy In {type}-{where} Enemy List!")
        if work == "add":
            Enemies.update({userid: {"type": type, "where": where}})
            client.DB.set_key("ENEMIES", Enemies)
            await event.edit(text=f"**{client.str} The User** ( {client.mention(userinfo)} ) **Is Added To {type} Enemy List For {where} Location!**")
        elif work == "del":
            Enemies.remove(userid)
            client.DB.set_key("ENEMIES", Enemies)
            await event.edit(text=f"**{client.str} The User** ( {client.mention(userinfo)} ) **Is Deleted From {type} Enemy List For {where} Location!**")

@client.Callback(data="closeenemy")
async def closeenemy(event):
    await event.edit(text=f"**{client.str} The Enemy Panel Successfuly Closed!**")
