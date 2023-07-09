from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random

__INFO__ = {
    "Category": "Manage",
    "Name": "Quick",
    "Info": {
        "Help": "To Setting Your Quicks Answers!",
        "Commands": {
            "{CMD}Quicks <On-Off>": {
                "Help": "To Turn On-Off Quicks!"
            },
            "{CMD}AddQuick '<CMD>' <Answers>": {
                "Help": "To Add Quick To Quicks! ( Use , To Split Answers )",
                "Input": {
                    "<CMD>": "Command For Quick",
                    "<Answers>": "Answers For Quick",
                },
            },
            "{CMD}DelQuick <CMD>": {
                "Help": "To Delete Quick From Quicks!",
                "Input": {
                    "<CMD>": "Command For Quick",
                },
            },
            "{CMD}GetQuick <CMD>": {
                "Help": "To Getting Quick From Quicks!",
                "Input": {
                    "<CMD>": "Command For Quick",
                },
            },
            "{CMD}QuickList": {
                "Help": "To Getting Quicks List!",
            },
            "{CMD}CleanQuickList": {
                "Help": "To Cleaning Quicks List!",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} \ud804\udc4d The Quicks Mode Has Been {}!**",
    "notin": "**{STR} \ud804\udc4d The Command** ( `{}` ) **Not In Quicks Command Lists!**",
    "quickpage": "**{STR} \ud804\udc4d Select And Setting This Quick Answer:**\n\n**Command:** ( `{}` )\n**Answer:** ( `{}` )",
    "setquick": "**{STR} \u279c The {} Setting Was Set To** ( `{}` )",
    "savequick": "**{STR} \ud804\udc4d The Quick Answer Was Saved!**\n\n**\u272f Person:** ( `{}` )\n**\u272f Where:** ( `{}` )\n**\u272f Type:** ( `{}` )\n**\u272f Find:** ( `{}` )\n**\u272f Sleep:** ( `{}` )\n\n**\u272f Command:** ( `{}` )\n\n**\u272f Answer(s):** ( `{}` )",
    "delquick": "**{STR} \ud804\udc4d The Quick** ( `{}` ) **From List** ( `{} -> {} -> {}` ) **Has Been Deleted!**",
    "getquick": "**{STR} \u272f Command:** ( `{}` )\n\n**\u272f Answer(s):** ( `{}` )\n\n**\u272f Person:** ( `{}` )\n**\u272f Where:** ( `{}` )\n**\u272f Type:** ( `{}` )\n**\u272f Find:** ( `{}` )\n**\u272f Sleep:** ( `{}` )",
    "listdel": "**{STR} \ud804\udc4d Choose From Which List You Want** ( `{}` ) **Quick Answer To Be Deleted:**",
    "quicklist": "**{STR} \ud804\udc4d Select Each Quick Answer To View Its Information:**\n\n**\u272f Quicks Count:** ( `{}` )",
    "allempty": "**{STR} \ud804\udc4d The Quicks List Is Already Empty!**",
    "cleanquick": "**{STR} \ud804\udc4d The Quicks List Was Cleaned!**",
    "empty": "**{STR} \ud804\udc4d The Quicks List Is Empty!**"
}

@client.Command(command="Quick (On|Off)")
async def quickmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("QUICK_LIST_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(onlysudo=False, allowedits=False)
async def quicksupdate(event):
    if event.checkCmd() or not event.text: return
    QMode = client.DB.get_key("QUICK_LIST_MODE") or "ON"
    if QMode == "OFF": return
    quicks = client.DB.get_key("QUICK_LIST") or {}
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
            if info["Where"] == "Pv" and not event.is_private: continue
            if info["Where"].startswith("CHAT") and not event.chat_id == int(info["Where"].replace("CHAT", "")): continue
        MainAnswers = info["Answers"]
        if info["Type"] == "Normal":
            if info["Person"] == "Sudo":
                await event.delete()
                await event.respond(MainAnswers)
            else:
                await event.reply(MainAnswers)
            continue
        elif info["Type"] == "Random":
            SplitAnswers = MainAnswers.split(",")
            if info["Person"] == "Sudo":
                await event.edit(random.choice(SplitAnswers))
            else:
                await event.reply(random.choice(SplitAnswers))
            continue
        elif info["Type"] == "Multi":
            SplitAnswers = MainAnswers.split(",")
            if info["Person"] == "Sudo":
                await event.delete()
            for answer in SplitAnswers:
                if info["Person"] == "Sudo":
                    await event.respond(answer)
                else:
                    await event.reply(answer)
                await asyncio.sleep(eval(info["Sleep"]))
            continue
        elif info["Type"] == "Edit":
            SplitAnswers = MainAnswers.split(",")
            if info["Person"] == "Others":
                event = await event.reply(SplitAnswers[0])
                SplitAnswers = SplitAnswers[1:]
                if not SplitAnswers: continue
                await asyncio.sleep(eval(info["Sleep"]))
            for answer in SplitAnswers:
                await event.edit(answer)
                await asyncio.sleep(eval(info["Sleep"]))
            continue
        elif info["Type"] == "Media":
            if info["Person"] == "Sudo":
                await event.delete()
                getmsg = await client.get_messages(int(MainAnswers["chat_id"]), ids=int(MainAnswers["msg_id"]))
                await event.respond(getmsg)
            else:
                getmsg = await client.get_messages(int(MainAnswers["chat_id"]), ids=int(MainAnswers["msg_id"]))
                await event.reply(getmsg)
            continue
        elif info["Type"] == "Draft":
            if info["Person"] == "Sudo":
                await event.delete()
            await client(functions.messages.SaveDraftRequest(peer=event.chat_id, message=MainAnswers))
            continue

def get_buttons(quick):
    buttons = []
    Quicks = client.DB.get_key("QUICK_LIST") or {}
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
            ShowMode = client.STRINGS["inline"]["On"] if str(info["Sleep"]) == str(sleep) else client.STRINGS["inline"]["Off"]
            osleepbts.append(Button.inline(f"{sleep} {ShowMode}", data=f"SetQuick:Sleep:{quick}:{sleep}"))
        sleepbts += list(client.functions.chunks(osleepbts, 3))
        buttons += sleepbts
    buttons.append([Button.inline("📥 Save ✅", data=f"SaveQuick:{quick}"), Button.inline(client.STRINGS["inline"]["Delete"], data=f"DelQuick:{quick}")])
    return buttons

@client.Command(command="AddQuick \'([\s\S]*)\' ?([\s\S]*)?")
async def addquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)[:25]
    answers = event.pattern_match.group(2)[:500]
    quicks = client.DB.get_key("QUICK_LIST") or {}
    rand = random.randint(111111111, 999999999)
    QName = f"Quick{str(rand)}"
    replyuser = event.reply_message.sender_id if event.is_reply else None
    if not answers:
        if not event.is_reply:
            return await event.edit(client.getstrings(STRINGS)["notans"])
        info = await event.reply_message.save()
        quicks.update({QName: {"Command": cmd, "Answers": info, "chatid": event.chat_id, "Reply": replyuser, "Person": "Sudo", "Where": "All", "Type": "Media", "Finder": "Yes", "Sleep": 0, "DO": False}})
    else:
        quicks.update({QName: {"Command": cmd, "Answers": answers, "chatid": event.chat_id, "Reply": replyuser, "Person": "Sudo", "Where": "All", "Type": "Normal", "Finder": "Yes", "Sleep": 0, "DO": False}})
    client.DB.set_key("QUICK_LIST", quicks)
    res = await client.inline_query(client.bot.me.username, f"QuickPage:{QName}")
    if replyuser:
        await res[0].click(event.chat_id, reply_to=event.reply_message.id)
    else:
        await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="DelQuick ([\s\S]*)")
async def delquick(event):
    await event.edit(client.STRINGS["wait"])
    command = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICK_LIST") or {}
    quicklist = []
    for quick in quicks:
        if command == quicks[quick]["Command"]:
            quicklist.append(quicks[quick])
    if not quicklist:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(command))
    res = await client.inline_query(client.bot.me.username, f"QuickDel:{command}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Command(command="GetQuick (.*)")
async def getquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)
    quicks = client.DB.get_key("QUICK_LIST") or {}
    quicklist = []
    for quick in quicks:
        if cmd == quicks[quick]["Command"]:
            quicklist.append(quick)
    if not quicklist:
        return await event.edit(client.getstrings(STRINGS)["notin"].format(cmd))    
    for squick in quicklist:
        info = quicks[squick]
        if info["Type"] == "Media":
            msg = await client.get_messages(int(info["Answers"]["chat_id"]), ids=int(info["Answers"]["msg_id"]))
            send = await event.respond(msg)
            await send.reply(client.getstrings(STRINGS)["getquick"].format(info["Command"], "Repleyed Message", info["Person"], info["Where"], info["Type"], info["Finder"], info["Sleep"]))
        else:
            await event.respond(client.getstrings(STRINGS)["getquick"].format(info["Command"], info["Answers"], info["Person"], info["Where"], info["Type"], info["Finder"], info["Sleep"]))
    await event.delete()

