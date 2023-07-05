from FidoSelf import client
import os

__INFO__ = {
    "Category": "Usage",
    "Plugname": "Screen Shot",
    "Pluginfo": {
        "Help": "To Take Screen Shot From Sites!",
        "Commands": {
            "{CMD}SShot <URL>": {
                "Help": "To Get Screen Shot",
                "Input": {
                    "<URL>": "Url Of Site",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "invlink": "**The Site Link** ( `{}` ) **Is Invalid!**",
    "taked": "**The Screen Shot From Site** ( `{}` ) **Has Been Taked!**",
}

@client.Command(command="SShot (.*)")
async def screenshot(event):
    await event.edit(client.STRINGS["wait"])
    sitelink = event.pattern_match.group(1)
    token = "SY1196W-HN84TCJ-G8J41WK-4B17FNK"
    url = f"https://shot.screenshotapi.net/screenshot?token={token}&url={sitelink}&full_page=true"
    result = await client.functions.request(url, json=True)
    if "error" in result:
        return await event.edit(STRINGS["invlink"].format(sitelink))
    content = await client.functions.request(result["screenshot"], content=True)
    screenshot = client.PATH + f"Screen-{sitelink}.png"
    open(screenshot, "wb").write(content)
    caption = STRINGS["taked"].format(sitelink)
    await client.send_file(event.chat_id, screenshot, caption=caption, force_document=True)
    os.remove(screenshot)
    await event.delete()