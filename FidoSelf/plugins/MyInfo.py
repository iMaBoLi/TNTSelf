from FidoSelf import client
from telethon import functions

__INFO__ = {
    "Category": "Account",
    "Plugname": "My Info",
    "Pluginfo": {
        "Help": "To Get Account Information!",
        "Commands": {
            "{CMD}MyInfo": None,
            "{CMD}MyId": None,
            "{CMD}MyName": None,
            "{CMD}MyBio": None,
            "{CMD}MyUsername": None,
            "{CMD}MyPhone": None,
            "{CMD}MyProfile": None,
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "info": "**Your Profile Info:**\n\n   **ID:** ( `{}` )\n   **Name:** ( `{}` )\n   **UserName:** ( `{}` )\n   **Biography:** ( `{}` )",
    "id": "**Your ID:** ( `{RES}` )",
    "name": "**Your Name:** ( `{RES}` )",
    "username": "**Your UserName:** ( `{RES}` )",
    "bio": "**Your Biography:** ( `{RES}` )",
    "phone": "**Your Phone:** ( `{RES}` )",
    "notprof": "**You Profile Photos iS Empty!**",
    "profile": "**Your Profile Picture!**",
}

@client.Command(command="My(iNfo|iD|Name|Bio|Username|Phone|Profile)")
async def myinfo(event):
    type = event.pattern_match.group(1).lower()
    info = await client.get_me()
    uinfo = (await client(functions.users.GetFullUserRequest("me"))).full_user
    mypic = await client.get_profile_photos("me")
    name = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    username = f"@{info.username}" if info.username else "---"
    prof = mypic[0] if mypic else None
    if type == "info":
        text = STRINGS[type]
        text = text.format(info.id, name, username, uinfo.about)
        await event.respond(text, file=prof)
        await event.delete()
    infos = {
        "id": info.id,
        "name": name,
        "phone": "+" + info.phone,
        "profile": prof,
        "username": username,
        "bio": uinfo.about,
    }
    text = STRINGS[type]
    if type == "profile":
        if not prof:
            await event.edit(STRINGS["notprof"])
        await event.respond(text, file=prof)
        await event.delete()
    else:
        result = infos[type]
        text = text.format(RES=result)
        await event.edit(text)
