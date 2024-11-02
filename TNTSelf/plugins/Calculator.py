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
    "uncalc": "{STR} This Operation Is InValid!",
    "notcalc": "{STR} The Calculator Operation Is Empty!",
    "rescalc": "**{STR} Your Operation:** ( `{}` )\n\n**{STR} Result:** ( `{}` )",
}

NUMS = ["１", "２", "３", "４", "５", "６", "７", "８", "９", "０"]
OPERS =  ["✚", "-", "×", "÷"]
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
    "×": "*",
    "÷": "/",
}
    
def get_calc_buttons():
    buttons = [[Button.inline("🆑", data=f"ClearCalc"), Button.inline("⌫", data=f"DelCalc")]]
    otherbuttons = []
    for othbts in OPERS:
        otherbuttons.append(Button.inline(othbts, data=f"AddCalc:{othbts}"))
    otherbuttons = list(client.functions.chunks(otherbuttons, 4))
    numbuttons = []
    for num in NUMS:
        numbuttons.append(Button.inline(num, data=f"AddCalc:{num}"))
    numbuttons = list(client.functions.chunks(numbuttons, 3))
    resbutton = [[Button.inline("=", data=f"CalcRes")]]
    buttons += otherbuttons + numbuttons + resbutton
    return buttons

@client.Command(command="Calc")
async def calculator(event):
    await event.edit(client.STRINGS["wait"])
    res = await client.inline_query(client.bot.me.username, "Calc")
    await res[0].click(event.chat_id)
    await event.delete()

@client.Inline(pattern="Calc")
async def inlinecalculator(event):
    data = client.DB.get_key("CALCULATOR") or "Empty"
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons()
    await event.answer([event.builder.article("TNTSelf - Calculator", text=text, buttons=buttons)])

@client.Callback(data="AddCalc\\:(.*)")
async def addcalculator(event):
    string = str(event.data_match.group(1).decode('utf-8'))
    getdata = client.DB.get_key("CALCULATOR") or "Empty"
    if getdata == "Empty":
        if string in OPERS or string == "0":
            return await event.answer(client.getstrings(STRINGS)["uncalc"], alert=True)
        data = string
    else:
        if str(getdata)[-1] in OPERS and (string in OPERS or string == "0"):
            return await event.answer(client.getstrings(STRINGS)["uncalc"], alert=True)
        data = str(getdata) + string
    client.DB.set_key("CALCULATOR", data)
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="DelCalc\\:(.*)\\:(.*)")
async def delcalculator(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    msgid = int(event.data_match.group(2).decode('utf-8'))
    getdata = client.DB.get_key("CALCULATOR") or "Empty"
    if getdata == "Empty":
        return await event.answer(client.getstrings(STRINGS)["notcalc"], alert=True)
    data = str(getdata)[:-1]
    data = data if data else "Empty"
    client.DB.set_key("CALCULATOR", data)
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="CalcRes\\:(.*)\\:(.*)")
async def rescalculator(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    msgid = int(event.data_match.group(2).decode('utf-8'))
    data = client.DB.get_key("CALCULATOR") or "Empty"
    if data == "Empty":
        return await event.answer(client.getstrings(STRINGS)["notcalc"], alert=True)
    newdata = data
    for element in BUTTONS:
        newdata = newdata.replace(element, BUTTONS[element])
    result = eval(newdata)
    client.DB.set_key("CALCULATOR", "Empty")
    text = client.getstrings(STRINGS)["rescalc"].format(data, result)
    await event.edit(text=text)

@client.Callback(data="ClearCalc\\:(.*)\\:(.*)")
async def clearcalculator(event):
    chatid = int(event.data_match.group(1).decode('utf-8'))
    msgid = int(event.data_match.group(2).decode('utf-8'))
    client.DB.set_key("CALCULATOR", "Empty")
    text = client.getstrings(STRINGS)["calc"].format("Empty")
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)