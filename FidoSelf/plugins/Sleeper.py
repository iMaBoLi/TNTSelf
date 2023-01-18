from FidoSelf import client

SLEEPS = {
    "Say": "SAY_SLEEP",
    "Monshi": "MONSHI_SLEEP",
    "AutoDelete": "AUTO_DELETE_SLEEP",
}
Pattern = ""
for SLEEP in SLEEPS:
    Pattern += SLEEP + "|"
Pattern = Pattern[:-1]

@client.Cmd(pattern=f"(?i)^\{client.cmd}Sleep ?({Pattern}) (\d*(\.)?\d*)$")
async def sleeper(event):
    await event.edit(client.get_string("Wait"))
    inlist = event.pattern_match.group(1).title()
    sleep = event.pattern_match.group(2)
    SLEEP = SLEEPS[inlist]
    client.DB.set_key(SLEEP, sleep)
    mode = client.get_string("Sleeper")[SLEEP]
    csleep = client.utils.convert_time(sleep)
    sleep = csleep if csleep != "0s" else sleep
    await event.edit(client.get_string("Sleeper_Main").format(mode, sleep))
