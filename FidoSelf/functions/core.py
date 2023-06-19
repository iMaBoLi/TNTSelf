from FidoSelf import client
from telethon.types import Message
import re
import time
import os

def checkCmd(event, text=None):
    if not event.text and not text: return False
    text = text if text else event.text
    for command in client.COMMANDS:
        search = re.search(command, text)
        if search:
            return True
    return False

setattr(Message, "checkCmd", checkCmd)

SPAMS = {}

def checkSpam(event):
    bantime = 30
    maxtime = 4
    if event.sender_id not in SPAMS:
        SPAMS[event.sender_id] = {"next_time": int(time.time()) + maxtime, "messages": 0, "banned": 0}
        uspam = SPAMS[event.sender_id]
    else:
        uspam = SPAMS[event.sender_id]
        uspam["messages"] += 1
    if uspam["banned"] >= int(time.time()):
        return True
    else:
        if uspam["next_time"] >= int(time.time()):
            if uspam["messages"] >= 8:
                SPAMS[event.sender_id]["banned"] = int(time.time()) + bantime
                return True
        else:
            SPAMS[event.sender_id]["messages"] = 0
            SPAMS[event.sender_id]["next_time"] = int(time.time()) + maxtime
            return False

setattr(Message, "checkSpam", checkSpam)

def checkReply(event, medias):
    result = False
    message = None
    mediatype = client.functions.mediatype(event.reply_message)
    if not event.is_reply and mediatype not in medias:
        message = ""
        for media in medias:
            message += media + " Or "
        message = message[:-3]
        message = client.STRINGS["reply"].format(message)
        result = True
    return result, message

setattr(Message, "checkReply", checkReply)

async def DownloadFiles():
    os.mkdir("downloads")

    foshs = client.DB.get_key("FOSHS_FILE")
    if foshs:
        try:
            get = await client.get_messages(int(foshs["chat_id"]), ids=int(foshs["msg_id"]))
            await get.download_media(client.PATH + "FOSHS.txt")
        except:
            pass

    cover = client.DB.get_key("FILE_COVER")
    if cover:
        try:
            get = await client.get_messages(int(cover["chat_id"]), ids=int(cover["msg_id"]))
            await get.download_media(client.PATH + "Cover.png")
        except:
            pass

    photos = client.DB.get_key("PHOTOS")
    if photos:
        for photo in list(photos.keys()):
            try:
                get = await client.get_messages(int(photos[photo]["chat_id"]), ids=int(photos[photo]["msg_id"]))
                await get.download_media(client.PATH + photo)
            except:
                pass
            
    fonts = client.DB.get_key("FONTS")
    if fonts:
        for font in fonts:
            try:
                get = await client.get_messages(int(fonts[font]["chat_id"]), ids=int(fonts[font]["msg_id"]))
                await get.download_media(client.PATH + font)
            except:
                pass