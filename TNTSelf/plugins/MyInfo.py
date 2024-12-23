from TNTSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Name": "My Info",
    "Info": {
        "Help": "To Get Account Information!",
        "Commands": {
            "{CMD}MyInfo": {
                "Help": "To Get Full Info Of Your Account",
            },
            "{CMD}MyId": {
                "Help": "To Get ID Of Your Account",
            },
            "{CMD}MyName": {
                "Help": "To Get Name Of Your Account",
            },
            "{CMD}MyBio": {
                "Help": "To Get Biography Of Your Account",
            },
            "{CMD}MyUsername": {
                "Help": "To Get Username Of Your Account",
            },
            "{CMD}MyPhone": {
                "Help": "To Get Phone Of Your Account",
            },
            "{CMD}MyProfile": {
                "Help": "To Get Profile Picture Of Your Account",
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
   "info": "**{STR} Your Profile Info:**\n\n   **{STR} ID:** ( `{}` )\n   **{STR} Name:** ( `{}` )\n   **{STR} UserName:** ( `{}` )\n   **{STR} Biography:** ( `{}` )",
    "id": "**{STR} Your ID:** ( `{}` )",
    "name": "**{STR} Your Name:** ( `{}` )",
    "username": "**{STR} Your UserName:** ( `{}` )",
    "bio": "**{STR} Your Biography:** ( `{}` )",
    "phone": "**{STR} Your Phone:** ( `{}` )",
    "notprof": "**{STR} You Profile Photos iS Empty!**",
    "profile": "**{STR} Your Profile Picture!**",
}

@client.Command(command="My(iNfo|iD|Name|Bio|Username|Phone|Profile)")
async def myinfo(event):
    type = event.pattern_match.group(1).lower()
    info = await event.client.get_me()
    uinfo = (await event.client(functions.users.GetFullUserRequest("me"))).full_user
    mypic = await event.client.get_profile_photos("me")
    name = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    username = f"@{info.username}" if info.username else "---"
    prof = mypic[0] if mypic else None
    if type == "info":
        text = client.getstrings(STRINGS)[type]
        text = text.format(info.id, name, username, uinfo.about)
        await event.respond(text, file=prof)
        return await event.delete()
    infos = {
        "id": info.id,
        "name": name,
        "phone": "+" + info.phone,
        "profile": prof,
        "username": username,
        "bio": uinfo.about,
    }
    text = client.getstrings(STRINGS)[type]
    if type == "profile":
        if not prof:
            await event.edit(client.getstrings(STRINGS)["notprof"])
        await event.respond(text, file=prof)
        await event.delete()
    else:
        result = infos[type]
        text = text.format(result)
        await event.edit(text)
