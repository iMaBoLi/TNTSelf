from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random

STRINGS = {
    "notans": "**Enter Text Answers Or Reply To Message!**",
    "notin": "**The Command** ( `{}` ) **Not In Quicks Command Lists!**",
    "get": "**Command:** ( `{}` )\n\n**Answer(s):** ( `{}` )\n\n**Person:** ( `{}` )\n**Where:** ( `{}` )\n**Type:** ( `{}` )\n**Find:** ( `{}` )\n**Sleep:** ( `{}` )",
    "empty": "**The Quicks List Is Empty!**",
    "person": "**Select You Want This Quick Answer To Be Saved For Person:**",
    "where": "**Choose Where You Want This Quick Answer To Be Saved:**",
    "type": "**Select The Type Of This Quick Answer:**",
    "search": "**Select Whether To Search For This Quick Answer Command In Messages:**",
    "sleep": "**Choose A Sleep Time Between Each Answer:**",
    "save": "**The New Quick Answer Was Saved!**\n\n**Person:** ( `{}` )\n**Where:** ( `{}` )\n**Type:** ( `{}` )\n**Find:** ( `{}` )\n**Sleep:** ( `{}` )\n\n**Command:** ( `{}` )\n\n**Answer(s):** ( `{}` )",
    "close": "**The Quick Panel Successfuly Closed!**",
    "lidel": "**Choose From Which List You Want** ( `{}` ) **Quick Answer To Be Deleted:**",
    "del": "**The Quick** ( `{}` ) **From List** ( `{} -> {} -> {}` ) **Has Been Deleted!**",
    "info":  "**Select Each Quick Answer To View Its Information:**\n\n**Quicks Count:** ( `{}` )",
}

def get_buttons(quick):
    buttons = []
    Quicks = client.DB.get_key("QUICKS") or {}
    info = Quicks[quick]
    perbts = [[Button.inline("• Person :", data="Empty")]]
    operbts = []
    persons = ["Sudo", "Others", "Replyed User"] if info["reply"] else ["Sudo", "Others"] 
    for person in persons:
        ShowMode = client.STRINGS["Off"]
        if (person == "Replyed User" and info["person"].startswith("USER")) or info["person"] == person:
            ShowMode = client.STRINGS["On"]
        sperson = person if person != "Replyed User" else f"USER{info['reply']}"
        operbts.append(Button.inline(f"• {person} {ShowMode} •", data=f"SetQuick:person:{quick}:{sperson}"))
    perbts += [operbts]
    buttons.append(perbts)
    wherebts = [[Button.inline("• Place :", data="Empty")]]
    owherebts = []
    wheres = ["All", "Pv", "Groups", "Here"] 
    for where in wheres:
        ShowMode = client.STRINGS["Off"]
        if (where == "Here" and info["where"].startswith("CHAT")) or info["where"] == where:
            ShowMode = client.STRINGS["On"]
        swhere = where if where != "Here" else f"CHAT{info['chatid']}"
        owherebts.append(Button.inline(f"• {where} {ShowMode} •", data=f"SetQuick:where:{quick}:{swhere}"))
    wherebts += [owherebts]
    buttons.append(wherebts)
    if info["anstype"] != "Media":
        typebts = [[Button.inline("• Type :", data="Empty")]]
        otypebts = []
        types = ["Normal", "Multi", "Edit", "Random", "Draft"] if len(info["answers"].split(",")) > 1 else ["Normal", "Draft"]
        for type in types:
            ShowMode = client.STRINGS["On"] if info["type"] == type else client.STRINGS["Off"]
            otypebts.append(Button.inline(f"• {type} {ShowMode} •", data=f"SetQuick:type:{quick}:{type}"))
        typebts += list(client.functions.chunks(otypebts, 3))
        buttons.append(typebts)
    client.STRINGS["inline"]["Yes"]
    findbts = [[Button.inline("• Find :", data="Empty")]]
    ofindbts = []
    findes = ["Yes", "No"] 
    for find in findes:
        ShowMode = client.STRINGS["On"] if info["find"] == find else client.STRINGS["Off"]
        ofindbts.append(Button.inline(f"• {find} {ShowMode} •", data=f"SetQuick:find:{quick}:{find}"))
    findbts += [ofindbts]
    buttons.append(findbts)
    if info["anstype"] != "Media" and len(info["answers"].split(",")) > 1:
        sleepbts = [[Button.inline("• Sleep :", data="Empty")]]
        osleepbts = []
        sleeps = [0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 10]
        for sleep in sleeps:
            ShowMode = client.STRINGS["On"] if info["sleep"] == sleep else client.STRINGS["Off"]
            osleepbts.append(Button.inline(f"• {sleep} {ShowMode} •", data=f"SetQuick:sleep:{quick}:{sleep}"))
        sleepbts += list(client.functions.chunks(osleepbts, 4))
        buttons.append(sleepbts)
    buttons.append([Button.inline("• Save •", data=f"SaveQuick:{quick}")])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"CloseQuick:{quick}")])

