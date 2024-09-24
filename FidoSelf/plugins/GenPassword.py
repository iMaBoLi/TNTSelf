from FidoSelf import client
import string
import random

__INFO__ = {
    "Category": "Funs",
    "Name": "Password",
    "Info": {
        "Help": "To Generate Random Passwords!",
        "Commands": {
            "{CMD}SPEasy <Count>": {
                "Help": "To Craete Easy Password",
                "Input": {
                    "<Count>": "Number Of Password",
                },
            },
            "{CMD}SPMedium <Count>": {
                "Help": "To Craete Medium Password",
                "Input": {
                    "<Count>": "Number Of Password",
                },
            },
            "{CMD}SPHard <Count>": {
                "Help": "To Craete Hard Password",
                "Input": {
                    "<Count>": "Number Of Password",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "EN": {
        "pass": "**{STR} Your Password:** ( `{}` )\n\n`{}`"
    },
    "FA": {
        "pass": "**{STR} پسوورد شما:** ( `{}` )\n\n`{}`"
    },
}

@client.Command(command="SP(Easy|Medium|Hard) (\d*)")
async def password(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).title()
    count = int(event.pattern_match.group(2))
    count = count if count < 20 else 20
    if type == "Easy":
        characters = string.ascii_letters
    elif type == "Medium":
        characters = string.ascii_letters + string.digits
    elif type == "Hard":
        characters = string.ascii_letters + string.digits + ".,*:;!?@#$_&-+()/~|÷×={}[]\%"
    characters = characters.replace("`", "")
    characters = characters.replace(" ", "")
    password = ""
    for i in range(count):
        password += random.choice(characters)
    text = client.getstring(STRINGS, "pass").format(type, password)
    await event.edit(text)