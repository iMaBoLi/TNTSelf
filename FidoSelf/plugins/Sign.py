from FidoSelf import client

__INFO__ = {
    "Category": "Funs",
    "Plugname": "Sign",
    "Pluginfo": {
        "Help": "To Sign A Text On Your Messages!",
        "Commands": {
            "{CMD}Sign <On-Off>": None,
            "{CMD}SetSign <Text>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Sign Mode Has Been {}!**",
    "setsign": "**The Sign Text Was Set To** ( `{}` )",
}

@client.Command(command="Sign (On|Off)")
async def signmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("SIGN_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="SetSign ([\s\S]*)")
async def setsign(event):
    await event.edit(client.STRINGS["wait"])
    stext = event.pattern_match.group(1)
    client.DB.set_key("SIGN_TEXT", stext)
    text = STRINGS["setsign"].format(stext)
    await event.edit(text)

@client.Command(allowedits=False)
async def sign(event):
    if event.checkCmd(): return
    mode = client.DB.get_key("SIGN_MODE") or "OFF"
    if mode == "ON":
        stext = client.DB.get_key("SIGN_TEXT") or "- Signed By Me!"
        if event.text:
            ntext = event.text + "\n\n" + stext
        else:
            ntext = stext
        await event.edit(ntext)