from FidoSelf import client
from instagrapi import Client
from instagrapi.exceptions import BadPassword, ChallengeError
import os

STRINGS = {
    "session": "**The Instagram Account Session File!**\n\n**Username:** ( `{}` )\n**Password:** ( `{}` )",
    "invpass": "**The Instagram Account Password In Incorrect!**\n\n**Username:** ( `{}` )\n**Password:** ( `{}` )",
    "banacc": "**The Instagram Account Is Blocked!**\n\n**Username:** ( `{}` )\n**Password:** ( `{}` )",
}

@client.Command(command="Cinsta (.*)\:(.*)\:?(.*)?")
async def createsession(event):
    await event.edit(client.STRINGS["wait"])
    username = event.pattern_match.group(1)
    password = event.pattern_match.group(2)
    verpass = event.pattern_match.group(3) or None
    insta = Client()
    try:
        insta.login(username, password, verification_code=verpass)
    except BadPassword:
        return await event.edit(STRINGS["invpass"].format(username, password)
    except ChallengeError:
        return await event.edit(STRINGS["banacc"].format(username, password)
    sesfile = client.PATH + username + "-" + password + ".json"
    insta.dump_settings(sesfile)
    caption = STRINGS["session"].format(username, password)
    await client.respond(caption, file=sesfile)
    os.remove(sesfile)
    await event.delete()