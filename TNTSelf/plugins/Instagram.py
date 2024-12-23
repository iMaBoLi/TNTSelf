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
    "invsessionid": "**{STR} The Instagram Session ID** ( `{}` ) **Is Invalid!**",
    "setsession": "**{STR} The Instagram Session ID** ( `{}` ) **Has Been Saved!**",
    "nosession": "**{STR} The Instagram Session ID Is Not Saved!**",
    "invsession": "**{STR} The Instagram Session ID** ( `{}` ) **Is Invalid!**",
    "invlink": "**{STR} The Instagram Link** ( `{}` ) **Is Invalid!**",
    "notpost": "**{STR} The Instagram Link** ( `{}` ) **Is Not For A Post!**",
    "downpost": "**{STR} Downloading Instagram Post ...**\n**{STR} Link:** ( `{}` )",
    "postcaption": "**{STR} Instagram Link: ( `{}` )**\n\n**{STR} Publisher: ( {} )**\n\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )\n**{STR} Publish Time:** ( `{}` )",
    "notstory": "**{STR} The Instagram Link** ( `{}` ) **Is Not For A Story!**",
    "downstory": "**{STR} Downloading Instagram Story ...**\n**{STR} Link:** ( `{}` )",
    "storycaption": "**{STR} Instagram Link: ( `{}` )**\n\n**{STR} Publisher: ( {} )**\n\n**{STR} Pubilsh Time:** ( `{}` )",
    "notuser": "**{STR} The Instagram User** ( `{}` ) **Is Not Founded!**",
    "usercaption": "**{STR} Name: ( `{}` )**\n\n**{STR} Usernams: ( `{}` )**\n**{STR} ID:** ( `{}` )\n**{STR} Followers:** ( `{}` )\n**{STR} Followings:** ( `{}` )\n**{STR} Media Count:** ( `{}` )\n**{STR} Bio:** ( `{}` )",
}

@client.Command(command="INLogin (.*)")
async def instalogin(event):
    await event.edit(client.STRINGS["wait"])
    sessionid = event.pattern_match.group(1)
    try:
        INSTA = Insta()
        INSTA.login_by_sessionid(sessionid)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsessionid"].format(sessionid))
    event.client.DB.set_key("INSTAGRAM_SESSION", sessionid)
    await event.edit(client.getstrings(STRINGS)["setsession"].format(sessionid))
    
@client.Command(command="INPost (.*)")
async def instapostdl(event):
    await event.edit(client.STRINGS["wait"])
    event.client.loop.create_task(postdl(event))

async def postdl(event):
    link = str(event.pattern_match.group(1))
    sessionid = event.client.DB.get_key("INSTAGRAM_SESSION")
    if not sessionid:
        return await event.edit(client.getstrings(STRINGS)["nosession"])
    try:
        INSTA = Insta()
        INSTA.login_by_sessionid(sessionid)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(sessionid))
    try:
        mediapk = INSTA.media_pk_from_url(event.text)
        mediainfo = INSTA.media_info(mediapk)
    except:
        return await event.edit(client.getstrings(STRINGS)["invlink"].format(link))
    if not mediainfo.product_type in ["clips", "feed", "igtv", "carousel_container"]:
        return await event.edit(client.getstrings(STRINGS)["notpost"].format(link))
    await event.edit(client.getstrings(STRINGS)["downpost"].format(link))
    publisher = f"[{mediainfo.user.full_name}](https://www.instagram.com/{mediainfo.user.username})"
    seconds = datetime.now(timezone.utc) - mediainfo.taken_at
    seconds = seconds.total_seconds()
    pubtime = client.functions.convert_time(seconds) + " Ago"
    caption = client.getstrings(STRINGS)["postcaption"].format(link, publisher, mediainfo.like_count, mediainfo.comment_count, pubtime)
    if mediainfo.media_type in [1, 2]:
        if mediainfo.media_type == 2 and mediainfo.product_type in ["clips", "feed", "igtv"]:
            post = INSTA.video_download(mediapk, folder=event.client.PATH)
            attributes = [types.DocumentAttributeVideo(duration=mediainfo.video_duration, supports_streaming=True, w=mediainfo.image_versions2["candidates"][0]["width"], h=mediainfo.image_versions2["candidates"][0]["height"])]
            thumbnail = event.client.PATH + mediapk + ".jpg"
            img_data = requests.get(mediainfo.image_versions2["candidates"][0]["url"]).content
            with open(thumbnail, "wb") as img:
                img.write(img_data)
            callback = event.progress(upload=True)
        elif mediainfo.media_type == 1:
            post = INSTA.photo_download(mediapk, folder=event.client.PATH)
            attributes, thumbnail, callback = None, None
        await event.client.send_file(event.chat_id, post, caption=caption, thumb=thumbnail, attributes=attributes, progress_callback=callback)
        os.remove(post)
        if thumbnail: os.remove(thumbnail)
    elif mediainfo.media_type == 8:
        post = INSTA.album_download(mediapk, folder=event.client.PATH)
        for lpost in client.functions.chunks(post, 9):
            await event.client.send_file(event.chat_id, lpost, caption=caption)
        for rpost in post:
            os.remove(rpost)
    await event.delete()
            
