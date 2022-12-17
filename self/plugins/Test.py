from self import client
import os

@client.Cmd(pattern=f"(?i)^\{client.cmd}log (m|c|i)$")
async def logs(event):
    await event.edit(f"**{client.str} Processing . . .**")
    type = str(event.pattern_match.group(1))
    if type == "m" and os.path.exists("CmdError.txt"):
        await event.respond(f"**{client.str} Log File!**", file="CmdError.txt")
        await event.delete()
    elif type == "c" and os.path.exists("CallbackError.txt"):
        await event.respond(f"**{client.str} Log File!**", file="CallbackError.txt")
        await event.delete()
    elif type == "i" and os.path.exists("InlineError.txt"):
        await event.respond(f"**{client.str} Log File!**", file="InlineError.txt")
        await event.delete()
    else:
        await event.edit(f"**{client.str} The Log File Is Not Available!**")
