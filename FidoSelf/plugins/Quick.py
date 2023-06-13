from FidoSelf import client
from telethon import functions, types, Button
import asyncio, random

STRINGS = {
    "notans": "**Enter Text Answers Or Reply To Message!**",
    "notin": "**The Command** ( `{}` ) **Not In Quicks Command Lists!**",
    "get": "**Command:** ( `{}` )\n\n**Answer(s):** ( `{}` )\n\n**Person:** ( `{}` )\n**Where:** ( `{}` )\n**Type:** ( `{}` )\n**Find:** ( `{}` )\n**Sleep:** ( `{}` )",
    "empty": "**The Quicks List Is Empty!**",
    "Person": "**Select You Want This Quick Answer To Be Saved For Person:**",
    "Where": "**Choose Where You Want This Quick Answer To Be Saved:**",
    "Type": "**Select The Type Of This Quick Answer:**",
    "search": "**Select Whether To Search For This Quick Answer Command In Messages:**",
    "Sleep": "**Choose A Sleep Time Between Each Answer:**",
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
        if (person == "Replyed User" and info["Person"].startswith("USER")) or info["Person"] == person:
            ShowMode = client.STRINGS["On"]
        sperson = person if person != "Replyed User" else f"USER{info['reply']}"
        operbts.append(Button.inline(f"• {person} {ShowMode} •", data=f"SetQuick:Person:{quick}:{sperson}"))
    perbts += [operbts]
    buttons += perbts
    wherebts = [[Button.inline("• Place :", data="Empty")]]
    owherebts = []
    wheres = ["All", "Pv", "Groups", "Here"] 
    for where in wheres:
        ShowMode = client.STRINGS["Off"]
        if (where == "Here" and info["Where"].startswith("CHAT")) or info["Where"] == where:
            ShowMode = client.STRINGS["On"]
        swhere = where if where != "Here" else f"CHAT{info['chatid']}"
        owherebts.append(Button.inline(f"• {where} {ShowMode} •", data=f"SetQuick:Where:{quick}:{swhere}"))
    wherebts += [owherebts]
    buttons += wherebts
    if info["Type"] != "Media":
        typebts = [[Button.inline("• Type :", data="Empty")]]
        otypebts = []
        types = ["Normal", "Multi", "Edit", "Random", "Draft"] if len(info["Answers"].split(",")) > 1 else ["Normal", "Draft"]
        for type in types:
            ShowMode = client.STRINGS["On"] if info["Type"] == type else client.STRINGS["Off"]
            otypebts.append(Button.inline(f"• {type} {ShowMode} •", data=f"SetQuick:Type:{quick}:{type}"))
        typebts += list(client.functions.chunks(otypebts, 3))
        buttons += typebts
    client.STRINGS["inline"]["Yes"]
    findbts = [[Button.inline("• Find :", data="Empty")]]
    ofindbts = []
    findes = ["Yes", "No"] 
    for find in findes:
        ShowMode = client.STRINGS["On"] if info["Finder"] == find else client.STRINGS["Off"]
        ofindbts.append(Button.inline(f"• {find} {ShowMode} •", data=f"SetQuick:Finder:{quick}:{find}"))
    findbts += [ofindbts]
    buttons += findbts
    if info["Type"] != "Media" and len(info["Answers"].split(",")) > 1:
        sleepbts = [[Button.inline("• Sleep :", data="Empty")]]
        osleepbts = []
        sleeps = [0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 10]
        for sleep in sleeps:
            ShowMode = client.STRINGS["On"] if info["Sleep"] == sleep else client.STRINGS["Off"]
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
        quicks.update({QName: {"Command": cmd, "Answers": info, "chatid": event.chat_id, "reply": replyuser, "Person": "Sudo", "Where": "All", "Type": "Media", "Finder": "Yes", "Sleep": 1, "DO": False}})
    else:
        quicks.update({QName: {"Command": cmd, "Answers": answers, "chatid": event.chat_id, "reply": replyuser, "Person": "Sudo", "Where": "All", "Type": "Normal", "Finder": "Yes", "Sleep": 1, "DO": False}})
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
    text = "Hi"
    buttons = get_buttons(quick)
    open("Bt.txt", "w").write(str(buttons))
    await client.send_file("me", "Bt.txt")
    await event.answer([event.builder.article("FidoSelf - Quick Page", text=text, buttons=buttons)])
