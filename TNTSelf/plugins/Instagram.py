from TNTSelf import client
from instagrapi import Client as Insta
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
    "invsession": "**{STR} The Instagram Session ID** ( `{}` ) **Is Invalid!**",
    "setsession": "**{STR} The Instagram Session ID** ( `{}` ) **Has Been Saved!**",
    "nosession": "**{STR} The Instagram Session ID Is Not Saved!**",
    "invlink": "**{STR} The Instagram Link** ( `{}` ) **Is Invalid!**",
    "notpost": "**{STR} The Instagram Link** ( `{}` ) **Is Not For Posts!**",
    "downpost": "**{STR} Downloading Instagram Post ...**\n**{STR} Link:** ( `{}` )",
    "postcaption": "**{STR} Instagram Link: ( `{}` )**\n\n**{STR} Likes:** ( `{}` )\n**{STR} Comments:** ( `{}` )",
}

@client.Command(command="INLogin (.*)")
async def instalogin(event):
    await event.edit(client.STRINGS["wait"])
    sessionid = event.pattern_match.group(1)
    try:
        cl = Insta()
        cl.login_by_sessionid(sessionid)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(sessionid))
    client.DB.set_key("INSTAGRAM_SESSION", sessionid)
    await event.edit(client.getstrings(STRINGS)["setsession"].format(sessionid))
    
@client.Command(command="INPost (.*)")
async def instapostdl(event):
    await event.edit(client.STRINGS["wait"])
    link = str(event.pattern_match.group(1))
    sessionid = client.DB.get_key("INSTAGRAM_SESSION")
    if not sessionid:
        return await event.edit(client.getstrings(STRINGS)["nosession"])
    try:
        insta = Insta()
        insta.login_by_sessionid(sessionid)
    except:
        return await event.edit(client.getstrings(STRINGS)["invsession"].format(sessionid))
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
    caption = client.getstrings(STRINGS)["postcaption"].format(link, mediainfo.like_count, mediainfo.comment_count)
    callback = event.progress(upload=True)
    await client.send_file(event.chat_id, post, caption=caption, progress_callback=callback)
    os.remove(file)
    await edit.delete()