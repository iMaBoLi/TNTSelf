from FidoSelf import client

__INFO__ = {
    "Category": "Pv",
    "Name": "MutePv",
    "Info": {
        "Help": "To Mute Users In Pv!",
        "Commands": {
            "{CMD}MutePv <On-Off>": {
                "Help": "To Turn On-Off Mute Pv",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**{STR} The Mute Pv Mode Has Been {}!**"
}
@client.Command(command="MutePv (On|Off)")
async def mutepvmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).upper()
    client.DB.set_key("MUTEPV_MODE", change)
    showchange = client.STRINGS["On"] if change == "ON" else client.STRINGS["Off"]
    await event.edit(client.getstrings(STRINGS)["change"].format(showchange))

@client.Command(onlysudo=False, allowedits=False)
async def mutepv(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("MUTEPV_MODE") or "OFF"
    if mode == "ON":
        await event.delete()