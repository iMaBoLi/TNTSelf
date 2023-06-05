from FidoSelf import client

STRINGS = {
    "set": "**The Sign Text Was Set To** ( `{}` )",
    "sete": "**The Enemy Sign Text Was Set To** ( `{}` )",
}

@client.Command(command="Set(Sign|EnemySign) ([\s\S]*)")
async def setsign(event):
    await event.edit(client.STRINGS["wait"])
    type = event.pattern_match.group(1).lower()
    stext = event.pattern_match.group(2)
    if type == "sign":
        client.DB.set_key("SIGN_TEXT", stext)
        text = STRINGS["set"].format(stext)
    else:
        client.DB.set_key("SIGNENEMY_TEXT", stext)
        text = STRINGS["sete"].format(stext)
    await event.edit(text)

@client.Command(alowedits=False)
async def sign(event):
    if event.checkCmd(): return
    mode = client.DB.get_key("SIGN_MODE") or "off"
    if mode == "on":
        stext = client.DB.get_key("SIGN_TEXT") or "- Signed By Me!"
        if event.text:
            ntext = event.text + "\n\n" + stext
        else:
            ntext = stext
        await event.edit(ntext)