@client.Inline(pattern="addquick\:(.*)")
async def inlinequicks(event):
    quick = str(event.pattern_match.group(1))
    quicks = client.DB.get_key("INQUICKS") or {}
    text = STRINGS["person"]
    buttons = [[Button.inline("• SuDo •", data=f"wherequick:{quick}:Sudo"), Button.inline("• OtherS •", data=f"wherequick:{quick}:Others")]]
    if quicks[quick]["reply"]:
        user = quicks[quick]["reply"]
        buttons.append([Button.inline("• Replyed  User •", data=f"wherequick:{quick}:user{user}")])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}")])
    await event.answer([event.builder.article("FidoSelf - Add Quick", text=text, buttons=buttons)])


@client.Command(command="AddQuick \'([\s\S]*)\' ?([\s\S]*)?")
async def addquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)
    answers = event.pattern_match.group(2)
    quicks = client.DB.get_key("INQUICKS") or {}
    rand = random.randint(111111111, 999999999)
    replyuser = event.reply_message.sender_id if event.is_reply else None
    if not answers:
        if not event.is_reply:
            return await event.edit(STRINGS["notans"])
        info = await event.reply_message.save()
        quicks.update({"Quick-" + str(rand): {"cmd": cmd, "anstype": "Media", "answers": info, "reply": replyuser}})
    else:
        quicks.update({"Quick-" + str(rand): {"cmd": cmd, "anstype": "Text", "answers": answers, "reply": replyuser}})
    client.DB.set_key("INQUICKS", quicks)
    res = await client.inline_query(client.bot.me.username, f"addquick:Quick-{str(rand)}")
    if replyuser:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="DelQuick ([\s\S]*)")
async def delquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"]:
            qlist.append(quicks[quick])
    if not qlist:
        return await event.edit(STRINGS["notin"].format(cmd))
    res = await client.inline_query(client.bot.me.username, f"dquickdel:{cmd}")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Command(command="GetQuick (.*)")
async def delquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"]:
            qlist.append(quick)
    if not qlist:
        return await event.edit(STRINGS["notin"].format(cmd))    
    for nq in qlist:
        info = quicks[nq]
        if info["type"] == "Media":
            msg = await client.get_messages(int(info["answers"].split(":")[1]), ids=int(info["answers"].split(":")[2]))
            send = await event.respond(msg)
            await send.reply(STRINGS["get"].format(info["cmd"], "Repleyed Message", info["person"].replace("user", ""), info["where"].replace("chat", ""), info["type"], info["find"], (client.functions.convert_time(info["sleep"]) or "---")))
        else:
            await event.respond(STRINGS["get"].format(info["cmd"], info["answers"], info["person"].replace("user", ""), info["where"].replace("chat", ""), info["type"], info["find"], (client.functions.convert_time(info["sleep"]) or "---")))
    await event.delete()

