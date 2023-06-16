from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Private",
    "Plugname": "Anti Spam",
    "Pluginfo": {
        "Help": "To Setting Anti Spam For Pv!",
        "Commands": {
            "{CMD}AntiSpamPv <On-Off>": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "change": "**The Anti Spam Pv Mode Has Been {}!**",
}

@client.Command(command="AntiSpamPv (On|Off)")
async def antipvmode(event):
    await event.edit(client.STRINGS["wait"])
    change = event.pattern_match.group(1).lower()
    client.DB.set_key("ANTISPAM_PV", change)
    ShowChange = client.STRINGS["On"] if change == "on" else client.STRINGS["Off"]
    await event.edit(STRINGS["change"].format(ShowChange))

@client.Command(command="SetSpamPvLimit (\d*)")
async def setautodeletesleep(event):
    await event.edit(STRINGS["wait"])
    sleep = event.pattern_match.group(1)
    client.DB.set_key("SPAM_PV_LIMIT", sleep)
    await event.edit(client.get_string("AntiSpamPv_2").format(client.utils.convert_time(sleep)))

@client.Command(onlysudo=False, alowedits=False)
async def antispam(event):
    if not event.is_private or event.is_white or event.is_sudo or event.is_bot: return
    mode = client.DB.get_key("ANTISPAM_PV") or "off"
    warns = client.DB.get_key("ANTISPAM_WARNS") or {}
    if mode == "on":
        if not event.sender_id in warns:
            warns.update({event.sender_id: 0})
        last = warns[event.sender_id]
        uwarns = last + 1
        warns.update({event.sender_id: uwarns})
        client.DB.set_key("ANTISPAM_WARNS", warns)
        limit = client.DB.get_key("SPAM_PV_LIMIT") or 5
        WARNS = f"{uwarns}/{limit}"
        if uwarns >= limit:
            await event.respond(f"**• Warns:** ( `{WARNS}` )\n\n**• You Are Blocked!**")
        else:
            await event.respond(f"**• Warns:** ( `{WARNS}` )")
