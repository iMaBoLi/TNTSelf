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
async def autosign(event):
    if event.checkCmd(): return
    smode = client.DB.get_key("SIGN_MODE") or "OFF"
    signtext = client.DB.get_key("SIGN_TEXT")
    if smode == "ON" and signtext:
        newtext = signtext if not event.text else event.text + "\n\n" + signtext
        await event.edit(newtext)