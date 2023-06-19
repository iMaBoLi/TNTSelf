from FidoSelf import client

__INFO__ = {
    "Category": "Private",
    "Plugname": "MutePv",
    "Pluginfo": {
        "Help": "To Mute Users In Pv!",
        "Commands": {
            "{CMD}MutePv <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Mute Pv Mode Has Been {}!**",
}
@client.Command(command="MutePv (On|Off)")
async def mutepvmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("MUTE_PV", change)
    ShowChange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(onlysudo=False, alowedits=False)
async def mutepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("MUTE_PV") or "OFF"
    if mode == "ON":
        await event.delete()