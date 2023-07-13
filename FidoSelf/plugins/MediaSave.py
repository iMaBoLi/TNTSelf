from FidoSelf import client
import os

__INFO__ = {
    "Category": "Pv",
    "Name": "Media Save",
    "Info": {
        "Help": "To Save All Medias In Your Pv!",
        "Commands": {
            "{CMD}MSave <On-Off>": {
                "Help": "To Turn On-Off Media Save",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Save Media Has Been {}!**",
    "caption": "**{STR} The Media Was Saved!**\n\n**User:** ( {} )"
}

@client.Command(command="MSave (On|Off)")
async def msave(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("MEDIAPV_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(onlysudo=False)
async def savemedias(event):
    if not event.is_private or event.is_sudo or event.is_bot: return
    if not event.media: return
    mmode = client.DB.get_key("MEDIAPV_MODE") or "OFF"
    if mmode == "ON":
        sender = await event.get_sender()
        mention = client.functions.mention(sender)
        caption = client.getstrings(STRINGS)["caption"].format(mention)
        await client.send_file(client.REALM, event.media, caption=caption)