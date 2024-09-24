from FidoSelf import client
from google_play_scraper import app, exceptions
from telethon.tl.types import InputMediaWebPage

__INFO__ = {
    "Category": "Usage",
    "Name": "Google Play",
    "Info": {
        "Help": "To Get Information Of Google Play Apps!",
        "Commands": {
            "{CMD}GPInfo <App-Name>": {
                "Help": "To Get App Info",
                "Input": {
                    "<App-Name>": "Name Of App",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "EN": {
        "notapp": "**{STR} The Google Play App With ID** ( `{}` ) **Is Not Founded!**",
        "appinfo": "**{STR} App Name:** ( `{}` - `{}` )\n\n**{STR} Score:** ( `{}` )\n**{STR} Installs:** ( `{}` )\n**{STR} Rating:** ( `{}` )\n**{STR} Reviews:** ( `{}` )\n**{STR} Free:** ( `{}` )\n**{STR} Developer:** ( `{}` )\n\n**{STR} Description:** ( `{}` )",
    },
    "FA": {
        "notapp": "**{STR} هیچ اپلیکیشنی با آیدی** ( `{}` ) **پیدا نشد!**",
        "appinfo": "**{STR} اسم اپلیکیشن:** ( `{}` - `{}` )\n\n**{STR} امتیاز:** ( `{}` )\n**{STR} تعداد نصب:** ( `{}` )\n**{STR} رتبه:** ( `{}` )\n**{STR} بازدیدها:** ( `{}` )\n**{STR} رایگان:** ( `{}` )\n**{STR} سازنده:** ( `{}` )\n\n**{STR} توضیحات:** ( `{}` )",
    },
}

@client.Command(command="GPInfo (.*)")
async def googlepinfo(event):
    await event.edit(client.STRINGS["wait"])
    appID = event.pattern_match.group(1)
    try:
        result = app(appID)
    except exceptions.NotFoundError:
        return await event.edit(client.getstring(STRINGS, "notapp").format(appID))
    free = "✅" if result["free"] else "❌"
    description = result["description"][:1000] + "...."
    caption = client.getstring(STRINGS, "appinfo").format(result["title"], result["appId"], result["score"], result["installs"], result["ratings"], result["reviews"], free, result["developer"], description)
    icon = InputMediaWebPage(url=result["icon"])
    await event.respond(caption, file=icon)
    await event.delete()