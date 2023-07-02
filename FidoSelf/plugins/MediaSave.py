from FidoSelf import client
import os

__INFO__ = {
    "Category": "Private",
    "Plugname": "Media Save",
    "Pluginfo": {
        "Help": "To Save Sended Medias In Pv!",
        "Commands": {
            "{CMD}MSave <On-Off>": {
                "Help", "To Turn On-Off Media Save",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Save Media Has Been {}!**",
    "caption": "**The Media Was Saved!**\n\n**User:** ( {} )",
}

@client.Command(command="MSave (On|Off)")
async def msave(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("MEDIAPV_MODE", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(onlysudo=False)
async def savemedias(event):
    if not event.is_private or event.is_bot: return
    if event.checkReply(["Media"]): return
    mmode = client.DB.get_key("MEDIAPV_MODE")
    if mmode == "ON":
        if event.file.size > client.MAX_SIZE: return
        file = await event.download_media(client.PATH)
        sender = await event.get_sender()
        mention = client.functions.mention(sender)
        caption = STRINGS["caption"].format(mention)
        await client.send_file(client.REALM, file, caption=caption)
        os.remove(file)