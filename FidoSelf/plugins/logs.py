from FidoSelf import client
import os


@client.Command(
    commands={
        "EN": "Logs \-(c|g)",
        "FA": "ارور \-(c|g)",
     }
)
async def logs(event):
    type = str(event.pattern_match.group(1))
    if type == "c" and os.path.exists("Fidog.log"):
        await event.respond(f"**{client.str} The Console Logs File!**", file="Fido.log")
        await event.delete()
    elif type == "g":
        git = await client.utils.runcmd('git log --pretty=format:"[%an]: %s"')
        open("Github.log", "w").write(str(git[0]))
        await event.respond(f"**{client.str} The Github Commits Logs File!**", file="Github.log")
        os.remove("Github.log")
        await event.delete()
    else:
        await event.edit(f"**{client.str} The Log File Is Not Available!**")
