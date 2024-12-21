from TNTSelf import client
from instagrapi import Client as Insta
from datetime import datetime, timezone
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
    "invsession": "**{STR} The Instagram Session** ( `{}` ) **Is Invalid!**",
    "setsession": "**{STR} The Instagram Session** ( `{}` ) **Has Been Saved!**",
    "nosession": "**{STR} The Instagram Session Is Not Saved!**",
    "invlink": "**{STR} The Instagram Link** ( `{}` ) **Is Invalid!**",
    "notpost": "**{STR} The Instagram Link** ( `{}` ) **Is Not For Posts!**",
    "downpost": "**{STR} Downloading Instagram Post ...**\n**{STR} Link:** ( `{}` )",
    "postcaption": "**{STR} Instagram Link: ( `{}` )**\n\n**{STR} Publisher: ( {} )**\n\n**{STR} Views:** ( `{}` )\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )\n**{STR} Publish Time:** ( `{}` )\n**{STR} Caption:** ( `{}` )",
}

@client.Command(command="INLogin (.*)")
async def instalogin(event):
    await event.edit(client.STRINGS["wait"])
    sessionid = event.pattern_match.group(1)
    session = client.PATH + "Instagram.json"
    try:
        cl = Insta()
        cl.login_by_sessionid(sessionid)
        cl.dump_settings(session)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(sessionid))
    send = await event.reply(client.getstrings(STRINGS)["setsession"].format(sessionid), file=session)
    info = await send.save()
    client.DB.set_key("INSTAGRAM_SESSION", info)
    await event.delete()
    
@client.Command(command="INPost (.*)")
async def instapostdl(event):
    await event.edit(client.STRINGS["wait"])
    link = str(event.pattern_match.group(1))
    session = client.PATH + "Instagram.json"
    if not os.path.exists(session):
        return await event.edit(client.getstrings(STRINGS)["nosession"])
    try:
        insta = Insta()
        insta.load_settings(session)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(session))
    try:
        mediapk = insta.media_pk_from_url(event.text)
        mediainfo = insta.media_info(mediapk)
    except:
        return await event.edit(client.getstrings(STRINGS)["invlink"].format(link))
    if not mediainfo.media_type in [1,2,8]:
        return await event.edit(client.getstrings(STRINGS)["notpost"].format(link))
    await event.edit(client.getstrings(STRINGS)["downpost"].format(link))
    if mediainfo.media_type == 1:
        post = insta.photo_download(mediapk, folder=client.PATH)
    elif mediainfo.media_type == 2 and mediainfo.product_type == "feed":
        post = insta.video_download(mediapk, folder)
    elif mediainfo.media_type == 2 and mediainfo.product_type == "igtv":
        post = insta.igtv_download(mediapk, folder=client.PATH)
    elif mediainfo.media_type == 2 and mediainfo.product_type == "clips":
        post = insta.clip_download(mediapk, folder=client.PATH)
    elif mediainfo.media_type == 8:
        post = insta.album_download(mediapk, folder=client.PATH)
    publisher = f"[{mediainfo.user.full_name}](https://www.instagram.com/{mediainfo.user.username})"
    seconds = datetime.now(timezone.utc) - mediainfo.taken_at
    seconds = seconds.total_seconds()
    pubtime = client.functions.convert_time(seconds) + " Ago"
    mcap = mediainfo.caption_text if len(mediainfo.caption_text) <= 3000 else (mediainfo.caption_text[:3000] + " ...")
    caption = client.getstrings(STRINGS)["postcaption"].format(link, publisher, mediainfo.view_count, mediainfo.like_count, mediainfo.comment_count, pubtime, mcap)
    callback = event.progress(upload=True)
    if type(post) == list:
        for lpost in client.functions.chunks(post, 9):
            await client.send_file(event.chat_id, lpost, caption=caption, progress_callback=callback)
        for rpost in post:
            os.remove(rpost)
    else:
        await client.send_file(event.chat_id, post, caption=caption, progress_callback=callback)
        os.remove(post)
    await event.delete()