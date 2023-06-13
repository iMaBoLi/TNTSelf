from FidoSelf import client
import string
import random

STRINGS = {
    "pass": "**Your Password:** ( `{}` )\n\n`{}`",
}

@client.Command(command="SP(Easy|Medium|Hard) ?(\d*)?")
async def password(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).title()
    count = int(event.pattern_match.group(2) or 8)
    if type == "Easy":
        characters = string.ascii_letters
    elif type == "Medium":
        characters = str(string.ascii_letters) + str(string.digits)
    elif type == "Hard":
        characters = string.printable
    characters = characters.replace("`", "")
    password = ""
    for i in range(count):
        password += random.choice(characters)
    text = STRINGS["pass"].format(type, password)
    await event.edit(text)