from FidoSelf import client
from telethon import functions

STRINGS = {
    "EN": {
        "info": "**{STR} Your Profile Info:**\n\n   **ID:** ( `{}` )\n   **Name:** ( `{}` )\n   **UserName:** ( `{}` )\n   **Biography:** ( `{}` )",
        "id": "**{STR} Your ID:** ( `{RES}` )",
        "name": "**{STR} Your Name:** ( `{RES}` )",
        "phone": "**{STR} Your Phone:** ( `{RES}` )",
        "profile": "**{STR} Your Profile Picture!**",
    },
    "FA": {
        "اطلاعات": "**{STR} اطلاعات شما:**\n\n   **آیدی:** ( `{}` )\n   **اسم:** ( `{}` )\n   **نام کاربری:** ( `{}` )\n   **بیوگرافی:** ( `{}` )",
        "آیدی": "**{STR} آیدی شما:** ( `{RES}` )",
        "اسم": "**{STR} اسم شما:** ( `{RES}` )",
        "شماره": "**{STR} شماره شما:** ( `{RES}` )",
        "پروفایل": "**{STR} عکس پروفایل شما!**",
    },
}

@client.Command(
    commands={
        "EN": "My(iNfo|iD|Name|Phone|Profile)",
        "FA": "(اطلاعات|آیدی|اسم|شماره|پروفایل) من",
     }
)
async def myinfo(event):
    type = event.pattern_match.group(1)
    info = await client.get_me()
    mypic = await client.get_profile_photos("me")
    name = f"{info.first_name} {info.last_name}" if info.last_name else info.first_name,
    if type.upper() in ["INFO", "اطلاعات"]:
        text = client.get_string(type.lower(), STRINGS)
        uinfo = (await client(functions.users.GetFullUserRequest("me"))).full_user
        text = text.format(info.id, name, info.username, uinfo.about)
        await event.respond(text, file=mypic[0])
        await event.delete()
    infos = {
        "EN": {
            "ID": info.id,
            "NAME": name,
            "PHONE": "+" + info.phone,
            "PROFILE": mypic[0],
        },
        "FA": {
            "آیدی": info.id,
            "اسم": name,
            "شماره": "+" + info.phone,
            "پروفایل": mypic[0],
        },
    }
    result = infos[client.LANG][type.upper()]
    text = client.get_string(type.lower(), STRINGS)
    if type.upper() in ["PROFILE", "پروفایل"]:
        await event.respond(text, file=result)
        await event.delete()
    else:
        text = text.format(RES=result)
        await event.edit(text)
