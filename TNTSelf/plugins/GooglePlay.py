from TNTSelf import client
from google_play_scraper import app, exceptions, search
import requests
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Google Play",
    "Info": {
        "Help": "To Get Information Of Google Play Apps!",
        "Commands": {
            "{CMD}GPInfo <App-ID>": {
                "Help": "To Get App Info",
                "Input": {
                    "<App-Name>": "ID Of App",
                },
            },
            "{CMD}GPSearch <App-Name>": {
                "Help": "To Search For App",
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
        "appinfo": "**{STR} App Name:** ( `{}` - `{}` )\n\n**{STR} Genre:** ( `{}` )\n**{STR} Score:** ( `{}` )\n**{STR} Downloads:** ( `{}` )\n**{STR} Rating:** ( `{}` )\n**{STR} Reviews:** ( `{}` )\n**{STR} Free:** ( `{}` )\n**{STR} Developer:** ( `{}` )\n\n**{STR} Description:** ( `{}` )\n\n\n**{STR} More Photos:**",
        "notsearch": "**{STR} The Google Play App With Name** ( `{}` ) **Is Not Founded!**",
        "appsearch": "**{STR} Google Play Apps With Name:** ( `{}` )\n\n",
    },
    "FA": {
        "notapp": "**{STR} هیچ اپلیکیشنی با آیدی** ( `{}` ) **پیدا نشد!**",
        "appinfo": "**{STR} اسم اپلیکیشن:** ( `{}` - `{}` )\n\n**{STR} موضوع:** ( `{}` )\n**{STR} امتیاز:** ( `{}` )\n**{STR} تعداد دانلود:** ( `{}` )\n**{STR} رتبه:** ( `{}` )\n**{STR} بازدیدها:** ( `{}` )\n**{STR} رایگان:** ( `{}` )\n**{STR} سازنده:** ( `{}` )\n\n**{STR} توضیحات:** ( `{}` )\n\n\n**{STR} عکس های بیشتر:**",
        "notsearch": "**{STR} هیچ اپلیکیشنی با نام** ( `{}` ) **پیدا نشد!**",
        "appsearch": "**{STR} اپلیکیشن های گوگل پلی با نام:** ( `{}` )\n\n",
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
    free = "✅" if result["free"] else "❌ - " + str(result["price"]) 
    description = result["description"][:1000] + "...."
    caption = client.getstring(STRINGS, "appinfo").format(result["title"], result["appId"], result["genre"], (str(round(result["score"], 1)) + " ★"), result["installs"], result["ratings"], result["reviews"], free, result["developer"], description)
    icon = client.PATH + appID + ".jpg"
    with open(icon, "wb") as f:
        f.write(requests.get(result["icon"]).content)
    info = await client.send_file(event.chat_id, icon, caption=caption)
    shots = []
    for i, shot in enumerate(result["screenshots"]):
        shname = client.PATH + appID + str(i) + ".jpg"
        with open(shname, "wb") as f:
            f.write(requests.get(shot).content)
        shots.append(shname)
    await info.reply(file=shots)
    await event.delete()
    os.remove(icon)
    for shot in shots:
        os.remove(shot)
        
@client.Command(command="GPSearch (.*)")
async def googlepsearch(event):
    await event.edit(client.STRINGS["wait"])
    appname = event.pattern_match.group(1)
    try:
        result = search(appname, n_hits=20)
    except TypeError:
        return await event.edit(client.getstring(STRINGS, "notsearch").format(appname))
    sres = client.getstring(STRINGS, "appsearch").format(appname)
    count = 1
    for app in result:
        title = app["title"]
        appid = app["appId"]
        sres += f"**{count} -** `{title}` ( `{appid}` )\n"
        count += 1
    await event.edit(sres)