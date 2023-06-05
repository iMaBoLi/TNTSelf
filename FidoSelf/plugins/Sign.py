SIGN_MODE
from FidoSelf import client

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