@client.Command(command="QuickList")
async def quicklist(event):
    await event.edit(client.STRINGS["wait"])
    quicks = client.DB.get_key("QUICK_LIST") or {}
    if not quicks:
        return await event.edit(client.getstrings(STRINGS)["empty"])    
    res = await client.inline_query(client.bot.me.username, "QuickList")
    await res[0].click(event.chat_id, reply_to=event.id)
    await event.delete()
    
@client.Command(command="CleanQuickList")
async def cleanquicklist(event):
    await event.edit(client.STRINGS["wait"])
    quicks = client.DB.get_key("QUICK_LIST") or {}
    if not quicks:
        return await event.edit(client.getstrings(STRINGS)["allempty"])
    client.DB.del_key("QUICK_LIST")
    await event.edit(client.getstrings(STRINGS)["cleanquick"])

@client.Inline(pattern="QuickPage\:(.*)")
async def quickpage(event):
    quick = str(event.pattern_match.group(1))
    quicks = client.DB.get_key("QUICK_LIST") or {}
    info = quicks[quick]
    answer = info["Answers"] if info["Type"] != "Media" else "Media"
    text = client.getstrings(STRINGS)["quickpage"].format(info["Command"], answer)
    buttons = get_buttons(quick)
    await event.answer([event.builder.article("FidoSelf - Quick Page", text=text, buttons=buttons)])

