from TNTSelf import client

__INFO__ = {
    "Category": "Funs",
    "Name": "Sign",
    "Info": {
        "Help": "To Sign A Text On Your Messages!",
        "Commands": {
            "{CMD}Sign <On-Off>": {
                "Help": "To Turn On-Off Sign Mode",
            },
            "{CMD}SetSign <Text>": {
                "Help": "To Set Sign Text",
                "Input": {
                    "<Text>": "Sign Text",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Sign Mode Has Been {}!**",
    "setsign": "**{STR} The Sign Text Was Set To** ( `{}` )"
}

@client.Command(command="Sign (On|Off)")
async def signmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    event.client.DB.set_key("SIGN_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(command="SetSign ([\\s\\S]*)")
async def setsign(event):
    await event.edit(client.STRINGS["wait"])
    stext = event.pattern_match.group(1)
    event.client.DB.set_key("SIGN_TEXT", stext)
    text = client.getstrings(STRINGS)["setsign"].format(stext)
    await event.edit(text)

@client.Command(allowedits=False, checkCmd=True)
async def autosign(event):
    smode = event.client.DB.get_key("SIGN_MODE") or "OFF"
    signtext = event.client.DB.get_key("SIGN_TEXT")
    if smode == "ON" and signtext:
        newtext = signtext if not event.text else event.text + "\n\n" + signtext
        await event.edit(newtext)