@client.Command(command="INStory (.*)")
async def instastorydl(event):
    await event.edit(client.STRINGS["wait"])
    event.client.loop.create_task(storydl(event))

async def storydl(event):
    link = str(event.pattern_match.group(1))
    sessionid = event.client.DB.get_key("INSTAGRAM_SESSION")
    if not sessionid:
        return await event.edit(client.getstrings(STRINGS)["nosession"])
    try:
        INSTA = Insta()
        INSTA.login_by_sessionid(sessionid)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(sessionid))
    try:
        mediapk = INSTA.story_pk_from_url(event.text)
        mediainfo = INSTA.media_info(mediapk)
    except:
        return await event.edit(client.getstrings(STRINGS)["invlink"].format(link))
    if not mediainfo.product_type == "story":
        return await event.edit(client.getstrings(STRINGS)["notstory"].format(link))
    await event.edit(client.getstrings(STRINGS)["downstory"].format(link))
    publisher = f"[{mediainfo.user.full_name}](https://www.instagram.com/{mediainfo.user.username})"
    seconds = datetime.now(timezone.utc) - mediainfo.taken_at
    seconds = seconds.total_seconds()
    pubtime = client.functions.convert_time(seconds) + " Ago"
    caption = client.getstrings(STRINGS)["storycaption"].format(link, publisher, pubtime)
    story = INSTA.story_download(mediapk , folder=event.client.PATH)
    if mediainfo.media_type == 2:
        attributes = [types.DocumentAttributeVideo(duration=mediainfo.video_duration, supports_streaming=True, w=mediainfo.image_versions2["candidates"][0]["width"], h=mediainfo.image_versions2["candidates"][0]["height"])]
        thumbnail = event.client.PATH + mediapk + ".jpg"
        img_data = requests.get(mediainfo.image_versions2["candidates"][0]["url"]).content
        with open(thumbnail, "wb") as img:
            img.write(img_data)
    elif mediainfo.media_type == 1:
        attributes, thumbnail = None, None
    await event.client.send_file(event.chat_id, story, caption=caption, thumb=thumbnail, attributes=attributes)
    os.remove(story)
    if thumbnail:
        os.remove(thumbnail)
    await event.delete()
    
@client.Command(command="INUser (.*)")
async def instauserinfo(event):
    await event.edit(client.STRINGS["wait"])
    username = str(event.pattern_match.group(1))
    sessionid = event.client.DB.get_key("INSTAGRAM_SESSION")
    if not sessionid:
        return await event.edit(client.getstrings(STRINGS)["nosession"])
    try:
        INSTA = Insta()
        INSTA.login_by_sessionid(sessionid)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(sessionid))
    try:
        info = INSTA.user_info_by_username(username)
    except:
        return await event.edit(client.getstrings(STRINGS)["notuser"].format(username))
    photo = event.client.PATH + info.full_name + ".jpg"
    img_data = requests.get(info.profile_pic_url_hd).content
    with open(photo, 'wb') as img:
        img.write(img_data)
    caption = client.getstrings(STRINGS)["usercaption"].format(info.full_name, info.username, info.pk, info.follower_count, info.following_count, info.media_count, info.biography)
    await event.client.send_file(event.chat_id, photo, caption=caption)
    os.remove(photo)
    await event.delete()