@client.Callback(data="SetQuick\:(.*)\:(.*)\:(.*)")
async def setqucik(event):
    Mode = event.data_match.group(1).decode('utf-8')
    quick = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    quicks = client.DB.get_key("QUICK_LIST") or {}
    info = quicks[quick]
    quicks[quick][Mode] = change 
    client.DB.set_key("QUICK_LIST", quicks)
    answer = info["Answers"] if info["Type"] != "Media" else "Media"
    lasttext = client.getstrings(STRINGS)["quickpage"].format(info["Command"], answer)
    settext = client.getstrings(STRINGS)["setquick"].format(Mode, change)
    text = settext + "\n\n" + lasttext
    buttons = get_buttons(quick)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="SaveQuick\:(.*)")
async def savequcik(event):
    quick = event.data_match.group(1).decode('utf-8')
    quicks = client.DB.get_key("QUICK_LIST") or {}
    info = quicks[quick]
    quicks[quick]["DO"] = True 
    client.DB.set_key("QUICK_LIST", quicks)
    answer = info["Answers"] if info["Type"] != "Media" else "Media"
    text = client.getstrings(STRINGS)["savequick"].format(info["Person"], info["Where"], info["Type"], info["Finder"], info["Sleep"], info["Command"], answer)
    await event.edit(text=text)

