from TNTSelf import client
from telethon import functions, Button
import re

__INFO__ = {
    "Category": "Manage",
    "Name": "Calculator",
    "Info": {
        "Help": "To Get Calculator Menu For Operations!",
        "Commands": {
            "{CMD}Calc": {
                "Help": "To Get Calculator",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "calc": "**{STR} Use Following Options For The Calculator:**\n\n**{STR} Operation:** ( `{}` )",
}

NUMS = ["１", "２", "３", "４", "５", "６", "７", "８", "９", "０"]
    
def get_calc_buttons(chatid, msgid):
    numbuttons = []
    for num in NUMS:
        numbuttons.append(Button.inline(num, data=f"AddCalc:{chatid}:{msgid}:{num}"))
    buttons = list(client.functions.chunks(numbuttons, 3))
    otherbuttons = ["+", "-", "×", "÷"]
    for othbts in otherbuttons:
        buttons.append([Button.inline(othbts, data=f"AddCalc:{chatid}:{msgid}:{othbts}")])
    return buttons

async def get_calc_data(chatid, msgid):
    message = await client.get_messages(chatid, ids=msgid)
    if not message:
        return "Empty"
    match = "Operation\\: \\( (.*) \\)"
    search = re.search(match, message.raw_text)
    if not search:
        return "Empty"
    data = search.group(1)
    return data

@client.Command(command="Calc")
async def calculator(event):
    await event.edit(client.STRINGS["wait"])
    chatid = event.chat_id
    msgid = event.id
    res = await client.inline_query(client.bot.me.username, f"Calc:{chatid}:{msgid}")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Calc\\:(.*)\\:(.*)")
async def inlinecalculator(event):
    chatid = int(event.pattern_match.group(1))
    msgid = int(event.pattern_match.group(2))
    data = await get_calc_data(chatid, msgid)
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons(chatid, msgid)
    await event.answer([event.builder.article("TNTSelf - Calculator", text=text, buttons=buttons)])

@client.Callback(data="AddCalc\\:(.*)\\:(.*)\\:(.*)")
async def addcalculator(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    msgid = int(event.data_match.group(2).decode('utf-8'))
    string = str(event.data_match.group(3).decode('utf-8'))
    data = await get_calc_data(chatid, msgid)
    data = str(data) + string
    data = data.replace("Empty", "")
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons(chatid, msgid)
    await event.edit(text=text, buttons=buttons)