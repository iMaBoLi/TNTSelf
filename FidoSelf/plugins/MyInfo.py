from FidoSelf import client

STRINGS = {
    "EN": {
        "id": "**{STR} Your ID:** ( `{RES}` )",
        "name": "**{STR} Your Name:** ( `{RES}` )",
        "phone": "**{STR} Your Phone:** ( `{RES}` )",
        "profile": "**{STR} Your Profile Picture!**",
    },
    "FA": {
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
    infos = {
        "EN": {
            "ID": info.id,
            "NAME": f"{info.first_name} {info.last_name}" if info.last_name else info.first_name,
            "PHONE": info.phone,
            "PROFILE": (await client.get_profile_photos("me"))[0],
        },
        "FA": {
            "آیدی": info.id,
            "اسم": f"{info.first_name} {info.last_name}" if info.last_name else info.first_name,
            "شماره": info.phone,
            "پروفایل": (await client.get_profile_photos("me"))[0],
        },
    }
    result = infos[client.LANG][type.upper()]
    text = client.get_string(type.lower(), STRINGS)
    if type.upper() == "PROFILE":
        await event.edit(text, file=result)
    else:
        text = text.format(RES=result)
        await event.edit(text)
