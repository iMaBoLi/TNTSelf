from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random 

@client.Cmd(pattern=f"(?i)^\{client.cmd}Quicks (On|Off)$")
async def quicksmode(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("QUICKS_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(f"**{client.str} The Quicks Mode Has Been {change}!**")

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddQuick \'([\s\S]*)\' ?([\s\S]*)?")
async def addquick(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    cmd = event.pattern_match.group(1)
    answers = event.pattern_match.group(2)
    quicks = client.DB.get_key("INQUICKS") or {}
    rand = random.randint(11111111, 99999999)
    replyuser = None
    if event.is_reply:
        replyuser = event.reply_message.sender_id
    if not answers:
        if not event.is_reply:
            return await event.edit(f"**{client.str} Please Enter Text Answers Or Reply To Message!**")
        backch = client.DB.get_key("BACKUP_CHANNEL")
        if not backch:
            return await event.edit(f"**{client.str} The BackUp Channel Is Not Added!**")
        try:
            forward = await event.reply_message.forward_to(int(client.backch))
        except Exception as e:
            return await event.edit(f"**{client.str} The BackUp Channel Is Not Available! {e}**")
        quicks.update({"quick-" + str(rand): {"cmd": cmd, "answers": "QuickMedia:" + str(client.backch) + ":" + str(forward.id), "reply": replyuser}})
    else:
        quicks.update({"quick-" + str(rand): {"cmd": cmd, "answers": answers, "reply": replyuser}})
    client.DB.set_key("INQUICKS", quicks)
    res = await client.inline_query(client.bot.me.username, f"addquick:quick-{str(rand)}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelQuick ([\s\S]*)$")
async def delquick(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"]:
            qlist.append(quicks[quick])
    if not qlist:
        return await event.edit(f"**{client.str} The Command** ( `{cmd}` ) **Not In Quicks Command Lists!**")    
    res = await client.inline_query(client.bot.me.username, f"dquickdel:{cmd}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}GetQuick (.*)$")
async def delquick(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"]:
            qlist.append(quick)
    if not qlist:
        return await event.edit(f"**{client.str} The Command** ( `{cmd}` ) **Not In Quicks Command Lists!**")    
    for nq in qlist:
        info = quicks[nq]
        if info["type"] == "Media":
            msg = await client.get_messages(int(info["answers"].split(":")[1]), ids=int(info["answers"].split(":")[2]))
            send = await event.respond(msg)
            await send.reply(f"""
**{client.str} Command:** ( `{info["cmd"]}` )

**{client.str} Answer(s):** ( `Repleyed Media` )

**{client.str} Whom:** ( `{info["whom"].replace("user", "")}` )
**{client.str} Where:** ( `{info["where"].replace("chat", "")}` )
**{client.str} Type:** ( `{info["type"]}` )
**{client.str} Find:** ( `{info["find"]}` )
**{client.str} Sleep:** ( `{client.utils.convert_time(info["sleep"]) or "---"}` )
""")
        else:
            await event.respond(f"""
**{client.str} Command:** ( `{info["cmd"]}` )

**{client.str} Answer(s):** ( `{info["answers"]}` )

**{client.str} Whom:** ( `{info["whom"].replace("user", "")}` )
**{client.str} Where:** ( `{info["where"].replace("chat", "")}` )
**{client.str} Type:** ( `{info["type"]}` )
**{client.str} Find:** ( `{info["find"]}` )
**{client.str} Sleep:** ( `{client.utils.convert_time(info["sleep"]) or "---"}` )
""")
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}QuickList$")
async def quicklist(event):
    await event.edit(client.get_string("Wait_1").format(client.str))
    quicks = client.DB.get_key("QUICKS") or {}
    if not quicks:
        return await event.edit(f"**{client.str} The Quick List Is Empty!**")    
    res = await client.inline_query(client.bot.me.username, "allquicklist")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Cmd(sudo=False, edits=False)
async def quicksupdate(event):
    if event.is_cmd or not event.text: return
    mode = client.DB.get_key("QUICKS_MODE") or "off"
    if mode == "off": return
    quicks = client.DB.get_key("QUICKS") or {}
    if not quicks: return
    for quick in quicks:
        info = quicks[quick]
        if info["find"] == "Yes" and not info["cmd"] in event.text or info["find"] == "No" and not info["cmd"] == event.text: continue
        if info["whom"] == "Sudo" and not event.is_sudo and not event.is_ch: continue
        if info["whom"] == "Others" and event.is_sudo: continue
        if info["whom"].startswith("user") and not event.sender_id == int(info["whom"].replace("user", "")): continue
        if not info["where"] == "All":
            if info["where"] == "Groups" and not event.is_group: continue
            if info["where"] == "Privates" and not event.is_private: continue
            if info["where"].startswith("chat") and not event.chat_id == int(info["where"].replace("chat", "")): continue
        try:
            lastanswers = await client.vars(str(info["answers"]), event)
            answers = lastanswers.split(",")
            if info["type"] == "Normal":
                await event.reply(lastanswers)
                continue
            elif info["type"] == "Random":
                if info["whom"] == "Sudo":
                    await event.edit(random.choice(answers))
                else:
                    await event.reply(random.choice(answers))
                continue
            elif info["type"] == "Multi":
                for answer in answers:
                    await event.reply(answer)
                    await asyncio.sleep(int(info["sleep"]))
                continue
            elif info["type"] == "Edit":
                if info["whom"] == "Others":
                    event = await event.reply(answers[0])
                    answers = answers[1:]
                    if not answers: return
                    await asyncio.sleep(int(info["sleep"]))
                for answer in answers:
                    await event.edit(answer)
                    await asyncio.sleep(int(info["sleep"]))
                continue
            elif info["type"] == "Media":
                msg = await client.get_messages(int(info["answers"].split(":")[1]), ids=int(info["answers"].split(":")[2]))
                msg.text = await client.vars(str(msg.text), event)
                await event.reply(msg)
                continue
            elif info["type"] == "Draft":
                await client(functions.messages.SaveDraftRequest(peer=event.chat_id, message=lastanswers))
                continue
        except:
            continue

@client.Inline(pattern="addquick\:(.*)")
async def inlinequicks(event):
    quick = str(event.pattern_match.group(1))
    quicks = client.DB.get_key("INQUICKS") or {}
    text = f"**{client.str} Please Select You Want This Quick Answer To Be Saved For Whom:**"
    buttons = [[Button.inline("• SuDo •", data=f"wherequick:{quick}:Sudo"), Button.inline("• Others •", data=f"wherequick:{quick}:Others")]]
    if quicks[quick]["reply"]:
        user = quicks[quick]["reply"]
        buttons.append([Button.inline("• Reply User •", data=f"wherequick:{quick}:user{user}")])
    buttons.append([Button.inline("🚫 Close 🚫", data=f"closequick:{quick}")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Add Quick", text=text, buttons=buttons)])

@client.Callback(data="(.*)quick\:(.*)")
async def callbackquicks(event):
    work = str(event.data_match.group(1).decode('utf-8'))
    data = (str(event.data_match.group(2).decode('utf-8'))).split(":")
    quick = data[0]
    quicks = client.DB.get_key("INQUICKS") or {}
    cmd = quicks[quick]["cmd"]
    answers = quicks[quick]["answers"]
    if work == "where":
        whom = data[1]
        text = f"**{client.str} Please Choose Where You Want This Quick Answer To Be Saved:**"
        if answers.startswith("QuickMedia"):
            buttons = [[Button.inline("• All •", data=f"findquick:{quick}:{whom}:All:Media"), Button.inline("• Groups •", data=f"findquick:{quick}:{whom}:Groups:Media"), Button.inline("• Privates •", data=f"findquick:{quick}:{whom}:Privates:Media"), Button.inline("• Here •", data=f"findquick:{quick}:{whom}:chat{event.chat_id}:Media")]]
            buttons.append([Button.inline("🚫 Close 🚫", data=f"closequick:{quick}")])
        else:
            buttons = [[Button.inline("• All •", data=f"typequick:{quick}:{whom}:All"), Button.inline("• Groups •", data=f"typequick:{quick}:{whom}:Groups"), Button.inline("• Privates •", data=f"typequick:{quick}:{whom}:Privates"), Button.inline("• Here •", data=f"typequick:{quick}:{whom}:chat{event.chat_id}")]]
            buttons.append([Button.inline("🚫 Close 🚫", data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "type":
        whom = data[1]
        where = data[2]
        text = f"**{client.str} Please Select The Type Of This Quick Answer:**"
        if len(answers.split(",")) > 1:
            buttons = [[Button.inline("• Normal •", data=f"findquick:{quick}:{whom}:{where}:Normal"), Button.inline("• Multi •", data=f"findquick:{quick}:{whom}:{where}:Multi"), Button.inline("• Edit •", data=f"findquick:{quick}:{whom}:{where}:Edit"), Button.inline("• Random •", data=f"findquick:{quick}:{whom}:{where}:Random"), Button.inline("• Draft •", data=f"findquick:{quick}:{whom}:{where}:Draft")]]
        else:
            buttons = [[Button.inline("• Normal •", data=f"findquick:{quick}:{whom}:{where}:Normal"), Button.inline("• Draft •", data=f"findquick:{quick}:{whom}:{where}:Draft")]]
        buttons.append([Button.inline("🚫 Close 🚫", data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "find":
        whom = data[1]
        where = data[2]
        type = data[3]
        text = f"**{client.str} Please Select Whether To Search For This Quick Answer Command In Messages:**"
        if type == "Normal" or type == "Random" or type == "Draft" or type == "Media" or type == "Edit" and len(answers.split(",")) == 1 or type == "Multi" and len(answers.split(",")) == 1:
            buttons = [[Button.inline("• Yes •", data=f"setquick:{quick}:{whom}:{where}:{type}:Yes:0"), Button.inline("• No •", data=f"setquick:{quick}:{whom}:{where}:{type}:No:0")]]
        else:
            buttons = [[Button.inline("• Yes •", data=f"sleepquick:{quick}:{whom}:{where}:{type}:Yes"), Button.inline("• No •", data=f"sleepquick:{quick}:{whom}:{where}:{type}:No")]]
        buttons.append([Button.inline("🚫 Close 🚫", data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "sleep":
        whom = data[1]
        where = data[2]
        type = data[3]
        find = data[4]
        text = f"**{client.str} Please Choose A Sleep Time Between Each Answer:**"
        buttons = []
        for sleep in [1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 60, 120]:
            buttons.append(Button.inline(f"• {client.utils.convert_time(sleep)} •", data=f"setquick:{quick}:{whom}:{where}:{type}:{find}:{sleep}"))
        buttons.append(Button.inline("🚫 Close 🚫", data=f"closequick:{quick}"))
        buttons = list(client.utils.chunks(buttons, 4))
        await event.edit(text=text, buttons=buttons)
    elif work == "set":
        whom = data[1]
        where = data[2]
        type = data[3]
        find = data[4]
        sleep = data[5]
        gquick = quicks[quick]
        allquicks = client.DB.get_key("QUICKS") or {}
        allquicks.update({quick: {"cmd": gquick["cmd"],"answers": gquick["answers"],"whom": whom,"where": where,"type": type,"find": find,"sleep": sleep}})
        client.DB.set_key("QUICKS", allquicks)
        anss = gquick["answers"]
        await event.edit(text=f"""
**{client.str} The New Quick Answer Was Saved!**

**{client.str} Whom:** ( `{whom.replace("user", "")}` )
**{client.str} Where:** ( `{where.replace("chat", "")}` )
**{client.str} Type:** ( `{type}` )
**{client.str} Find:** ( `{find}` )
**{client.str} Sleep:** ( `{client.utils.convert_time(sleep) or "---"}` )

**{client.str} Command:** ( `{gquick["cmd"]}` )

**{client.str} Answer(s):** ( `{anss}` )""")
    elif work == "close":   
        del quicks[quick]
        client.DB.set_key("INQUICKS", quicks)
        await event.edit(text=f"**{client.str} The Quick Panel Successfuly Closed!**")

@client.Inline(pattern="dquickdel\:(.*)")
async def inlinequicks(event):
    cmd = str(event.pattern_match.group(1))
    text = f"**{client.str} Please Choose From Which List You Want** ( `{cmd}` ) **Quick Answer To Be Deleted:**"
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"] and "whom" in quicks[quick].keys():
            qlist.append(quick)
    buttons = []
    for quick in qlist:
        info = quicks[quick]
        buttons.append([Button.inline(f"""( {info["whom"].replace("user", "")} ) - ( {info["where"].replace("chat", "")} ) - ( {info["type"]} )""", data=f"dquickdel:{quick}")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Del Quick", text=text, buttons=buttons)])

@client.Callback(data="dquickdel\:(.*)")
async def delquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    await event.edit(text=f"""**{client.str} The Quick** ( `{quicks[quick]["cmd"]}` ) **From List** ( `{quicks[quick]["where"].replace("chat", "")} -> {quicks[quick]["whom"].replace("user", "")} -> {quicks[quick]["type"]}` ) **Has Been Deleted!**""")
    del quicks[quick]
    client.DB.set_key("QUICKS", quicks)

@client.Inline(pattern="allquicklist")
async def inlinequicklist(event):
    quicks = client.DB.get_key("QUICKS") or {}
    text = f"**{client.str} Please Select Each Quick Answer To View Its Information:**\n\n**{client.str} Quicks Count:** ( `{len(quicks)}` )"
    buttons = []
    for quick in list(quicks)[:10]:
        info = quicks[quick]
        buttons.append([Button.inline(f"""•[ {info["cmd"]} ]• ( {info["whom"].replace("user", "")} ) - ( {info["where"].replace("chat", "")} ) - ( {info["type"]} )""", data=f"viwequick:{quick}:1")])
    if len(quicks) > 10:
        buttons.append([Button.inline("Next ▶️", data=f"quicklistpage:2")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - List Quick", text=text, buttons=buttons)])

@client.Callback(data="quicklistpage\:(.*)")
async def listquicks(event):
    page = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    text = f"**{client.str} Please Select Each Quick Answer To View Its Information:**\n\n**{client.str} Quicks Count:** ( `{len(quicks)}` )"
    buttons = []
    qcount = (int(page) * 10)
    for quick in list(quicks)[(qcount-10):qcount]:
        info = quicks[quick]
        buttons.append([Button.inline(f"""•[ {info["cmd"]} ]• ( {info["whom"].replace("user", "")} ) - ( {info["where"].replace("chat", "")} ) - ( {info["type"]} )""", data=f"viwequick:{quick}:{page}")])
    pbts = []
    if int(page) != 1:
        pbts.append(Button.inline("◀️ Back", data=f"quicklistpage:{int(page)-1}"))
    if len(quicks) > qcount:
        pbts.append(Button.inline("Next ▶️", data=f"quicklistpage:{int(page)+1}"))
    buttons.append(pbts)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="viwequick\:(.*)\:(.*)")
async def listquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    page = str(event.data_match.group(2).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    buttons = [[Button.inline("❌ Delete ❌", data=f"dquickdel:{quick}")], [Button.inline("↩️ Back", data=f"quicklistpage:{page}")]]
    await event.edit(text=f"""
**{client.str} Quick Command:** ( `{info["cmd"]}` )

**{client.str} Answer(s):** ( `{info["answers"]}` )

**{client.str} Whom:** ( `{info["whom"].replace("user", "")}` )
**{client.str} Where:** ( `{info["where"].replace("chat", "")}` )
**{client.str} Type:** ( `{info["type"]}` )
**{client.str} Find:** ( `{info["find"]}` )
**{client.str} Sleep:** ( `{client.utils.convert_time(info["sleep"]) or "---"}` )""",buttons=buttons)