@client.Command(command="QuickList")
async def quicklist(event):
    await event.edit(client.STRINGS["wait"])
    quicks = client.DB.get_key("QUICKS") or {}
    if not quicks:
        return await event.edit(STRINGS["empty"])    
    res = await client.inline_query(client.bot.me.username, "allquicklist")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()

@client.Command(onlysudo=False, alowedits=False)
async def quicksupdate(event):
    if event.checkCmd() or not event.text: return
    mode = client.DB.get_key("QUICKS_MODE") or "off"
    if mode == "off": return
    quicks = client.DB.get_key("QUICKS") or {}
    if not quicks: return
    for quick in quicks:
        info = quicks[quick]
        if info["find"] == "Yes" and not info["cmd"] in event.text or info["find"] == "No" and not info["cmd"] == event.text: continue
        if info["person"] == "Sudo" and not event.is_sudo and not event.is_ch: continue
        if info["person"] == "Others" and event.is_sudo: continue
        if info["person"].startswith("user") and not event.sender_id == int(info["person"].replace("user", "")): continue
        if not info["where"] == "All":
            if info["where"] == "Groups" and not event.is_group: continue
            if info["where"] == "Privates" and not event.is_private: continue
            if info["where"].startswith("chat") and not event.chat_id == int(info["where"].replace("chat", "")): continue
        try:
            lastanswers = await client.AddVars(str(info["answers"]), event)
            answers = lastanswers.split(",")
            if info["type"] == "Normal":
                await event.reply(lastanswers)
                continue
            elif info["type"] == "Random":
                if info["person"] == "Sudo":
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
                if info["person"] == "Others":
                    event = await event.reply(answers[0])
                    answers = answers[1:]
                    if not answers: continue
                    await asyncio.sleep(int(info["sleep"]))
                for answer in answers:
                    await event.edit(answer)
                    await asyncio.sleep(int(info["sleep"]))
                continue
            elif info["type"] == "Media":
                media = info["answers"]
                msg = await client.get_messages(int(media["chat_id"]), ids=int(media["msg_id"]))
                msg.text = await client.AddVars(str(msg.text), event)
                await event.reply(msg)
                continue
            elif info["type"] == "Draft":
                await client(functions.messages.SaveDraftRequest(peer=event.chat_id, message=lastanswers))
                continue
        except Exception as error:
            client.LOGS.error(error)

@client.Inline(pattern="addquick\:(.*)")
async def inlinequicks(event):
    quick = str(event.pattern_match.group(1))
    quicks = client.DB.get_key("INQUICKS") or {}
    text = STRINGS["person"]
    buttons = [[Button.inline("• SuDo •", data=f"wherequick:{quick}:Sudo"), Button.inline("• OtherS •", data=f"wherequick:{quick}:Others")]]
    if quicks[quick]["reply"]:
        user = quicks[quick]["reply"]
        buttons.append([Button.inline("• Replyed  User •", data=f"wherequick:{quick}:user{user}")])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}")])
    await event.answer([event.builder.article("FidoSelf - Add Quick", text=text, buttons=buttons)])

