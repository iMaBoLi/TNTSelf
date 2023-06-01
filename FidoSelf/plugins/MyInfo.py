from FidoSelf import client
from telethon import functions

STRINGS = {
    "info": "**{STR} Your Profile Info:**\n\n   **ID:** ( `{}` )\n   **Name:** ( `{}` )\n   **UserName:** ( `{}` )\n   **Biography:** ( `{}` )",
    "id": "**{STR} Your ID:** ( `{RES}` )",
    "name": "**{STR} Your Name:** ( `{RES}` )",
    "username": "**{STR} Your UserName:** ( `{RES}` )",
    "bio": "**{STR} Your Biography:** ( `{RES}` )",
    "phone": "**{STR} Your Phone:** ( `{RES}` )",
    "profile": "**{STR} Your Profile Picture!**",
}

@client.Command(command="My(iNfo|iD|Name|Bio|Username|Phone|Profile)")
async def myinfo(event):
    type = event.pattern_match.group(1).lower()
    info = await client.get_me()
    uinfo = (await client(functions.users.GetFullUserRequest("me"))).full_user
    mypic = await client.get_profile_photos("me")
    name = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name
    username = f"@{info.username}" if info.username else "---"
    if type == "info":
        text = STRINGS[type]
        text = text.format(info.id, name, username, uinfo.about)
        await event.respond(text, file=mypic[0])
        await event.delete()
    infos = {
        "id": info.id,
        "name": name,
        "phone": "+" + info.phone,
        "profile": mypic[0],
        "username": username,
        "bio": uinfo.about,
    }
    result = infos[type]
    text = STRINGS[type]
    if type == "profile":
        await event.respond(text, file=result)
        await event.delete()
    else:
        text = text.format(RES=result)
        await event.edit(text)
