from FidoSelf import client
from telethon import functions

@client.Cmd(pattern=f"(?i)^\{client.cmd}AntiSpamPv (On|Off)$")
async def antispampv(event):
    await event.edit(client.get_string("Wait"))
    mode = event.pattern_match.group(1).lower()
    client.DB.set_key("ANTISPAM_PV", mode)
    change = client.get_string("Change_1") if mode == "on" else client.get_string("Change_2")
    await event.edit(client.get_string("AntiSpamPv_1").format(change))

@client.Cmd(pattern=f"(?i)^\{client.cmd}SetSpamPvLimit (\d*)$")
async def setautodeletesleep(event):
    await event.edit(client.get_string("Wait"))
    sleep = event.pattern_match.group(1)
    client.DB.set_key("SPAM_PV_LIMIT", sleep)
    await event.edit(client.get_string("AntiSpamPv_2").format(client.utils.convert_time(sleep)))

@client.Cmd(sudo=False, edits=False)
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
