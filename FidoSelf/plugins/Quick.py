from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random

STRINGS = {
    "quickpage": "**𑁍 Select And Setting This Quick Answer:**\n\n**Command:** ( `{}` )\n**Answer:** ( `{}` )",
    "setquick": "**➜ The {} Setting Was Set To** ( `{}` )",
    "savequick": "**𑁍 The Quick Answer Was Saved!**\n\n**✯ Person:** ( `{}` )\n**✯ Where:** ( `{}` )\n**✯ Type:** ( `{}` )\n**✯ Find:** ( `{}` )\n**✯ Sleep:** ( `{}` )\n\n**✯ Command:** ( `{}` )\n\n**✯ Answer(s):* ( `{}` )",
    "closequick": "**☻︎ The Quick Panel Successfully Closed!**",
}

@client.Command(onlysudo=False, alowedits=False)
async def quicksupdate(event):
    if event.checkCmd() or not event.text: return
    QMode = client.DB.get_key("QUICKS_MODE") or "off"
    if QMode == "off": return
    quicks = client.DB.get_key("QUICKS") or {}
    if not quicks: return
    for quick in quicks:
        info = quicks[quick]
        if not info["DO"]: continue
        if info["Finder"] == "Yes" and not info["Command"] in event.text or info["Finder"] == "No" and not info["Command"] == event.text: continue
        if info["Person"] == "Sudo" and not event.is_sudo and not event.is_ch: continue
        if info["Person"] == "Others" and event.is_sudo: continue
        if info["Person"].startswith("USER") and not event.sender_id == int(info["Person"].replace("USER", "")): continue
        if not info["Where"] == "All":
            if info["Where"] == "Groups" and not event.is_group: continue
            if info["Where"] == "Privates" and not event.is_private: continue
            if info["Where"].startswith("CHAT") and not event.chat_id == int(info["Where"].replace("CHAT", "")): continue
        try:
            lastanswers = await client.AddVars(str(info["Answers"]), event)
            answers = lastanswers.split(",")
            if info["Type"] == "Normal":
                await event.reply(lastanswers)
                continue
            elif info["Type"] == "Random":
                if info["Person"] == "Sudo":
                    await event.edit(random.choice(answers))
                else:
                    await event.reply(random.choice(answers))
                continue
            elif info["Type"] == "Multi":
                for answer in answers:
                    await event.reply(answer)
                    await asyncio.sleep(int(info["Sleep"]))
                continue
            elif info["Type"] == "Edit":
                if info["Person"] == "Others":
                    event = await event.reply(answers[0])
                    answers = answers[1:]
                    if not answers: continue
                    await asyncio.sleep(int(info["Sleep"]))
                for answer in answers:
                    await event.edit(answer)
                    await asyncio.sleep(int(info["Sleep"]))
                continue
            elif info["Type"] == "Media":
                media = info["Answers"]
                msg = await client.get_messages(int(media["chat_id"]), ids=int(media["msg_id"]))
                msg.text = await client.AddVars(str(msg.text), event)
                await event.reply(msg)
                continue
            elif info["Type"] == "Draft":
                await client(functions.messages.SaveDraftRequest(peer=event.chat_id, message=lastanswers))
                continue
        except Exception as error:
            client.LOGS.error(error)