@client.Callback(data="(.*)quick\:(.*)")
async def callbackquicks(event):
    work = str(event.data_match.group(1).decode('utf-8'))
    data = (str(event.data_match.group(2).decode('utf-8'))).split(":")
    quick = data[0]
    quicks = client.DB.get_key("INQUICKS") or {}
    cmd = quicks[quick]["cmd"]
    anstype = quicks[quick]["anstype"]
    answers = quicks[quick]["answers"]
    if work == "where":
        person = data[1]
        text = STRINGS["where"]
        if anstype == "Media":
            buttons = [[Button.inline("• All •", data=f"findquick:{quick}:{person}:All:Media"), Button.inline("• Groups •", data=f"findquick:{quick}:{person}:Groups:Media"), Button.inline("• Pv •", data=f"findquick:{quick}:{person}:Privates:Media"), Button.inline("• Here •", data=f"findquick:{quick}:{person}:chat{event.chat_id}:Media")]]
            buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}")])
        else:
            buttons = [[Button.inline("• All •", data=f"typequick:{quick}:{person}:All"), Button.inline("• Groups •", data=f"typequick:{quick}:{person}:Groups"), Button.inline("• Pv •", data=f"typequick:{quick}:{person}:Privates"), Button.inline("• Here •", data=f"typequick:{quick}:{person}:chat{event.chat_id}")]]
            buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "type":
        person = data[1]
        where = data[2]
        text = STRINGS["type"]
        if len(answers.split(",")) > 1:
            buttons = [[Button.inline("• Normal •", data=f"findquick:{quick}:{person}:{where}:Normal"), Button.inline("• Multi •", data=f"findquick:{quick}:{person}:{where}:Multi"), Button.inline("• Edit •", data=f"findquick:{quick}:{person}:{where}:Edit"), Button.inline("• Random •", data=f"findquick:{quick}:{person}:{where}:Random"), Button.inline("• Draft •", data=f"findquick:{quick}:{person}:{where}:Draft")]]
        else:
            buttons = [[Button.inline("• Normal •", data=f"findquick:{quick}:{person}:{where}:Normal"), Button.inline("• Draft •", data=f"findquick:{quick}:{person}:{where}:Draft")]]
        buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "find":
        person = data[1]
        where = data[2]
        type = data[3]
        text = STRINGS["search"]
        if type == "Normal" or type == "Random" or type == "Draft" or type == "Media" or type == "Edit" and len(answers.split(",")) == 1 or type == "Multi" and len(answers.split(",")) == 1:
            buttons = [[Button.inline(client.STRINGS["inline"]["Yes"], data=f"setquick:{quick}:{person}:{where}:{type}:Yes:0"), Button.inline(client.STRINGS["inline"]["No"], data=f"setquick:{quick}:{person}:{where}:{type}:No:0")]]
        else:
            buttons = [[Button.inline(client.STRINGS["inline"]["Yes"], data=f"sleepquick:{quick}:{person}:{where}:{type}:Yes"), Button.inline(client.STRINGS["inline"]["No"], data=f"sleepquick:{quick}:{person}:{where}:{type}:No")]]
        buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}")])
        await event.edit(text=text, buttons=buttons)
    elif work == "sleep":
        person = data[1]
        where = data[2]
        type = data[3]
        find = data[4]
        text = STRINGS["sleep"]
        buttons = []
        for sleep in [0.2, 0.5, 0.8, 1, 1.5, 2, 2.5, 3, 4, 5, 10, 15, 20, 30, 60, 120]:
            buttons.append(Button.inline(f"• {client.functions.convert_time(sleep)} •", data=f"setquick:{quick}:{person}:{where}:{type}:{find}:{sleep}"))
        buttons.append(Button.inline(client.STRINGS["inline"]["Close"], data=f"closequick:{quick}"))
        buttons = list(client.functions.chunks(buttons, 4))
        await event.edit(text=text, buttons=buttons)
    elif work == "set":
        person = data[1]
        where = data[2]
        type = data[3]
        find = data[4]
        sleep = data[5]
        gquick = quicks[quick]
        allquicks = client.DB.get_key("QUICKS") or {}
        allquicks.update({quick: {"cmd": gquick["cmd"],"answers": gquick["answers"],"person": person,"where": where,"type": type,"find": find,"sleep": sleep}})
        client.DB.set_key("QUICKS", allquicks)
        anss = gquick["answers"] if anstype != "Media" else "Media"
        person = person.replace("user", "")
        where = where.replace("chat", "")
        text = STRINGS["save"].format(person, where, type, client.STRINGS["inline"][find], (client.functions.convert_time(sleep)), gquick["cmd"], anss)
        await event.edit(text=text)
    elif work == "close":   
        del quicks[quick]
        client.DB.set_key("INQUICKS", quicks)
        await event.edit(text=STRINGS["Close"])

