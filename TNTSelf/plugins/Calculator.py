from TNTSelf import client
from telethon import functions, Button

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
    "notcalc": "{STR} The Calculator Operation Is Empty!",
    "rescalc": "**{STR} Your Operation:** ( `{}` )\n\n**{STR} Result:** ( `{}` )",
}

NUMS = ["１", "２", "３", "４", "５", "６", "７", "８", "９", "０"]
BUTTONS = {
    "０": "0",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
    "６": "6",
    "７": "7",
    "８": "8",
    "９": "9",
    "✚": "+",
}
    
def get_calc_buttons(chatid, msgid):
    buttons = []
    otherbuttons = ["✚", "-", "×", "÷"]
    for othbts in otherbuttons:
        buttons.append(Button.inline(othbts, data=f"AddCalc:{chatid}:{msgid}:{othbts}"))
    buttons = list(client.functions.chunks(buttons, 4))
    numbuttons = []
    for num in NUMS:
        numbuttons.append(Button.inline(num, data=f"AddCalc:{chatid}:{msgid}:{num}"))
    numbuttons = list(client.functions.chunks(numbuttons, 3))
    resbutton = [[Button.inline("=", data=f"CalcRes:{chatid}:{msgid}")]]
    buttons = buttons + numbuttons + resbutton
    return buttons

async def get_calc_data(chatid, msgid):
    message = await client.get_messages(chatid, ids=msgid)
    if not message:
        return "Empty"
    return message.text

@client.Command(command="Calc")
async def calculator(event):
    await event.edit(client.STRINGS["wait"])
    message = await client.bot.send_message(client.REALM, "Empty")
    chatid = message.chat_id
    msgid = message.id
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
    getdata = await get_calc_data(chatid, msgid)
    data = str(getdata) + str(string)
    data = data.replace("Empty", "")
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons(chatid, msgid)
    await event.edit(text=text, buttons=buttons)
    await client.bot.edit_message(chatid, msgid, data)
    
@client.Callback(data="CalcRes\\:(.*)\\:(.*)")
async def rescalculator(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    msgid = int(event.data_match.group(2).decode('utf-8'))
    data = await get_calc_data(chatid, msgid)
    if data == "Empty":
        return await event.answer(client.getstrings(STRINGS)["notcalc"], alert=True)
    newdata = data
    for element in BUTTONS:
        newdata = newdata.replace(element, BUTTONS[element])
    text = client.getstrings(STRINGS)["rescalc"].format(data, eval(newdata))
    await event.edit(text=text)