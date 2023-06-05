SIGN_MODE
from FidoSelf import client

STRINGS = {
    "set": "**The Sign Text Was Set To** ( `{}` )",
}

@client.Command(command="SetSign ([\s\S]*)")
async def setsign(event):
    await event.edit(client.STRINGS["wait"])
    stext = event.pattern_match.group(1)
    client.DB.set_key("SIGN_TEXT", stext)
    text = STRINGS["set"].format(stext)
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