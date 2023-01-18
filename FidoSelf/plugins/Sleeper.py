from FidoSelf import client

SLEEPS = {
    "Say": "SAY_SLEEP",
    "Monshi": "MONSHI_SLEEP",
    "Enemy": "ENEMY_SLEEP",
    "AutoDelete": "AUTO_DELETE_SLEEP",
}
Pattern = ""
for SLEEP in SLEEPS:
    Pattern += SLEEP + "|"
Pattern = Pattern[:-1]

@client.Command(pattern=f"(?i)^\{client.cmd}Sleep ?({Pattern}) (\d*(\.)?\d*)$")
async def sleeper(event):
    await event.edit(client.get_string("Wait"))
    inlist = event.pattern_match.group(1).title()
    sleep = str(event.pattern_match.group(2))
    SLEEP = SLEEPS[inlist]
    client.DB.set_key(SLEEP, sleep)
    mode = client.get_string("Sleeper")[SLEEP]
    sleep = client.utils.convert_time(sleep) if sleep.isdigit() else sleep
    await event.edit(client.get_string("Sleeper_Main").format(mode, sleep))
