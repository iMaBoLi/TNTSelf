from FidoSelf import client
import string
import random

__INFO__ = {
    "Category": "Funs",
    "Name": "Password",
    "Info": {
        "Help": "To Generate Random Passwords!",
        "Commands": {
            "{CMD}GenPass <Count>": {
                "Help": "To Generate Password",
                "Input": {
                    "<Count>": "Number Of Password",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "pass": "**{STR} Passwords:**:\n\n    **{STR} Easy:** ( `{}` )\n    **{STR} Medium:** ( `{}` )\n    **{STR} Hard:** ( `{}` )"
}

@client.Command(command="GenPass (\\\d*)")
async def password(event):
    await event.edit(client.STRINGS["wait"])
    count = int(event.pattern_match.group(1))
    count = count if count < 20 else 20
    easy = string.ascii_letters
    medium = string.ascii_letters + string.digits
    hard = string.ascii_letters + string.digits + ".,*:;!?@#$_&-+()/~|÷×={}[]%"
    easypass = ""
    mediumpass = ""
    hardpass = ""
    for i in range(count):
        easychr = easy.replace("`", "").replace(" ", "")
        easypass += random.choice(easychr)
        mediumchr = medium.replace("`", "").replace(" ", "")
        mediumpass += random.choice(mediumchr)
        hardchr = hard.replace("`", "").replace(" ", "")
        hardpass += random.choice(hardchr)
    text = client.getstrings(STRINGS)["pass"].format(easypass, mediumpass, hardpass)
    await event.edit(text)