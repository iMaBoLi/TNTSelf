from FidoSelf import client
import instagrapi
import os, re

def INSTA():
    username = client.DB.get_key("INSTA_LOGIN_USER")
    password = client.DB.get_key("INSTA_LOGIN_PASS")
    session = client.DB.get_key("INSTA_LOGIN_SESSION")
    if not username or not password: return "empty"
    INSTA = instagrapi.Client()
    if os.path.exists("iNstaSession.json"):
        INSTA.load_settings("iNstaSession.json")
        INSTA.login(username, password)
        try:
            INSTA.get_timeline_feed()
        except instagrapi.exceptions.LoginRequired:
            INSTA.relogin()
            try:
                INSTA.login(username, password)
            except Exception as error:
                return f"Error: {error}"
    elif session:
        open("iNstaSession.json", "w").write(session)
        INSTA.load_settings("iNstaSession.json")
        INSTA.login(username, password)
        try:
            INSTA.get_timeline_feed()
        except instagrapi.exceptions.LoginRequired:
            INSTA.relogin()
            try:
                INSTA.login(username, password)
            except Exception as error:
                return f"Error: {error}"
    else:
        try:
            INSTA.login(username, password)
        except Exception as error:
            return f"Error: {error}"
        INSTA.dump_settings("iNstaSession.json")
        data = open("iNstaSession.json", "r").read()
        client.DB.set_key("INSTA_LOGIN_SESSION", data)
    return INSTA

@client.Cmd(pattern=f"(?i)^{client.cmd}instalogin (.*)\:(.*)$")
async def logininstagram(event):
    await event.edit(client.get_string("Wait").format(client.str))
    username = event.pattern_match.group(1)
    password = event.pattern_match.group(2)
    client.DB.set_key("INSTA_LOGIN_USER", username)
    client.DB.set_key("INSTA_LOGIN_PASS", password)
    login = INSTA()
    if login.startswith("Error:"):
        return await event.edit(f"**{client.str} The Login To Instagram Account Failed!**\n\n`{login}`")
    await event.edit(f"**{client.str} The Instagram Login With Username** ( `{username}` ) **And Password** ( `{password}` ) **Completed!**")

@client.Cmd(pattern=f"(?i)^{client.cmd}igpost (.*)$")
async def postdownload(event):
    await event.edit(client.get_string("Wait").format(client.str))
    link = event.pattern_match.group(1)
    if not re.search("(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/?(?:p|reel|tv)\/(.*)", link):
        return await event.edit(f"**{client.str} Your Entered Link For Not A Post Media!**")     
    insta = INSTA()
    if insta == "invalid" or insta == "empty":
        return await event.edit(f"**{client.str} Please Login With Your Instagram Account First!**\n\n• `{client.cmd}instalogin username:password`")
    folder = client.path + "insta/"
    mpk = insta.media_pk_from_url(link)
    media = insta.media_info(mpk)
    if media.media_type == 1:
        file = insta.photo_download(mpk, folder=folder)
    elif media.media_type == 2 and media.product_type == "feed":
        file = insta.video_download(mpk, folder=folder)
    elif media.media_type == 2 and media.product_type == "igtv":
        file = insta.igtv_download(mpk, folder=folder)
    elif media.media_type == 2 and media.product_type == "clips":
        file = insta.clip_download(mpk, folder=folder)
    elif media.media_type == 8:
        file = insta.album_download(mpk, folder=folder)
    else:
        return await event.edit(f"**{client.str} This Media Type Is Not Supported!**") 
    await event.reply(f"**{client.str} Like Count:** ( `{media.like_count}` )\n**{client.str} Comment Count:** ( `{media.comment_count}` )\n\n**{client.str} Caption:** ( `{media.caption_text}` )", file=file)
    await event.delete()
    if len(file) > 1:
        os.remove([f for f in file])
    else:
        os.remove(file)

@client.Cmd(pattern=f"(?i)^{client.cmd}iginfo (.*)$")
async def userinfo(event):
    await event.edit(client.get_string("Wait").format(client.str))
    username = event.pattern_match.group(1).replace("@", "")
    insta = INSTA()
    if insta == "invalid" or insta == "empty":
        return await event.edit(f"**{client.str} Please Login With Your Instagram Account First!**\n\n• `{client.cmd}instalogin username:password`")
    try:
        info = insta.user_info_by_username(username).dict()
    except instagrapi.exceptions.UserNotFound:
        return await event.edit(f"**{client.str} This Instagram Username Is Not Available!**")
    thumb = info['full_name'] + ".jpg"
    img = requests.get(info['profile_pic_url_hd']).content
    open(thumb , "wb").write(img)
    await event.reply(f"""
**{client.str} Name:** ( `{info['full_name']}` )
**{client.str} Username:** ( `{info['username']}` )
**{client.str} ID:** ( `{info['pk']}` )
**{client.str} Followers:** ( `{info['follower_count']}` )
**{client.str} Following:** ( `{info['following_count']}` )
**{client.str} Category Name:** ( `{info['category_name']}` )
**{client.str} Media Count:** ( `{info['media_count']}` )
**{client.str} Is Private:** ( `{"✅" if info['is_private'] else "❌"}` )
**{client.str} Is Verified:** ( `{"✅" if info['is_verified'] else "❌"}` )
**{client.str} Is Business Account:** ( `{"✅" if info['is_business'] else "❌"}` )
**{client.str} Business Category Name:** ( `{info['business_category_name'] or "---"}` )
**{client.str} Bio:** ( `{info['biography'] or "---"}` )
**{client.str} External Url:** ( `{info['external_url'] or "---"}` )
""")
    os.remove(thumb)
    await event.delete()
