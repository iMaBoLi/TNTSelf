from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random

STRINGS = {
    "quickpage": "**Select And Setting Quick Answer:**\n\n**Command:** ( `{}` )\n**Answer:** ( `{}` )",
    "setquick": "**The {} Setting Was Set To** ( `{}` )",
    "savequick": "**The New Quick Answer Was Saved!**\n\n**Person:** ( `{}` )\n**Where:** ( `{}` )\n**Type:** ( `{}` )\n**Find:** ( `{}` )\n**Sleep:** ( `{}` )\n\n**Command:** ( `{}` )\n\n**Answer(s):** ( `{}` )",
    "closequick": "**The Quick Panel Successfully Closed!**",
}

def get_buttons(quick):
    buttons = []
    Quicks = client.DB.get_key("QUICKS") or {}
    info = Quicks[quick]
    perbts = [[Button.inline("• Person :", data="Empty")]]
    operbts = []
    persons = ["Sudo", "Others", "Replyed User"] if info["Reply"] else ["Sudo", "Others"] 
    for person in persons:
        ShowMode = client.STRINGS["inline"]["Off"]
        if (person == "Replyed User" and info["Person"].startswith("USER")) or info["Person"] == person:
            ShowMode = client.STRINGS["inline"]["On"]
        sperson = person if person != "Replyed User" else f"USER{info['Reply']}"
        operbts.append(Button.inline(f"• {person} {ShowMode} •", data=f"SetQuick:Person:{quick}:{sperson}"))
    perbts += [operbts]
    buttons += perbts
    wherebts = [[Button.inline("• Place :", data="Empty")]]
    owherebts = []
    wheres = ["All", "Pv", "Groups", "Here"] 
    for where in wheres:
        ShowMode = client.STRINGS["inline"]["Off"]
        if (where == "Here" and info["Where"].startswith("CHAT")) or info["Where"] == where:
            ShowMode = client.STRINGS["inline"]["On"]
        swhere = where if where != "Here" else f"CHAT{info['chatid']}"
        owherebts.append(Button.inline(f"• {where} {ShowMode} •", data=f"SetQuick:Where:{quick}:{swhere}"))
    wherebts += [owherebts]
    buttons += wherebts
    if info["Type"] != "Media":
        typebts = [[Button.inline("• Type :", data="Empty")]]
        otypebts = []
        types = ["Normal", "Multi", "Edit", "Random", "Draft"] if len(info["Answers"].split(",")) > 1 else ["Normal", "Draft"]
        for type in types:
            ShowMode = client.STRINGS["inline"]["On"] if info["Type"] == type else client.STRINGS["inline"]["Off"]
            otypebts.append(Button.inline(f"• {type} {ShowMode} •", data=f"SetQuick:Type:{quick}:{type}"))
        typebts += list(client.functions.chunks(otypebts, 3))
        buttons += typebts
    client.STRINGS["inline"]["Yes"]
    findbts = [[Button.inline("• Find :", data="Empty")]]
    ofindbts = []
    findes = ["Yes", "No"] 
    for find in findes:
        ShowMode = client.STRINGS["inline"]["On"] if info["Finder"] == find else client.STRINGS["inline"]["Off"]
        ofindbts.append(Button.inline(f"• {find} {ShowMode} •", data=f"SetQuick:Finder:{quick}:{find}"))
    findbts += [ofindbts]
    buttons += findbts
    if info["Type"] != "Media" and len(info["Answers"].split(",")) > 1:
        sleepbts = [[Button.inline("• Sleep :", data="Empty")]]
        osleepbts = []
        sleeps = [0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 10]
        for sleep in sleeps:
            ShowMode = client.STRINGS["inline"]["On"] if info["Sleep"] == sleep else client.STRINGS["inline"]["Off"]
            osleepbts.append(Button.inline(f"• {sleep} {ShowMode} •", data=f"SetQuick:Sleep:{quick}:{sleep}"))
        sleepbts += list(client.functions.chunks(osleepbts, 4))
        buttons += sleepbts
    buttons.append([Button.inline("• Save •", data=f"SaveQuick:{quick}")])
    buttons.append([Button.inline(client.STRINGS["inline"]["Close"], data=f"CloseQuick:{quick}")])
    return buttons

@client.Command(command="AddQuick \'([\s\S]*)\' ?([\s\S]*)?")
async def addquick(event):
    await event.edit(client.STRINGS["wait"])
    cmd = event.pattern_match.group(1)
    answers = event.pattern_match.group(2)
    quicks = client.DB.get_key("QUICKS") or {}
    rand = random.randint(111111111, 999999999)
    QName = f"Quick-{str(rand)}"
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
    answer = info["Answers"] if info["Type"] == "Text" else "Media"
    text = STRINGS["quickpage"].format(info["Command"], answer)
    buttons = get_buttons(quick)
    await event.answer([event.builder.article("FidoSelf - Quick Page", text=text, buttons=buttons)])

@client.Callback(data="SetQucik\:(.*)\:(.*)\:(.*)")
async def SetQucik(event):
    Mode = event.data_match.group(1).decode('utf-8')
    quick = event.data_match.group(2).decode('utf-8')
    change = event.data_match.group(3).decode('utf-8')
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[qucik]
    quicks[quick][Mode] = change 
    client.DB.get_key("QUICKS", quicks)
    answer = info["Answers"] if info["Type"] == "Text" else "Media"
    lasttext = STRINGS["quickpage"].format(info["Command"], answer)
    settext = STRINGS["setquick"].format(Mode, change)
    text = settext + "\n\n" + lasttext
    buttons = get_buttons(quick)
    await event.edit(text=text, buttons=buttons)
    
@client.Callback(data="SaveQucik\:(.*)")
async def savequcik(event):
    quick = event.data_match.group(1).decode('utf-8')
    quicks = client.DB.get_key("QUICKS") or {}
    info = quicks[qucik]
    quicks[quick]["DO"] = True 
    client.DB.get_key("QUICKS", quicks)
    answer = info["Answers"] if info["Type"] == "Text" else "Media"
    text = STRINGS["savequick"].format(info["Person"], info["Where"], info["Type"], info["Find"], info["Sleep"], info["Command"], answer)
    await event.edit(text=text)

@client.Callback(data="CloseQucik\:(.*)")
async def closequcik(event):
    quick = event.data_match.group(1).decode('utf-8')
    quicks = client.DB.get_key("QUICKS") or {}
    del quicks[qucik]
    client.DB.get_key("QUICKS", quicks)
    await event.edit(text=STRINGS["closequick"])