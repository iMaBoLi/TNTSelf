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
    "uncalc": "• This Operation Is InValid!",
    "notcalc": "• The Calculator Operation Is Empty!",
    "invcalc": "• The Calculator Operation Is InValid!",
    "longcalc": "• The Calculator Operation Is Too Long!",
    "rescalc": "**{STR} Operation:** ( `{}` )\n**{STR} Result:** ( `{}` )\n\n**{STR} Use Following Options For The Calculator:**",
}

NUMS = ["𝟭", "𝟮", "𝟯", "𝟰", "𝟱", "𝟲", "𝟳", "𝟴", "𝟵", "𝟬"]
OPERS = ["➕", "➖", "✖️", "➗"]
POPERS = ["π"]
BUTTONS = {
    "𝟭": "1",
    "𝟮": "2",
    "𝟯": "3",
    "𝟰": "4",
    "𝟱": "5",
    "𝟲": "6",
    "𝟳": "7",
    "𝟴": "8",
    "𝟵": "9",
    "𝟬": "0",
    "➕": "+",
    "➖": "-",
    "✖️": "*",
    "➗": "/",
    "π": "3.141592653589793238",
}
    
def get_calc_buttons():
    buttons = [[Button.inline("©", data=f"ClearCalc"), Button.inline("⌫", data=f"DelCalc")]]
    otherbuttons = []
    for othbts in OPERS:
        otherbuttons.append(Button.inline(othbts, data=f"AddCalc:{othbts}"))
    otherbuttons = list(client.functions.chunks(otherbuttons, 4))
    majbuttons = []
    for majbts in ["π", "(", ")"]:
        majbuttons.append(Button.inline(majbts, data=f"AddCalc:{majbts}"))
    majbuttons = list(client.functions.chunks(majbuttons, 4))
    numbuttons = []
    for num in NUMS:
        numbuttons.append(Button.inline(num, data=f"AddCalc:{num}"))
    numbuttons = list(client.functions.chunks(numbuttons, 3))
    resbutton = [[Button.inline("🟰", data=f"CalcRes")]]
    buttons += otherbuttons + majbuttons + numbuttons + resbutton
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
        if string in OPERS or string == "𝟬":
            text = client.getstrings(STRINGS)["uncalc"]
            return await event.answer(text, alert=True)
        data = string
    else:
        if len(getdata) > 500:
            text = client.getstrings(STRINGS)["longcalc"]
            return await event.answer(text, alert=True)
        if str(getdata)[-1] in OPERS and string in OPERS:
            text = client.getstrings(STRINGS)["uncalc"]
            return await event.answer(text, alert=True)
        if str(getdata)[-1] in POPERS and (string in NUMS or string in POPERS):
            text = client.getstrings(STRINGS)["uncalc"]
            return await event.answer(text, alert=True)
        if str(getdata)[-1] in OPERS and string == "𝟬":
            text = client.getstrings(STRINGS)["uncalc"]
            return await event.answer(text, alert=True)
        data = str(getdata) + string
    client.DB.set_key("CALCULATOR", data)
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="DelCalc")
async def delcalculator(event):
    getdata = client.DB.get_key("CALCULATOR") or "Empty"
    if getdata == "Empty":
        text = client.getstrings(STRINGS)["notcalc"]
        return await event.answer(text, alert=True)
    data = str(getdata)[:-1]
    data = data if data else "Empty"
    client.DB.set_key("CALCULATOR", data)
    text = client.getstrings(STRINGS)["calc"].format(data)
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="CalcRes")
async def rescalculator(event):
    data = client.DB.get_key("CALCULATOR") or "Empty"
    if data == "Empty":
        text = client.getstrings(STRINGS)["notcalc"]
        return await event.answer(text, alert=True)
    newdata = data[:-1] if data[-1] in OPERS else data
    for element in BUTTONS:
        newdata = newdata.replace(element, BUTTONS[element])
    try:
        result = eval(newdata)
    except:
        text = client.getstrings(STRINGS)["invcalc"]
        return await event.answer(text, alert=True)
    client.DB.set_key("CALCULATOR", "Empty")
    text = client.getstrings(STRINGS)["rescalc"].format(data, result)
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)

@client.Callback(data="ClearCalc")
async def clearcalculator(event):
    data = client.DB.get_key("CALCULATOR") or "Empty"
    if data == "Empty":
        text = client.getstrings(STRINGS)["notcalc"]
        return await event.answer(text, alert=True)
    client.DB.set_key("CALCULATOR", "Empty")
    text = client.getstrings(STRINGS)["calc"].format("Empty")
    buttons = get_calc_buttons()
    await event.edit(text=text, buttons=buttons)