@client.Inline(pattern="dquickdel\:(.*)")
async def inlinequicks(event):
    cmd = str(event.pattern_match.group(1))
    text = STRINGS["lidel"].format(cmd)
    quicks = client.DB.get_key("QUICKS") or {}
    qlist = []
    for quick in quicks:
        if cmd == quicks[quick]["cmd"] and "person" in quicks[quick].keys():
            qlist.append(quick)
    buttons = []
    for quick in qlist:
        info = quicks[quick]
        person = info["person"].replace("user", "")
        where = info["where"].replace("chat", "")
        type = info["type"]
        buttons.append([Button.inline(f"""( {person} ) - ( {where} ) - ( {type} )""", data=f"dquickdel:{quick}")])
    await event.answer([event.builder.article("FidoSelf - Del Quick", text=text, buttons=buttons)])

@client.Callback(data="dquickdel\:(.*)")
async def delquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    person = info["person"].replace("user", "")
    where = info["where"].replace("chat", "")
    type = info["type"]
    text = STRINGS["del"].format(info["cmd"], person, where, type)
    await event.edit(text=text)
    del quicks[quick]
    client.DB.set_key("QUICKS", quicks)

@client.Inline(pattern="allquicklist")
async def inlinequicklist(event):
    quicks = client.DB.get_key("QUICKS") or {}
    text = STRINGS["info"].format(len(quicks))
    buttons = []
    for quick in list(quicks)[:10]:
        info = quicks[quick]
        person = info["person"].replace("user", "")
        where = info["where"].replace("chat", "")
        type = info["type"]
        buttons.append([Button.inline(f"""•[ {info["cmd"]} ]• ( {person} ) - ( {where} ) - ( {type} )""", data=f"viwequick:{quick}:1")])
    if len(quicks) > 10:
        buttons.append([Button.inline(client.STRINGS["inline"]["Next"], data=f"quicklistpage:2")])
    await event.answer([event.builder.article("FidoSelf - List Quick", text=text, buttons=buttons)])

@client.Callback(data="quicklistpage\:(.*)")
async def listquicks(event):
    page = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    text = STRINGS["info"].format(len(quicks))
    buttons = []
    qcount = (int(page) * 10)
    for quick in list(quicks)[(qcount-10):qcount]:
        info = quicks[quick]
        person = info["person"].replace("user", "")
        where = info["where"].replace("chat", "")
        type = info["type"]
        buttons.append([Button.inline(f"""•[ {info["cmd"]} ]• ( {person} ) - ( {where} ) - ( {type} )""", data=f"viwequick:{quick}:{page}")])
    pbts = []
    if int(page) != 1:
        pbts.append(Button.inline(client.STRINGS["inline"]["Next"], data=f"quicklistpage:{int(page)-1}"))
    if len(quicks) > qcount:
        pbts.append(Button.inline(client.STRINGS["inline"]["Close"], data=f"quicklistpage:{int(page)+1}"))
    buttons.append(pbts)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="viwequick\:(.*)\:(.*)")
async def listquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    page = str(event.data_match.group(2).decode('utf-8'))
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    person = info["person"].replace("user", "")
    where = info["where"].replace("chat", "")
    type = info["type"]
    anss = info["answers"]
    anss = anss if info["type"] != "Media" else "Media"
    text = STRINGS["get"].format(info["cmd"], anss, person, where, type, client.STRINGS["inline"][info["find"]], (client.functions.convert_time(info["sleep"])))
    buttons = [[Button.inline("❌ Delete ❌", data=f"dquickdel:{quick}"), Button.inline("↩️ Back", data=f"quicklistpage:{page}")]]
    await event.edit(text=text, buttons=buttons)))