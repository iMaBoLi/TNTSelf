from TNTSelf import client
from telethon import types
from instagrapi import Client as Insta
from datetime import datetime, timezone
import requests
import os

__INFO__ = {
    "Category": "Usage",
    "Name": "Instagram",
    "Info": {
        "Help": "To Manage And Download Instagram Medias!",
        "Commands": {
            "{CMD}INLogin <SesID>": {
                "Help": "To Login To Account",
                "Input": {
                    "<SesID>": "Session ID Of Account",
                },
            },
            "{CMD}INPost <Link>": {
                "Help": "To Download Posts",
                "Input": {
                    "<Link>": "Link Of Post",
                },
            },
        },
    },
}
client.functions.AddInfo(__INFO__)

STRINGS = {
    "invsessionid": "**{STR} The Instagram Session** ( `{}` ) **Is Invalid!**",
    "setsession": "**{STR} The Instagram Session** ( `{}` ) **Has Been Saved!**",
    "nosession": "**{STR} The Instagram Session Is Not Saved!**",
    "invsession": "**{STR} The Instagram Session Is Invalid!**",
    "invlink": "**{STR} The Instagram Link** ( `{}` ) **Is Invalid!**",
    "notpost": "**{STR} The Instagram Link** ( `{}` ) **Is Not For Posts!**",
    "downpost": "**{STR} Downloading Instagram Post ...**\n**{STR} Link:** ( `{}` )",
    "postcaption": "**{STR} Instagram Link: ( `{}` )**\n\n**{STR} Publisher: ( {} )**\n\n**{STR} Views:** ( `{}` )\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )\n**{STR} Publish Time:** ( `{}` )\n**{STR} Caption:** ( `{}` )",
    "notuser": "**{STR} The Instagram User** ( `{}` ) **Is Not Founded!**",
}

SESSION = client.PATH + "Instagram.json"
INSTA = None
if os.path.exists(SESSION):
    INSTA = Insta()
    INSTA.load_settings(SESSION)

@client.Command(command="INLogin (.*)")
async def instalogin(event):
    await event.edit(client.STRINGS["wait"])
    sessionid = event.pattern_match.group(1)
    try:
        instacl = Insta()
        instacl.login_by_sessionid(sessionid)
        instacl.dump_settings(SESSION)
        global INSTA
        INSTA = instacl
    except:
        return await event.edit(client.getstrings(STRINGS)["invsessionid"].format(sessionid))
    send = await event.reply(client.getstrings(STRINGS)["setsession"].format(sessionid), file=SESSION)
    info = await send.save()
    client.DB.set_key("INSTAGRAM_SESSION", info)
    await event.delete()
    
@client.Command(command="INPost (.*)")
async def instapostdl(event):
    await event.edit(client.STRINGS["wait"])
    link = str(event.pattern_match.group(1))
    if not INSTA:
        return await event.edit(client.getstrings(STRINGS)["nosession"])
    try:
        INSTA.get_timeline_feed()
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"])
    try:
        mediapk = INSTA.media_pk_from_url(event.text)
        mediainfo = INSTA.media_info(mediapk)
    except:
        return await event.edit(client.getstrings(STRINGS)["invlink"].format(link))
    if not mediainfo.media_type in [1,2,8]:
        return await event.edit(client.getstrings(STRINGS)["notpost"].format(link))
    await event.edit(client.getstrings(STRINGS)["downpost"].format(link))
    publisher = f"[{mediainfo.user.full_name}](https://www.instagram.com/{mediainfo.user.username})"
    seconds = datetime.now(timezone.utc) - mediainfo.taken_at
    seconds = seconds.total_seconds()
    pubtime = client.functions.convert_time(seconds) + " Ago"
    mcap = mediainfo.caption_text if len(mediainfo.caption_text) <= 3000 else (mediainfo.caption_text[:3000] + " ...")
    caption = client.getstrings(STRINGS)["postcaption"].format(link, publisher, mediainfo.view_count, mediainfo.like_count, mediainfo.comment_count, pubtime, mcap)
    if mediainfo.media_type in [1, 2]:
        if mediainfo.product_type in ["clips", "feed", "igtv"]:
            post = INSTA.video_download(mediapk, folder=client.PATH)
            attributes = [types.DocumentAttributeVideo(duration=mediainfo.video_duration, supports_streaming=True, w=mediainfo.image_versions2["candidates"][0]["width"], h=mediainfo.image_versions2["candidates"][0]["height"])]
            thumbnail = client.PATH + link + ".jpg"
            img_data = requests.get(mediainfo.image_versions2["candidates"][0]["url"]).content
            with open(thumbnail, "wb") as img:
                imh.write(img_data)
        else:
            post = INSTA.photo_download(mediapk, folder=client.PATH)
            attributes, thumbnail = None, None
        await client.send_file(event.chat_id, post, caption=caption, thumb=thumbnail, attributes=attributes)
        os.remove(post)
        if thumbnail:
            os.remove(thumbnail)
    elif mediainfo.media_type == 8:
        post = INSTA.album_download(mediapk, folder=client.PATH)
        callback = event.progress(upload=True)
        for lpost in client.functions.chunks(post, 9):
            await client.send_file(event.chat_id, lpost, caption=caption, progress_callback=callback)
        for rpost in post:
            os.remove(rpost)