def get_buttons(quick):
    buttons = []
    Quicks = client.DB.get_key("QUICKS") or {}
    info = Quicks[quick]
    perbts = [[Button.inline("🙎 Person : ⤵️", data="Empty")]]
    operbts = []
    persons = ["Sudo", "Others", "Replyed User"] if info["Reply"] else ["Sudo", "Others"] 
    for person in persons:
        ShowMode = client.STRINGS["inline"]["Off"]
        if (person == "Replyed User" and info["Person"].startswith("USER")) or info["Person"] == person:
            ShowMode = client.STRINGS["inline"]["On"]
        sperson = person if person != "Replyed User" else f"USER{info['Reply']}"
        operbts.append(Button.inline(f"{person} {ShowMode}", data=f"SetQuick:Person:{quick}:{sperson}"))
    perbts += [operbts]
    buttons += perbts
    wherebts = [[Button.inline("🛸 Place : ⤵️", data="Empty")]]
    owherebts = []
    wheres = ["All", "Pv", "Groups", "Here"] 
    for where in wheres:
        ShowMode = client.STRINGS["inline"]["Off"]
        if (where == "Here" and info["Where"].startswith("CHAT")) or info["Where"] == where:
            ShowMode = client.STRINGS["inline"]["On"]
        swhere = where if where != "Here" else f"CHAT{info['chatid']}"
        owherebts.append(Button.inline(f"{where} {ShowMode}", data=f"SetQuick:Where:{quick}:{swhere}"))
    wherebts += list(client.functions.chunks(owherebts, 2))
    buttons += wherebts
    if info["Type"] != "Media":
        typebts = [[Button.inline("💡 Type : ⤵️", data="Empty")]]
        otypebts = []
        types = ["Normal", "Multi", "Edit", "Random", "Draft"] if len(info["Answers"].split(",")) > 1 else ["Normal", "Draft"]
        for type in types:
            ShowMode = client.STRINGS["inline"]["On"] if info["Type"] == type else client.STRINGS["inline"]["Off"]
            otypebts.append(Button.inline(f"{type} {ShowMode}", data=f"SetQuick:Type:{quick}:{type}"))
        typebts += list(client.functions.chunks(otypebts, 3))
        buttons += typebts
    client.STRINGS["inline"]["Yes"]
    findbts = [[Button.inline("🔎 Find : ⤵️", data="Empty")]]
    ofindbts = []
    findes = ["Yes", "No"] 
    for find in findes:
        ShowMode = client.STRINGS["inline"]["On"] if info["Finder"] == find else client.STRINGS["inline"]["Off"]
        ofindbts.append(Button.inline(f"{find} {ShowMode}", data=f"SetQuick:Finder:{quick}:{find}"))
    findbts += [ofindbts]
    buttons += findbts
    if info["Type"] != "Media" and len(info["Answers"].split(",")) > 1:
        sleepbts = [[Button.inline("💤 Sleep : ⤵️", data="Empty")]]
        osleepbts = []
        sleeps = [0, 0.2, 0.5, 1, 1.5, 2, 3, 4, 5]
        for sleep in sleeps:
            ShowMode = client.STRINGS["inline"]["On"] if info["Sleep"] == sleep else client.STRINGS["inline"]["Off"]
            osleepbts.append(Button.inline(f"{sleep} {ShowMode}", data=f"SetQuick:Sleep:{quick}:{sleep}"))
        sleepbts += list(client.functions.chunks(osleepbts, 3))
        buttons += sleepbts
    buttons.append([Button.inline("📥 Save ✅", data=f"SaveQuick:{quick}")])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"CloseQuick:{quick}")])
    return buttons

@client.Command(command="AddQuick \'([\s\S]*)\' ?([\s\S]*)?")
async def addquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)[:25]
    answers = event.pattern_match.group(2)[:500]
    quicks = client.DB.get_key("QUICKS") or {}
    rand = random.randint(111111111, 999999999)
    QName = f"Quick{str(rand)}"
    replyuser = event.reply_message.sender_id if event.is_reply else None
    if not answers:
        if not event.is_reply:
            return await event.edit(STRINGS["notans"])
        info = await event.reply_message.save()
        quicks.update({QName: {"Command": cmd, "Answers": info, "chatid": event.chat_id, "Reply": replyuser, "Person": "Sudo", "Where": "All", "Type": "Media", "Finder": "Yes", "Sleep": 1, "DO": False}})
    else:
        quicks.update({QName: {"Command": cmd, "Answers": answers, "chatid": event.chat_id, "Reply": replyuser, "Person": "Sudo", "Where": "All", "Type": "Normal", "Finder": "Yes", "Sleep": 1, "DO": False}})
    client.DB.set_key("QUICKS", quicks)
    res = await client.inline_query(client.bot.me.username, f"QuickPage:{QName}")
    if replyuser:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()
    
@client.Inline(pattern="QuickPage\:(.*)")
async def quickpage(event):
    quick = str(event.pattern_match.group(1))
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    answer = info["Answers"] if info["Type"] != "Media" else "Media"
    text = STRINGS["quickpage"].format(info["Command"], answer)
    buttons = get_buttons(quick)
    await event.answer([event.builder.article("FidoSelf - Quick Page", text=text, buttons=buttons)])

@client.Callback(data="SetQuick\:(.*)\:(.*)\:(.*)")
async def setqucik(event):
    Mode = event.data_match.group(1).decode('utf-8')
    quick = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    quicks[quick][Mode] = change 
    client.DB.set_key("QUICKS", quicks)
    answer = info["Answers"] if info["Type"] != "Media" else "Media"
    lasttext = STRINGS["quickpage"].format(info["Command"], answer)
    settext = STRINGS["setquick"].format(Mode, change)
    text = settext + "\n\n" + lasttext
    buttons = get_buttons(quick)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="SaveQuick\:(.*)")
async def savequcik(event):
    quick = event.data_match.group(1).decode('utf-8')
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[quick]
    quicks[quick]["DO"] = True 
    client.DB.set_key("QUICKS", quicks)
    answer = info["Answers"] if info["Type"] != "Media" else "Media"
    text = STRINGS["savequick"].format(info["Person"], info["Where"], info["Type"], info["Finder"], info["Sleep"], info["Command"], answer)
    await event.edit(text=text)

@client.Callback(data="CloseQuick\:(.*)")
async def closequcik(event):
    quick = event.data_match.group(1).decode('utf-8')
    quicks = client.DB.get_key("QUICKS") or {}
    del quicks[quick]
    client.DB.set_key("QUICKS", quicks)
    await event.edit(text=STRINGS["closequick"])