@client.Inline(pattern="QuickDel\:(.*)")
async def inlinedelquick(event):
    command = str(event.pattern_match.group(1))
    text = client.getstrings(STRINGS)["listdel"].format(command)
    quicks = client.DB.get_key("QUICK_LIST") or {}
    quicklist = []
    for quick in quicks:
        if command == quicks[quick]["Command"] and quicks[quick]["DO"]:
            quicklist.append(quick)
    buttons = []
    for quick in quicklist:
        info = quicks[quick]
        ShowName = f'( {info["Person"]} ) - ( {info["Where"]} ) - ( {info["Type"]} )'
        buttons.append([Button.inline(ShowName, data=f"DelQuick:{quick}")])
    await event.answer([event.builder.article("FidoSelf - Del Quick", text=text, buttons=buttons)])

@client.Callback(data="DelQuick\:(.*)")
async def delqucik(event):
    quick = event.data_match.group(1).decode('utf-8')
    quicks = client.DB.get_key("QUICK_LIST") or {}
    info = quicks[quick]
    text = client.getstrings(STRINGS)["delquick"].format(info["Command"], info["Person"], info["Where"], info["Type"])
    await event.edit(text=text)
    del quicks[quick]
    client.DB.set_key("QUICK_LIST", quicks)
    
@client.Inline(pattern="QuickList")
async def inlinequicklist(event):
    quicks = client.DB.get_key("QUICK_LIST") or {}
    text = client.getstrings(STRINGS)["quicklist"].format(len(quicks))
    buttons = []
    for quick in list(quicks)[:10]:
        info = quicks[quick]
        ShowName = f'[ {info["Command"]} ] ( {info["Person"]} ) - ( {info["Where"]} ) - ( {info["Type"]} )'
        buttons.append([Button.inline(ShowName, data=f"ViweQuick:{quick}:1")])
    if len(quicks) > 10:
        buttons.append([Button.inline(client.STRINGS["inline"]["Next"], data=f"QuickListPage:2")])
    await event.answer([event.builder.article("FidoSelf - List Quick", text=text, buttons=buttons)])

@client.Callback(data="QuickListPage\:(.*)")
async def listquickspage(event):
    page = str(event.data_match.group(1).decode('utf-8'))
    quicks = client.DB.get_key("QUICK_LIST") or {}
    text = client.getstrings(STRINGS)["quicklist"].format(len(quicks))
    buttons = []
    qcount = (int(page) * 10)
    for quick in list(quicks)[(qcount-10):qcount]:
        info = quicks[quick]
        ShowName = f'[ {info["Command"]} ] ( {info["Person"]} ) - ( {info["Where"]} ) - ( {info["Type"]} )'
        buttons.append([Button.inline(ShowName, data=f"ViweQuick:{quick}:{page}")])
    pbts = []
    if int(page) != 1:
        pbts.append(Button.inline(client.STRINGS["inline"]["BackPage"], data=f"QuickListPage:{int(page)-1}"))
    if len(quicks) > qcount:
        pbts.append(Button.inline(client.STRINGS["inline"]["NextPage"], data=f"QuickListPage:{int(page)+1}"))
    buttons.append(pbts)
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="ViweQuick\:(.*)\:(.*)")
async def viewquicks(event):
    quick = str(event.data_match.group(1).decode('utf-8'))
    page = str(event.data_match.group(2).decode('utf-8'))
    quicks = client.DB.get_key("QUICK_LIST") or {}
    info = quicks[quick]
    answers = info["Answers"] if info["Type"] != "Media" else "Media"
    text = client.getstrings(STRINGS)["getquick"].format(info["Command"], answers, info["Person"], info["Where"], info["Type"], info["Finder"], info["Sleep"])
    buttons = [[Button.inline(client.STRINGS["inline"]["Delete"], data=f"DelQuick:{quick}"), Button.inline(client.STRINGS["inline"]["Back"], data=f"QuickListPage:{page}")]]
    await event.edit(text=text, buttons=buttons)