from FidoSelf import client

STRINGS = {
    "EN": {
        "id": "**{STR} Your ID:** ( `{RES}` )",
        "name": "**{STR} Your Name:** ( `{RES}` )",
        "phone": "**{STR} Your Phone:** ( `{RES}` )",
    },
    "FA": {
        "آیدی": "^{STR} من همیشه آنلاین هستم!$",
        "اسم": "^{STR} ربات آنلاین است!$",
        "شماره": "^{STR} در حال بازنشانی ربات ...$",
    },
}

@client.Command(
    commands={
        "EN": "My (iD|Name|Phone)",
        "FA": "(آیدی|اسم|شماره) من",
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
        }
        "FA": {
            "آیدی": info.id,
            "اسم": f"{info.first_name} {info.last_name}" if info.last_name else info.first_name,
            "شماره": info.phone,
        }
    }
    result = infos[client.LANG][type.upper()]
    text = client.get_string(type.lower(), STRINGS)
    text = text.format(RES=result)
    await event.edit(text)
