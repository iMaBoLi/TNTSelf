from FidoSelf import client
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}log (m|c|i)$")
async def logs(event):
    await event.edit(f"**{client.str} Processing . . .**")
    type = str(event.pattern_match.group(1))
    if type == "m" and os.path.exists("CmdError.log"):
        await event.respond(f"**{client.str} Log File!**", file="CmdError.log")
        await event.delete()
    elif type == "c" and os.path.exists("CallbackError.log"):
        await event.respond(f"**{client.str} Log File!**", file="CallbackError.log")
        await event.delete()
    elif type == "i" and os.path.exists("InlineError.log"):
        await event.respond(f"**{client.str} Log File!**", file="InlineError.log")
        await event.delete()
    else:
        await event.edit(f"**{client.str} The Log File Is Not Available!**")
