from FidoSelf import client
import instagrapi
import os

STRINGS = {
    "session": "**The Instagram Account Session File!**\n\n**Username:** ( `{}` )\n**Password:** ( `{}` )",
}

@client.Command(command="Cinsta (.*)\:(.*)\:?(.*)?")
async def createsession(event):
    await event.edit(client.STRINGS["wait"])
    username = event.pattern_match.group(1)
    password = event.pattern_match.group(2)
    verpass = event.pattern_match.group(3)
    insta = instagrapi.Client()
    if verpass:
        insta.login(username, password, verification_code=verpass)
    else:
        insta.login(username, password)
    sesfile = client.PATH + username + "-" + password + ".json"
    insta.dump_settings(sesfile)
    caption = STRINGS["session"].format(username, password)
    await client.respond(caption, file=sesfile)
    os.remove(sesfile)
    await event.delete()