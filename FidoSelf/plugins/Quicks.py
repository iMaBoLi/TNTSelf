from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random 

@client.Cmd(pattern=f"(?i)^\{client.cmd}Quicks (On|Off)$")
async def quicksmode(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("QUICKS_MODE", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("Quicks_1").format(change))

@client.Cmd(pattern=f"(?i)^\{client.cmd}AddQuick \'([\s\S]*)\' ?([\s\S]*)?")
async def addquick(event):
    await event.edit(client.get_string("Wait"))
    cmd = event.pattern_match.group(1)
    answers = event.pattern_match.group(2)
    quicks = client.DB.get_key("INQUICKS") or {}
    rand = random.randint(11111111, 99999999)
    replyuser = None
    if event.is_reply:
        replyuser = event.reply_message.sender_id
    if not answers:
        if not event.is_reply:
            return await event.edit(client.get_string("Quicks_2"))
        backch = client.DB.get_key("BACKUP_CHANNEL")
        if not backch:
            return await event.edit(client.get_string("LogCh_1"))
        try:
            forward = await event.reply_message.forward_to(int(client.backch))
        except:
            return await event.edit(client.get_string("LogCh_2"))
        quicks.update({"quick-" + str(rand): {"cmd": cmd, "answers": "QuickMedia:" + str(client.backch) + ":" + str(forward.id), "reply": replyuser}})
    else:
        quicks.update({"quick-" + str(rand): {"cmd": cmd, "answers": answers, "reply": replyuser}})
    client.DB.set_key("INQUICKS", quicks)
    res = await client.inline_query(client.bot.me.username, f"addquick:quick-{str(rand)}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}DelQuick ([\s\S]*)$")
async def delquick(event):
    await event.edit(client.get_string("Wait"))
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"]:
            qlist.append(quicks[quick])
    if not qlist:
        return await event.edit(client.get_string("Quicks_3").format(cmd))
    res = await client.inline_query(client.bot.me.username, f"dquickdel:{cmd}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}GetQuick (.*)$")
async def delquick(event):
    await event.edit(client.get_string("Wait"))
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"]:
            qlist.append(quick)
    if not qlist:
        return await event.edit(client.get_string("Quicks_3").format(cmd))    
    for nq in qlist:
        info = quicks[nq]
        if info["type"] == "Media":
            msg = await client.get_messages(int(info["answers"].split(":")[1]), ids=int(info["answers"].split(":")[2]))
            send = await event.respond(msg)
            await send.reply(client.get_string("Quicks_4").format(info["cmd"], "Repleyed Message", info["whom"].replace("user", ""), info["where"].replace("chat", ""), info["type"], info["find"], (client.utils.convert_time(info["sleep"]) or "---")))
        else:
            await event.respond(client.get_string("Quicks_4").format(info["cmd"], info["answers"], info["whom"].replace("user", ""), info["where"].replace("chat", ""), info["type"], info["find"], (client.utils.convert_time(info["sleep"]) or "---")))
    await event.delete()

@client.Cmd(pattern=f"(?i)^\{client.cmd}QuickList$")
async def quicklist(event):
    await event.edit(client.get_string("Wait"))
    quicks = client.DB.get_key("QUICKS") or {}
    if not quicks:
        return await event.edit(client.get_string("Quicks_5"))    
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
    text = client.get_string("Quicks_6")
    buttons = [[Button.inline(f'• {client.get_string("InQuicks_Sudo")} •', data=f"wherequick:{quick}:Sudo"), Button.inline(f'• {client.get_string("InQuicks_Others")} •', data=f"wherequick:{quick}:Others")]]
    if quicks[quick]["reply"]:
        user = quicks[quick]["reply"]
        buttons.append([Button.inline(f'• {client.get_string("InQuicks_ReplyUser")} •', data=f"wherequick:{quick}:user{user}")])
    buttons.append([Button.inline(client.get_string("Inline_3"), data=f"closequick:{quick}")])
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
        text = client.get_string("Quicks_7")
        if answers.startswith("QuickMedia"):
            buttons = [[Button.inline(f'• {client.get_string("ChType_All")} •', data=f"findquick:{quick}:{whom}:All:Media"), Button.inline(f'• {client.get_string("ChType_Gp")} •', data=f"findquick:{quick}:{whom}:Groups:Media"), Button.inline(f'• {client.get_string("ChType_Pv")} •', data=f"findquick:{quick}:{whom}:Privates:Media"), Button.inline(f'• {client.get_string("ChType_Here")} •', data=f"findquick:{quick}:{whom}:chat{event.chat_id}:Media")]]
            buttons.append([Button.inline(client.get_string("Inline_3"), data=f"closequick:{quick}")])
        else:
            buttons = [[Button.inline(f'• {client.get_string("ChType_All")} •', data=f"typequick:{quick}:{whom}:All"), Button.inline(f'• {client.get_string("ChType_Gp")} •', data=f"typequick:{quick}:{whom}:Groups"), Button.inline(f'• {client.get_string("ChType_Pv")} •', data=f"typequick:{quick}:{whom}:Privates"), Button.inline(f'• {client.get_string("ChType_Here")} •', data=f"typequick:{quick}:{whom}:chat{event.chat_id}")]]
            buttons.append([Button.inline(client.get_string("Inline_3"), data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "type":
        whom = data[1]
        where = data[2]
        text = client.get_string("Quicks_8")
        if len(answers.split(",")) > 1:
            buttons = [[Button.inline(f'• {client.get_string("InQuicks_Normal")} •', data=f"findquick:{quick}:{whom}:{where}:Normal"), Button.inline(f'• {client.get_string("InQuicks_Multi")} •', data=f"findquick:{quick}:{whom}:{where}:Multi"), Button.inline(f'• {client.get_string("InQuicks_Edit")} •', data=f"findquick:{quick}:{whom}:{where}:Edit"), Button.inline(f'• {client.get_string("InQuicks_Random")} •', data=f"findquick:{quick}:{whom}:{where}:Random"), Button.inline(f'• {client.get_string("InQuicks_Draft")} •', data=f"findquick:{quick}:{whom}:{where}:Draft")]]
        else:
            buttons = [[Button.inline(f'• {client.get_string("InQuicks_Normal")} •', data=f"findquick:{quick}:{whom}:{where}:Normal"), Button.inline(f'• {client.get_string("InQuicks_Draft")} •', data=f"findquick:{quick}:{whom}:{where}:Draft")]]
        buttons.append([Button.inline(client.get_string("Inline_3"), data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "find":
        whom = data[1]
        where = data[2]
        type = data[3]
        text = client.get_string("Quicks_9")
        if type == "Normal" or type == "Random" or type == "Draft" or type == "Media" or type == "Edit" and len(answers.split(",")) == 1 or type == "Multi" and len(answers.split(",")) == 1:
            buttons = [[Button.inline(f'• {client.get_string("Yes")} •', data=f"setquick:{quick}:{whom}:{where}:{type}:Yes:0"), Button.inline(f'• {client.get_string("No")} •', data=f"setquick:{quick}:{whom}:{where}:{type}:No:0")]]
        else:
            buttons = [[Button.inline(f'• {client.get_string("Yes")} •', data=f"sleepquick:{quick}:{whom}:{where}:{type}:Yes"), Button.inline(f'• {client.get_string("No")} •', data=f"sleepquick:{quick}:{whom}:{where}:{type}:No")]]
        buttons.append([Button.inline(client.get_string("Inline_3"), data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "sleep":
        whom = data[1]
        where = data[2]
        type = data[3]
        find = data[4]
        text = client.get_string("Quicks_10")
        buttons = []
        for sleep in [0, 1, 2, 3, 4, 5, 10, 15, 20, 30, 60, 120]:
            buttons.append(Button.inline(f"• {client.utils.convert_time(sleep)} •", data=f"setquick:{quick}:{whom}:{where}:{type}:{find}:{sleep}"))
        buttons.append(Button.inline(client.get_string("Inline_3"), data=f"closequick:{quick}"))
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
        text = client.get_string("Quicks_11").format(whom.replace("user", ""), where.replace("chat", ""), client.get_string(f"InQuicks_{type}"), client.get_string(find), (client.utils.convert_time(sleep) or "---"), gquick["cmd"], anss)
        await event.edit(text=text)
    elif work == "close":   
        del quicks[quick]
        client.DB.set_key("INQUICKS", quicks)
        await event.edit(text=client.get_string("Quicks_12"))

@client.Inline(pattern="dquickdel\:(.*)")
async def inlinequicks(event):
    cmd = str(event.pattern_match.group(1))
    text = client.get_string("Quicks_13").format(cmd)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"] and "whom" in quicks[quick].keys():
            qlist.append(quick)
    buttons = []
    for quick in qlist:
        info = quicks[quick]
        buttons.append([Button.inline(f"""( {info["whom"].replace("user", "")} ) - ( {info["where"].replace("chat", "")} ) - ( {client.get_string(f'InQuicks_{info["type"]}')} )""", data=f"dquickdel:{quick}")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - Del Quick", text=text, buttons=buttons)])

@client.Callback(data="dquickdel\:(.*)")
async def delquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    text = client.get_string("Quicks_14").format(quicks[quick]["cmd"], quicks[quick]["where"].replace("chat", ""), quicks[quick]["whom"].replace("user", ""), quicks[quick]["type"])
    await event.edit(text=text)
    del quicks[quick]
    client.DB.set_key("QUICKS", quicks)

@client.Inline(pattern="allquicklist")
async def inlinequicklist(event):
    quicks = client.DB.get_key("QUICKS") or {}
    text = client.get_string("Quicks_15").format(len(quicks))
    buttons = []
    for quick in list(quicks)[:10]:
        info = quicks[quick]
        buttons.append([Button.inline(f"""•[ {info["cmd"]} ]• ( {info["whom"].replace("user", "")} ) - ( {info["where"].replace("chat", "")} ) - ( {client.get_string(f'InQuicks_{info["type"]}')} )""", data=f"viwequick:{quick}:1")])
    if len(quicks) > 10:
        buttons.append([Button.inline(client.get_string("Inline_4"), data=f"quicklistpage:2")])
    await event.answer([event.builder.article(f"{client.str} Smart Self - List Quick", text=text, buttons=buttons)])

@client.Callback(data="quicklistpage\:(.*)")
async def listquicks(event):
    page = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    text = client.get_string("Quicks_15").format(len(quicks))
    buttons = []
    qcount = (int(page) * 10)
    for quick in list(quicks)[(qcount-10):qcount]:
        info = quicks[quick]
        buttons.append([Button.inline(f"""•[ {info["cmd"]} ]• ( {info["whom"].replace("user", "")} ) - ( {info["where"].replace("chat", "")} ) - ( {info["type"]} )""", data=f"viwequick:{quick}:{page}")])
    pbts = []
    if int(page) != 1:
        pbts.append(Button.inline(client.get_string("Inline_4"), data=f"quicklistpage:{int(page)-1}"))
    if len(quicks) > qcount:
        pbts.append(Button.inline(client.get_string("Inline_3"), data=f"quicklistpage:{int(page)+1}"))
    buttons.append(pbts)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="viwequick\:(.*)\:(.*)")
async def listquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    page = str(event.data_match.group(2).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    buttons = [[Button.inline(f' {client.get_string("InQuicks_Delete")} ', data=f"dquickdel:{quick}")], [Button.inline(f'• {client.get_string("InQuicks_Back")} •', data=f"quicklistpage:{page}")]]
    text = client.get_string("Quicks_4").format(info["cmd"], info["answers"], info["whom"].replace("user", ""), info["where"].replace("chat", ""), client.get_string(f'InQuicks_{info["type"]}'), client.get_string(info["find"]), (client.utils.convert_time(info["sleep"]) or "---"))
    await event.edit(text=text,buttons=buttons)
