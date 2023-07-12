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
    "pass": "**{STR} Your Password:** ( `{}` )\n\n`{}`"
}

@client.Command(command="SP(Easy|Medium|Hard) (\d*)")
async def password(event):
    edit = await event.tryedit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).title()
    count = int(event.pattern_match.group(2))
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
    text = client.getstrings(STRINGS)["pass"].format(type, password)
    await edit.edit(text)