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
    client.LOGS.error(222)
    if not event.is_private:
        return client.LOGS.error(222)
    if event.is_white:
        return client.LOGS.error(222)
    if event.is_sudo:
        return client.LOGS.error(222)
    if event.is_bot:
        return client.LOGS.error(222)
    client.LOGS.error(1)
    mutemode = client.DB.get_key("MUTEPV_MODE") or "OFF"
    client.LOGS.error(2)
    if mutemode == "ON":
        client.LOGS.error(3)
        if event.checkSpam(maxmsg=6, block=True): return
        client.LOGS.error(4)
        await event.delete()